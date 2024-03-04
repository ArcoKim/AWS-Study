# IAM Policy
## CloudWatch
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
## Kinesis Data Streams
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
## Amazon OpenSearch Service
``` json title="iam_policy.json"
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
			  "es:ESHttp*"
			],
			"Resource": "*"
		}
	]
}
```