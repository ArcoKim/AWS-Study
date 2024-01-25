# EKS Logging
## Create ServiceAccount
### CloudWatch
``` json title="iam_policy.json"
{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"logs:CreateLogStream",
			"logs:CreateLogGroup",
			"logs:PutLogEvents"
		],
		"Resource": "*"
	}]
}
```
### Kinesis Data Streams
``` json title="iam_policy.json"
{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"kinesis:PutRecords"
		],
		"Resource": "*"
	}]
}
```
### Command
```
aws iam create-policy \
    --policy-name FluentBitIAMPolicy \
    --policy-document file://iam_policy.json

eksctl utils associate-iam-oidc-provider --cluster ${CLUSTER_NAME} --approve

eksctl create iamserviceaccount \
  --cluster=$CLUSTER_NAME \
  --namespace=kube-system \
  --name=aws-for-fluent-bit \
  --role-name FluentBitIAMRole \
  --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/FluentBitIAMPolicy \
  --approve
```
## Install with Helm
[Details](https://artifacthub.io/packages/helm/aws/aws-for-fluent-bit)
``` yaml title="values.yaml"
serviceAccount:
  create: false
  name: aws-for-fluent-bit

tolerations:
- key: node
  operator: Equal
  value: app
  effect: NoSchedule

cloudWatchLogs:
  enabled: true
  region: "ap-northeast-2"
  logGroupName: "/aws/eks/fluentbit-cloudwatch/logs"
  # logStreamName:
  logStreamPrefix: "fluentbit-"
  autoCreateGroup: true

kinesis:
  enabled: false
  region: "ap-northeast-2"
  stream: "wsi-streams"
  partitionKey: "container_id"
  # timeKey:
  # timeKeyFormat:

opensearch:
  enabled: false
  host: search-wsi-opensearch-abcdefg.ap-northeast-2.es.amazonaws.com
  awsRegion: "ap-northeast-2"
  tls: "On"
  awsAuth: "Off"
  Trace_Error: "On"
  httpUser: admin
  httpPasswd: Open1234!
  index: "aws-fluent-bit"
```
``` bash
helm repo add eks https://aws.github.io/eks-charts
helm upgrade --install aws-for-fluent-bit --namespace kube-system eks/aws-for-fluent-bit -f values.yaml
```