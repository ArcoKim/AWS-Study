# IAM Policy
## CloudWatch Logs
``` json
{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"logs:CreateLogStream",
			"logs:CreateLogGroup",
			"logs:DescribeLogGroups",
			"logs:DescribeLogStreams",
			"logs:PutLogEvents",
            "logs:PutRetentionPolicy"
		],
		"Resource": "*"
	}]
}
```
## Kinesis Data Streams
``` json
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
## Kinesis Data Firehose
``` json
{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"firehose:PutRecordBatch"
		],
		"Resource": "*"
	}]
}
```
## OpenSearch
``` json
{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"es:ESHttp*"
		],
		"Resource": "*"
	}]
}
```