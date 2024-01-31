# Calico NetworkPolicy
## Install Calico with Helm
``` bash
helm repo add projectcalico https://docs.tigera.io/calico/charts
echo '{ installation: {kubernetesProvider: EKS }}' > values.yaml
helm install calico projectcalico/tigera-operator --version v3.25.1 -f values.yaml --namespace tigera-operator --create-namespace
```
## Permissions and environment variable settings
``` bash
cat << EOF > append.yaml
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - patch
EOF
kubectl apply -f <(cat <(kubectl get clusterrole aws-node -o yaml) append.yaml)

kubectl set env daemonset aws-node -n kube-system ANNOTATE_POD_IP=true

CALICO_POD_NAME=$(kubectl get pods -n calico-system -o name | grep calico-kube-controllers- | cut -d '/' -f 2)
kubectl delete pod $CALICO_POD_NAME -n calico-system

CALICO_POD_NAME=$(kubectl get pods -n calico-system -o name | grep calico-kube-controllers- | cut -d '/' -f 2
kubectl describe pod $CALICO_POD_NAME -n calico-system | grep vpc.amazonaws.com/pod-ips
```
## Resource
[NetworkPolicy Maker](https://editor.networkpolicy.io/)
``` yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: skills
spec:
  podSelector:
    matchLabels:
      app: skills
  policyTypes:
  - Ingress
  - Egress
  ingress:
    - from:
      - ipBlock:
          cidr: 10.0.0.0/24
    - from:
      - ipBlock:
          cidr: 10.0.1.0/24
    - from:
      - ipBlock:
          cidr: 10.0.2.0/24
  egress:
    - to:
      - ipBlock:
          cidr: 0.0.0.0/0
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
        - port: 80
          protocol: TCP
        - port: 443
          protocol: TCP
```