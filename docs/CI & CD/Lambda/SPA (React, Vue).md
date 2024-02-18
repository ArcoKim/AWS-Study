# SPA (React, Vue)
Cloudfront Invalidation with Codepipeline
``` python
import boto3
import botocore
from time import time

cf = boto3.client('cloudfront')
code_pipeline = boto3.client('codepipeline')

def create_invalidation():
    DISTRIBUTION_ID = 'E3V00GOB0EULV5'
    try:
        res = cf.create_invalidation(
            DistributionId=DISTRIBUTION_ID,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        '/*'
                    ]
                },
                'CallerReference': str(time()).replace(".", "")
            }
        )
        return True
    except botocore.exceptions.ClientError as e:
        return False

def lambda_handler(event, context):
    job_id = event['CodePipeline.job']['id']
    if create_invalidation():
        code_pipeline.put_job_success_result(jobId=job_id)
    else:
        code_pipeline.put_job_failure_result(jobId=job_id, failureDetails={'message': "Check CloudWatch Logs.", 'type': 'JobFailed'})
```