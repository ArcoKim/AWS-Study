# Karpenter
Just-in-time Nodes for Any Kubernetes Cluster
## AWS Infrastructure Setting
Use CloudFormation to set up the infrastructure needed by the EKS cluster. 
``` bash
KARPENTER_VERSION=$(curl -sL "https://api.github.com/repos/aws/karpenter/releases/latest" | jq -r ".tag_name")
TEMPOUT=$(mktemp)

curl -fsSL https://raw.githubusercontent.com/aws/karpenter/"${KARPENTER_VERSION}"/website/content/en/preview/getting-started/getting-started-with-karpenter/cloudformation.yaml  > $TEMPOUT \
&& aws cloudformation deploy \
  --stack-name "Karpenter-${CLUSTER_NAME}" \
  --template-file "${TEMPOUT}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "ClusterName=${CLUSTER_NAME}"
```
## IAM Setting
Create a Kubernetes service account and AWS IAM Role, and associate them using IRSA to let Karpenter launch instances.
``` bash
eksctl utils associate-iam-oidc-provider --cluster ${CLUSTER_NAME} --approve

eksctl create iamidentitymapping \
  --username system:node:{{EC2PrivateDNSName}} \
  --cluster "${CLUSTER_NAME}" \
  --arn "arn:aws:iam::${AWS_ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}" \
  --group system:bootstrappers \
  --group system:nodes

eksctl create iamserviceaccount \
  --cluster "${CLUSTER_NAME}" --name karpenter --namespace karpenter \
  --role-name "${CLUSTER_NAME}-karpenter" \
  --attach-policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME}" \
  --role-only \
  --approve
```
## Install
Run helm to install karpenter.
``` bash
KARPENTER_IAM_ROLE_ARN="arn:aws:iam::${AWS_ACCOUNT_ID}:role/${CLUSTER_NAME}-karpenter"

helm upgrade karpenter oci://public.ecr.aws/karpenter/karpenter \
  --install --version ${KARPENTER_VERSION:1} --namespace karpenter --create-namespace \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=${KARPENTER_IAM_ROLE_ARN} \
  --set settings.clusterName=${CLUSTER_NAME} \
  --set settings.interruptionQueueName=${CLUSTER_NAME} \
  --set controller.resources.requests.cpu=1 \
  --set controller.resources.requests.memory=1Gi \
  --set controller.resources.limits.cpu=1 \
  --set controller.resources.limits.memory=1Gi \
  --wait
```
## Tagging to Resources
Tag the subnet and security group the node will use. Please note that you need to set the ASG_NAME variable (auto scaling group name of addon node group).
``` bash
SUBNETS=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names $ASG_NAME --query 'AutoScalingGroups[0].VPCZoneIdentifier' --output text | tr ',' '\n')
for SUBNET in $SUBNETS
do
	aws ec2 create-tags --resources $SUBNET --tags Key=karpenter.sh/discovery,Value=${CLUSTER_NAME}
done

LAUNCH_TEMPLATE_ID=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names $ASG_NAME --query 'AutoScalingGroups[0].MixedInstancesPolicy.LaunchTemplate.LaunchTemplateSpecification.LaunchTemplateId' --output text)
SECURITY_GROUPS=$(aws ec2 describe-launch-template-versions --launch-template-id $LAUNCH_TEMPLATE_ID --versions $Latest --query 'LaunchTemplateVersions[0].LaunchTemplateData.SecurityGroupIds' --output text)
for SECURITY_GROUP in $SECURITY_GROUPS
do
	aws ec2 create-tags --resources $SECURITY_GROUP --tags Key=karpenter.sh/discovery,Value=${CLUSTER_NAME}
done
```
## Create NodePool
A single Karpenter NodePool is capable of handling many different pod shapes. Karpenter makes scheduling and provisioning decisions based on pod attributes such as labels and affinity.
``` yaml title="nodepool.yaml"
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    metadata:
      labels:
        node: app
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      taints:
        - key: node
          value: app
          effect: NoSchedule
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: kubernetes.io/os
          operator: In
          values: ["linux"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["2"]
#       - key: node.kubernetes.io/instance-type
#         operator: In
#         values: ["t3.medium", "t3.large"]
      expireAfter: 720h
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
  limits:
    cpu: 1000
```
``` yaml title="nodeclass.yaml"
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: Bottlerocket
  amiSelectorTerms:
    - id: "ami-02150f72c202ee9bb"
  role: "KarpenterNodeRole-${CLUSTER_NAME}"
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: ${CLUSTER_NAME}
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: ${CLUSTER_NAME}
  metadataOptions:
    httpPutResponseHopLimit: 1
  tags:
    Name: wsi-app-node
```