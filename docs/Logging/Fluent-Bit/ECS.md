# ECS
## Config File Example
``` bash
[INPUT]
    Name tail
    Tag service-log
    Path /app/log/app.log
    Skip_Long_Lines   On
    Refresh_Interval  10
    Rotate_Wait       30

[FILTER]
    Name grep
    Match service-log
    Exclude log /healthcheck

[FILTER]
    Name aws
    Match service-log

[OUTPUT]
    Name cloudwatch
    Match   service-log
    region ap-northeast-2
    log_group_name /wsi/webapp/product
    log_stream_name $(ecs_task_id)
    auto_create_group true
    retry_limit 2
```
## Dockerfile
``` Dockerfile
FROM public.ecr.aws/aws-observability/aws-for-fluent-bit:stable
COPY product.conf /product.conf
```
## Task Definition
``` json
"firelensConfiguration": {
    "type": "fluentbit",
    "options": {
        "config-file-type": "file",
        "config-file-value": "/product.conf"
    }
}
```