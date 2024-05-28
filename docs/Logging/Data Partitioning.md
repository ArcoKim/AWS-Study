# Data Partitioning

## Not Use Dynamic Partitioning
year={timestamp:yyyy}/month={timestamp:MM}/day={timestamp:dd}/

## partitionKeyFromQuery
### JQ Example
```
.time| sub("\\.[[:digit:]]+"; "")| strptime("%Y-%m-%d %H:%M:%S")| strftime("%Y")
```
### S3 Bucket Prefix
```
year=!{partitionKeyFromQuery:year}/month=!{partitionKeyFromQuery:month}/day=!{partitionKeyFromQuery:day}/hour=!{partitionKeyFromQuery:hour}/
```

## partitionKeyFromLambda
### Lambda
``` python
from __future__ import print_function
import base64
import json
import datetime

def lambda_handler(firehose_records_input, context):
    print("Received records for processing from DeliveryStream: " + firehose_records_input['deliveryStreamArn']
          + ", Region: " + firehose_records_input['region']
          + ", and InvocationId: " + firehose_records_input['invocationId'])

    firehose_records_output = {'records': []}
 
    for firehose_record_input in firehose_records_input['records']:
        payload = base64.b64decode(firehose_record_input['data'])
        json_value = json.loads(payload)

        firehose_record_output = {}
        time = datetime.datetime.strptime(json_value['time'], "%Y-%m-%dT%H:%M:%SZ")
        partition_keys = {"year": time.strftime('%Y'),
                          "month": time.strftime('%m'),
                          "day": time.strftime('%d'),
                          "hour": time.strftime('%H')
                          }

        firehose_record_output = {'recordId': firehose_record_input['recordId'],
                                  'data': firehose_record_input['data'],
                                  'result': 'Ok',
                                  'metadata': { 'partitionKeys': partition_keys }}

        firehose_records_output['records'].append(firehose_record_output)

    return firehose_records_output
```
### S3 Bucket Prefix
```
year=!{partitionKeyFromLambda:year}/month=!{partitionKeyFromLambda:month}/day=!{partitionKeyFromLambda:day}/hour=!{partitionKeyFromLambda:hour}/
```

## Partition Projection
``` sql
CREATE EXTERNAL TABLE `accesslog`(
  `time` timestamp, 
  `host` string, 
  `method` string, 
  `path` string, 
  `http` string, 
  `code` smallint)
PARTITIONED BY ( 
  `year` smallint, 
  `month` tinyint, 
  `day` tinyint, 
  `hour` tinyint)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://color-application-logs/'
TBLPROPERTIES (
  'classification'='parquet',
  'projection.enabled'='true',
  'projection.year.range'='2024,2025', 
  'projection.year.type'='integer',
  'projection.month.digits'='2', 
  'projection.month.range'='1,12',
  'projection.month.type'='integer',
  'projection.day.digits'='2',
  'projection.day.range'='1,31', 
  'projection.day.type'='integer',
  'projection.hour.digits'='2',
  'projection.hour.range'='0,23',
  'projection.hour.type'='integer')
```