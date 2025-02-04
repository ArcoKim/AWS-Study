# ECS
## Environment Variables set by init tag
```
AWS_REGION / ECS_LAUNCH_TYPE / ECS_CLUSTER / ECS_FAMILY
ECS_TASK_ARN / ECS_TASK_ID / ECS_REVISION / ECS_TASK_DEFINITION
```

## Config File Example
``` bash title="extra.conf"
[SERVICE]
    log_level    info
    Parsers_File /fluent-bit/parsers/extra.conf

[INPUT]
    Name              tail
    Tag               service-log
    Path              /app/log/app.log
    Skip_Long_Lines   On
    Refresh_Interval  10
    Rotate_Wait       30

[FILTER]
    Name    grep
    Match   *
    Exclude log /healthcheck

[FILTER]
    Name     parser
    Match    *
    Key_Name log
    Parser   demo

[OUTPUT]
    Name              cloudwatch_logs
    Match             *
    region            ap-northeast-2
    log_group_name    /wsi/webapp/product
    log_stream_name   ${ECS_TASK_ID}
    auto_create_group true
    retry_limit       2
```

``` bash title="parsers.conf"
[PARSER]
    Name        demo
    Format      regex
    Regex       ([^\s]+)\s(?<time>[^|]*)\s\|\s(?<status>[^ ]*)\s\|\s+(?<latency>[^ ]*)\s\|\s+(?<client_ip>[^ ]*)\s\|\s(?<method>[^ ]*)\s+"(?<path>[^ ]*)"
    Time_Key    time
    Time_Format %Y/%m/%d - %H:%M:%S
    Time_Keep   Off
    Types       status:integer
```

## Dockerfile
``` Dockerfile
FROM public.ecr.aws/aws-observability/aws-for-fluent-bit:init-latest
COPY extra.conf /fluent-bit/conf/extra.conf
COPY parsers.conf /fluent-bit/parsers/extra.conf
```

## Task Definition
``` json
"firelensConfiguration": {
    "type": "fluentbit",
    "options": {
        "config-file-type": "file",
        "config-file-value": "/fluent-bit/conf/extra.conf"
    }
}
```