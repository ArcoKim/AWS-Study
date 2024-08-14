# EKS (Sidecar)
## ServiceAccount
``` bash
aws iam create-policy \
    --policy-name FluentdIAMPolicy \
    --policy-document file://iam_policy.json

eksctl create iamserviceaccount \
  --cluster=$CLUSTER_NAME \
  --namespace=fluentd \
  --name=fluentd \
  --role-name FluentdIAMPolicy \
  --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/FluentdIAMPolicy \
  --approve
```
## ConfigMap
### Fluent-Bit
``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: app
data:
  fluent-bit.conf: |-
    [SERVICE]
        Flush             5
        Grace             30
        Log_Level         info
        Daemon            off
        HTTP_Server       Off
        
    [INPUT]
        Name              tail
        Tag               ${POD_NAME}
        Path              /log/app.log
        Refresh_Interval  10
        
    [OUTPUT]
        Name              forward
        Match             *
        Host              fluentd.fluentd
        Port              24224
```
### Fluentd
``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: fluentd
data:
  fluent.conf: |-
    <source>
      @type forward
      bind 0.0.0.0
      port 24224
    </source>
    
    <match service-a-**>
      @type cloudwatch_logs
      region ap-northeast-2
      log_group_name /app/sample
      log_stream_name sample
      auto_create_stream true
      <buffer>
        flush_interval 5
      </buffer>
    </match>
```
## Pod
### Application
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample
  namespace: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sample
  template:
    metadata:
      labels:
        app: sample
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: sample
        image: sample
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: 250m
            memory: 512Mi
        ports:
          - containerPort: 8080
        volumeMounts:
          - name: log-volume
            mountPath: /log
      - name: default-fluentbit
        image: fluent/fluent-bit:latest
        imagePullPolicy: IfNotPresent
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
        volumeMounts:
          - name: config-volume
            mountPath: /fluent-bit/etc/
          - name: log-volume
            mountPath: /log
      volumes:
        - name: log-volume
          emptyDir: {}
        - name: config-volume
          configMap:
            name: fluent-bit-config
```
### Fluentd
``` yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: fluentd
spec:
  selector:
    matchLabels:
      k8s-app: fluentd-logging
  template:
    metadata:
      labels:
        k8s-app: fluentd-logging
    spec:
      terminationGracePeriodSeconds: 30
      serviceAccountName: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1.10.3-debian-cloudwatch-1.0
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        ports:
          - containerPort: 24224
        volumeMounts:
          - name: config-volume
            mountPath: /fluentd/etc
      volumes:
        - name: config-volume
          configMap:
            name: fluentd-config
---
apiVersion: v1
kind: Service
metadata:
  name: fluentd
  namespace: fluentd
spec:
  type: ClusterIP
  selector:
    k8s-app: fluentd-logging
  ports:
    - protocol: TCP
      port: 24224
      targetPort: 24224
```