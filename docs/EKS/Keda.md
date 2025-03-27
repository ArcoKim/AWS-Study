# Keda
## Create Policy
``` json title="iam_policy.json"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "GetQueueAttributes",
            "Effect": "Allow",
            "Action": "sqs:GetQueueAttributes",
            "Resource": "*"
        }
    ]
}
```

``` bash
aws iam create-policy \
    --policy-name SqsGetAttributesPolicy \
    --policy-document file://iam_policy.json
```

## Create ServiceAccount
``` bash
kubectl create namespace keda
eksctl create iamserviceaccount \
  --cluster=$CLUSTER_NAME \
  --namespace=keda \
  --name=keda-operator \
  --role-name=keda-operator-role \
  --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/SqsGetAttributesPolicy \
  --approve
```

## Install with Helm
``` bash
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda \
  -n keda \
  --set serviceAccount.operator.create=false \
  --set serviceAccount.operator.name=keda-operator
```

## ScaledObject
``` yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: sqsconsumer-hpa
  namespace: keda-sqs-guidance
spec:
  scaleTargetRef:
    name: sqs-consumer-backend
  minReplicaCount: 2
  maxReplicaCount: 100
  pollingInterval: 10
  cooldownPeriod:  10
  triggers:
  - type: aws-sqs-queue
    metadata:
      queueURL: https://sqs.ap-northeast-2.amazonaws.com/073813292468/skills-queue
      activationQueueLength: "0"
      queueLength: "5"
      awsRegion: ap-northeast-2
      identityOwner: operator
```

## Deployment Example
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata: 
  name: sqs-consumer-backend
  namespace: keda-sqs-guidance
spec:
  selector:
    matchLabels:
      app: sqs-consumer-backend
  template: 
    metadata:
      labels:
        app: sqs-consumer-backend
    spec:
      serviceAccountName: sqsconsumer
      containers:
      - name: sqs-consumer
        image: 073813292468.dkr.ecr.ap-northeast-2.amazonaws.com/sqsconsumer:latest
        env:
        - name: RELIABLE_QUEUE_NAME
          value: skills-queue
        - name: AWS_REGION
          value: ap-northeast-2
        - name: MAX_MSGS_PER_BATCH
          value: "5"
        - name: MSG_POLL_BACKOFF
          value: "2"
        - name: MSG_PROCESS_DELAY
          value: "10"
        - name: TOT_MSGS_TO_PROCESS
          value: "10000"
        - name: LOG_LEVEL
          value: INFO
```