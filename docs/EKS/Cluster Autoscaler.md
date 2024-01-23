# Cluster Autoscaler
Cluster Autoscaler - a component that automatically adjusts the size of a Kubernetes Cluster so that all pods have a place to run and there are no unneeded nodes.
## Create IAM Policy
``` json title="cluster-autoscaler-policy.json"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeScalingActivities",
        "autoscaling:DescribeTags",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeLaunchTemplateVersions"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup",
        "ec2:DescribeImages",
        "ec2:GetInstanceTypesFromInstanceRequirements",
        "eks:DescribeNodegroup"
      ],
      "Resource": ["*"]
    }
  ]
}
```
``` bash
POLICY_ARN=$(aws iam create-policy \
    --policy-name AmazonEKSClusterAutoscalerPolicy \
    --policy-document file://cluster-autoscaler-policy.json \
    --query 'Policy.Arn' \
    --output text
)
```
## Create ServiceAccount
``` bash
eksctl create iamserviceaccount \
    --cluster=$CLUSTER_NAME \
    --namespace=kube-system \
    --name=cluster-autoscaler \
    --attach-policy-arn=$POLICY_ARN \
    --override-existing-serviceaccounts \
    --approve
```
## Install with Helm
``` bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm repo update autoscaler

helm install cluster-autoscaler autoscaler/cluster-autoscaler \
    --namespace kube-system \
    --set autoDiscovery.clusterName=$CLUSTER_NAME \
    --set awsRegion=$AWS_DEFAULT_REGION \
    --set cloudProvider=aws \
    --set extraArgs.logtostderr=true \
    --set extraArgs.stderrthreshold=info \
    --set extraArgs.v=4 \
    --set extraArgs.skip-nodes-with-local-storage=false \
    --set extraArgs.expander=least-waste \
    --set extraArgs.balance-similar-node-groups=true \
    --set extraArgs.skip-nodes-with-system-pods=false \
    --set rbac.serviceAccount.create=false \
    --set rbac.serviceAccount.name=cluster-autoscaler
```