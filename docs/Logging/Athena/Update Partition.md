# Update Partition
``` python
import boto3

def lambda_handler(event, context):
    client = boto3.client('athena')

    config = {
        'OutputLocation': 's3://skills-app-arco/output/',
    }
    sql = 'MSCK REPAIR TABLE `skills_table`'
    context = {'Database': 'skills_db'}

    client.start_query_execution(QueryString = sql, 
                                 QueryExecutionContext = context,
                                 ResultConfiguration = config)
```