# EKS (Fargate)
## Create Namespace
``` yaml
kind: Namespace
apiVersion: v1
metadata:
  name: aws-observability
  labels:
    aws-observability: enabled
```
## Create Policy
``` bash
aws iam create-policy --policy-name eks-fargate-logging-policy --policy-document file://iam_policy.json

aws iam attach-role-policy \
  --policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/eks-fargate-logging-policy \
  --role-name AmazonEKSFargatePodExecutionRole
```
## Resources
### CloudWatch Logs
``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: aws-logging
  namespace: aws-observability
data:
  flb_log_cw: "false"  # Set to true to ship Fluent Bit process logs to CloudWatch.
  filters.conf: |
    [FILTER]
        Name     parser
        Match    *
        Key_name log
        Parser   crio
    [FILTER]
        Name                kubernetes
        Match               kube.*
        Merge_Log           On
        Keep_Log            Off
        Buffer_Size         0
        Kube_Meta_Cache_TTL 300s
  output.conf: |
    [OUTPUT]
        Name               cloudwatch_logs
        Match              kube.*
        region             ap-northeast-2
        log_group_name     /aws/eks/fargate/app
        log_stream_prefix  fluent-bit-
        log_retention_days 60
        auto_create_group  true
  parsers.conf: |
    [PARSER]
        Name        crio
        Format      Regex
        Regex       ^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>P|F) (?<log>.*)$
        Time_Key    time
        Time_Format %Y-%m-%dT%H:%M:%S.%L%z
```
### OpenSearch
``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: aws-logging
  namespace: aws-observability
data:
  output.conf: |
    [OUTPUT]
      Name               es
      Match              *
      Host               search-example-gjxdcilagiprbglqn42jsty66y.region-code.es.amazonaws.com
      Port               443
      Index              app-log
      AWS_Auth           On
      AWS_Region         ap-northeast-2
      tls                On
      Time_Key           time
      Suppress_Type_Name On
```
### Kinesis Data Firehose
``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: aws-logging
  namespace: aws-observability
data:
  output.conf: |
    [OUTPUT]
     Name            kinesis_firehose
     Match           *
     region          ap-northeast-2
     delivery_stream demo-firehose
```