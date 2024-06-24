# Container Insights
## Create ServiceAccount
``` bash
eksctl create iamserviceaccount \
  --name cloudwatch-agent \
  --namespace amazon-cloudwatch --cluster $CLUSTER_NAME \
  --role-name AmazonEKS_CloudWatch_DriverRole  \
  --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
  --role-only \
  --approve
```
## Create Addon with AWSCLI
``` bash
aws eks create-addon \
  --addon-name amazon-cloudwatch-observability \
  --cluster-name $CLUSTER_NAME \
  --service-account-role-arn arn:aws:iam::$AWS_ACCOUNT_ID:role/AmazonEKS_CloudWatch_DriverRole \
  --configuration-values '{ "containerLogs": { "enabled": false } }'
```