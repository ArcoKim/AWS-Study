# EKS (Daemonset)
## Namespace
```bash
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml
```
## ServiceAccount
``` bash
aws iam create-policy \
    --policy-name FluentBitIAMPolicy \
    --policy-document file://iam_policy.json

eksctl create iamserviceaccount \
  --cluster=$CLUSTER_NAME \
  --namespace=amazon-cloudwatch \
  --name=fluent-bit \
  --role-name FluentBitIAMRole \
  --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/FluentBitIAMPolicy \
  --approve
```
## ConfigMap
### Cluster Info
```bash
FluentBitHttpPort='2020'
FluentBitReadFromHead='Off'
[[ ${FluentBitReadFromHead} = 'On' ]] && FluentBitReadFromTail='Off'|| FluentBitReadFromTail='On'
[[ -z ${FluentBitHttpPort} ]] && FluentBitHttpServer='Off' || FluentBitHttpServer='On'
kubectl create configmap fluent-bit-cluster-info \
--from-literal=cluster.name=${CLUSTER_NAME} \
--from-literal=http.server=${FluentBitHttpServer} \
--from-literal=http.port=${FluentBitHttpPort} \
--from-literal=read.head=${FluentBitReadFromHead} \
--from-literal=read.tail=${FluentBitReadFromTail} \
--from-literal=logs.region=${AWS_DEFAULT_REGION} -n amazon-cloudwatch
```
### Config
```yaml title="configmap.yaml"
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: amazon-cloudwatch
  labels:
    k8s-app: fluent-bit
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush                     5
        Grace                     30
        Log_Level                 error
        Daemon                    off
        Parsers_File              parsers.conf
        HTTP_Server               ${HTTP_SERVER}
        HTTP_Listen               0.0.0.0
        HTTP_Port                 ${HTTP_PORT}
        storage.path              /var/fluent-bit/state/flb-storage/
        storage.sync              normal
        storage.checksum          off
        storage.backlog.mem_limit 5M

    [INPUT]
        Name                tail
        Tag                 application.*
        Path                /var/log/containers/customer*.log
        multiline.parser    docker, cri
        DB                  /var/fluent-bit/state/flb_container.db
        Mem_Buf_Limit       50MB
        Skip_Long_Lines     On
        Refresh_Interval    10
        Rotate_Wait         30
        storage.type        filesystem
        Read_from_Head      ${READ_FROM_HEAD}

    [FILTER]
        Name                kubernetes
        Match               application.*
        Kube_URL            https://kubernetes.default.svc:443
        Kube_Tag_Prefix     application.var.log.containers.
        Merge_Log           On
        Merge_Log_Key       log_processed
        K8S-Logging.Parser  On
        K8S-Logging.Exclude Off
        Labels              Off
        Annotations         Off
        Use_Kubelet         On
        Kubelet_Port        10250
        Buffer_Size         0

    [OUTPUT]
        Name                cloudwatch_logs
        Match               application.var.log.containers.customer*
        region              ${AWS_REGION}
        log_group_name      /wsi/webapp/customer
        log_stream_prefix   ${HOST_NAME}-
        auto_create_group   true

  parsers.conf: |
    [PARSER]
        Name   app
        Format regex
        Regex  ^(?<year>[^-]*)-(?<month>[^-]*)-(?<day>[^ ]*) (?<hour>[^:]*):(?<minute>[^:]*):(?<second>[^,]*),[^ ]* - - (?<ip>[^ ]*) (?<port>[^ ]*) (?<method>[^ ]*) (?<path>[^ ]*) (?<statuscode>[^ ]*)
```
```bash
kubectl apply -f configmap.yaml
```
## DaemonSet
```bash
kubectl apply -f https://raw.githubusercontent.com/ArcoKim/AWS-Study/main/docs/Logging/Fluent-Bit/daemonset.yaml
```