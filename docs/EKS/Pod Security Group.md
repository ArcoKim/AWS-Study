# Pod Security Group
## Attach Policy to ClusterRole
``` bash
cluster_role=$(aws eks describe-cluster --name $CLUSTER_NAME --query cluster.roleArn --output text | cut -d / -f 2)
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController --role-name $cluster_role
```
## Enable Pod ENI
``` bash
kubectl set env daemonset aws-node -n kube-system ENABLE_POD_ENI=true
kubectl get cninode -A  # [{"name":"SecurityGroupsForPods"}]
```
## Additional Actions

- If you use livenessProbe or readinessProbe
``` bash
kubectl patch daemonset aws-node -n kube-system \
  -p '{"spec": {"template": {"spec": {"initContainers": [{"env":[{"name":"DISABLE_TCP_EARLY_DEMUX","value":"true"}],"name":"aws-vpc-cni-init"}]}}}}'
```

- If you use NodeLocal DNSCache or Calico Networkpolicy or externalTrafficPolicy is Local
``` bash
kubectl set env daemonset aws-node -n kube-system POD_SECURITY_GROUP_ENFORCING_MODE=standard
```
## Deploy SecurityGroupPolicy
Please note that you will need to set the SG_ID variable.
``` yaml
apiVersion: vpcresources.k8s.aws/v1beta1
kind: SecurityGroupPolicy
metadata:
  name: wsi-sg-policy
spec:
  podSelector: 
    matchLabels:
      app: wsi
  securityGroups:
    groupIds:
      - ${SG_ID}
```