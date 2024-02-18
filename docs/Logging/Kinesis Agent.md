# Kinesis Agent
## Install
``` bash
yum install -y aws-kinesis-agent
```
## IAM Policy
``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "kinesis:PutRecords"
            ],
            "Resource": "*"
        }
    ]
}
```
## Config Files
### Kinesis Data Stream
``` json title="/etc/aws-kinesis/agent.json"
{
  "cloudwatch.emitMetrics": true,
  "cloudwatch.endpoint": "monitoring.ap-northeast-2.amazonaws.com",
  "kinesis.endpoint": "kinesis.ap-northeast-2.amazonaws.com",

  "flows": [
    {
      "filePattern": "/opt/app/app.log",
      "kinesisStream": "skills-stream",
      "dataProcessingOptions": [
        {
          "optionName": "LOGTOJSON",
          "logFormat": "COMMONAPACHELOG",
          "matchPattern": "^([^ ]*) - \\[([^\\]]*)\\] \\[([^\\]]*)\\] \"([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) \"([^ ]*)\"\"",
          "customFieldNames": ["host", "time", "level", "method", "path", "http", "code", "micro", "agent"]
        }
      ]
    }
  ]
}
```
### Kinesis Data Firehose
``` json title="/etc/aws-kinesis/agent.json"
{
  "cloudwatch.emitMetrics": true,
  "cloudwatch.endpoint": "monitoring.ap-northeast-2.amazonaws.com",
  "firehose.endpoint": "firehose.ap-northeast-2.amazonaws.com",

  "flows": [
    {
      "filePattern": "/opt/app/app.log",
      "deliveryStream": "skills-firehose",
      "dataProcessingOptions": [
        {
          "optionName": "LOGTOJSON",
          "logFormat": "COMMONAPACHELOG",
          "matchPattern": "^([^ ]*) - \\[([^\\]]*)\\] \\[([^\\]]*)\\] \"([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) \"([^ ]*)\"\"",
          "customFieldNames": ["host", "time", "level", "method", "path", "http", "code", "micro", "agent"]
        }
      ]
    }
  ]
}
```
## Start
``` bash
service aws-kinesis-agent start
chkconfig aws-kinesis-agent on
```