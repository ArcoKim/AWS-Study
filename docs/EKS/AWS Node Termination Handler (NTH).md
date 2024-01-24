# AWS Node Termination Handler (NTH)
This project ensures that the Kubernetes control plane responds appropriately to events that can cause your EC2 instance to become unavailable, such as EC2 maintenance events, EC2 Spot interruptions, ASG Scale-In, ASG AZ Rebalance, and EC2 Instance Termination via the API or Console. If not handled, your application code may not stop gracefully, take longer to recover full availability, or accidentally schedule work to nodes that are going down.
## Deploy CloudFormation Stack
Please note that you need to set the STACK_NAME variable.
``` bash
curl -LO https://raw.githubusercontent.com/aws/aws-node-termination-handler/main/docs/cfn-template.yaml

aws cloudformation deploy \
    --template-file ./cfn-template.yaml \
    --stack-name $STACK_NAME
```
## Create an ASG Termination Lifecycle Hook
Please note that you need to set the AUTO_SCALING_GROUP_NAME variable.
``` bash
aws autoscaling put-lifecycle-hook \
  --lifecycle-hook-name=my-k8s-term-hook \
  --auto-scaling-group-name=$AUTO_SCALING_GROUP_NAME \
  --lifecycle-transition=autoscaling:EC2_INSTANCE_TERMINATING \
  --default-result=CONTINUE \
  --heartbeat-timeout=300
```
## Auto Scaling Group Tagging
Please note that you need to set the AUTO_SCALING_GROUP_NAME variable.
``` bash
aws autoscaling create-or-update-tags \
  --tags ResourceId=$AUTO_SCALING_GROUP_NAME,ResourceType=auto-scaling-group,Key=aws-node-termination-handler/managed,Value=,PropagateAtLaunch=true
```
## Create ServiceAccount
``` json title="nth-policy.json"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "autoscaling:CompleteLifecycleAction",
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeTags",
                "ec2:DescribeInstances",
                "sqs:DeleteMessage",
                "sqs:ReceiveMessage"
            ],
            "Resource": "*"
        }
    ]
}
```
``` bash
POLICY_ARN=$(aws iam create-policy \
	--policy-name nth-policy \
	--policy-document file://nth-policy.json \
	--query 'Policy.Arn' \
	--output text
)

eksctl utils associate-iam-oidc-provider --cluster $CLUSTER_NAME --approve

eksctl create iamserviceaccount \
    --cluster $CLUSTER_NAME \
    --name aws-node-termination-handler \
    --namespace kube-system \
    --attach-policy-arn $POLICY_ARN \
    --role-name AWS_NTH_Role \
    --approve
```
## Install with Helm
Please note that you need to set the STACK_NAME variable.
``` bash
QUEUE_URL=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query "Stacks[0].Outputs[?OutputKey=='QueueURL'].OutputValue" \
    --output text
)

helm repo add eks https://aws.github.io/eks-charts

helm install aws-node-termination-handler eks/aws-node-termination-handler \
    --namespace kube-system \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-node-termination-handler \
    --set enableSqsTerminationDraining=true \
    --set queueURL=$QUEUE_URL
```