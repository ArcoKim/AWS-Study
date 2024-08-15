# IAM Policy
## RunInstances (RequestTag)
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "AllowToDescribeAll",
			"Effect": "Allow",
			"Action": [
				"ec2:Describe*"
			],
			"Resource": "*"
		},
		{
			"Sid": "AllowRunInstances",
			"Effect": "Allow",
			"Action": "ec2:RunInstances",
			"Resource": [
				"arn:aws:ec2:*::image/*",
				"arn:aws:ec2:*::snapshot/*",
				"arn:aws:ec2:*:*:subnet/*",
				"arn:aws:ec2:*:*:network-interface/*",
				"arn:aws:ec2:*:*:security-group/*",
				"arn:aws:ec2:*:*:key-pair/*",
				"arn:aws:ec2:*:*:volume/*"
			]
		},
		{
			"Sid": "AllowRunInstancesWithRestrictions",
			"Effect": "Allow",
			"Action": [
				"ec2:RunInstances"
			],
			"Resource": [
				"arn:aws:ec2:*:*:instance/*"
			],
			"Condition": {
				"StringEquals": {
					"aws:RequestTag/wsi-project": "developer"
				}
			}
		},
		{
			"Sid": "AllowCreateTagsOnlyLaunching",
			"Effect": "Allow",
			"Action": [
				"ec2:CreateTags"
			],
			"Resource": [
				"arn:aws:ec2:*:*:instance/*"
			],
			"Condition": {
				"StringEquals": {
					"ec2:CreateAction": [
						"RunInstances"
					]
				}
			}
		}
	]
}
```

## TerminateInstances (ResourceTag)
``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowToDescribeAll",
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowTerminateInstancesWithRestrictions",
            "Effect": "Allow",
            "Action": [
                "ec2:TerminateInstances"
            ],
            "Resource": "arn:aws:ec2:*:*:instance/*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/wsi-project": "developer"
                }
            }
        }
    ]
}
```