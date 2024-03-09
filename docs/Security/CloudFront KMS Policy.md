# CloudFront KMS Policy
``` json
{
    "Sid": "Allow users or roles to use KMS to CloudFront.",
    "Effect": "Allow",
    "Principal": {
        "Service": [
            "cloudfront.amazonaws.com"
        ]
     },
    "Action": [
        "kms:Decrypt",
        "kms:Encrypt",
        "kms:GenerateDataKey*"
    ],
    "Resource": "*",
    "Condition":{
        "StringEquals":{
            "aws:SourceArn": "arn:aws:cloudfront::<account id>:distribution/<cloudfront distribution id>"
        }
    }
}
```