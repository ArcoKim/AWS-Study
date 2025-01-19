# S3 Permission
``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSConfigBucketPermissionsCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::centralized-logs-demo",
      "Condition": { 
        "StringEquals": {
          "AWS:SourceAccount": "073813292468"
        }
      }
    },
    {
      "Sid": "AWSConfigBucketExistenceCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::centralized-logs-demo",
      "Condition": { 
        "StringEquals": {
          "AWS:SourceAccount": "073813292468"
        }
      }
    },
    {
      "Sid": "AWSConfigBucketDelivery",
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::centralized-logs-demo/config/AWSLogs/073813292468/Config/*",
      "Condition": { 
        "StringEquals": { 
          "s3:x-amz-acl": "bucket-owner-full-control",
          "AWS:SourceAccount": "073813292468"
        }
      }
    }
  ]
}
```