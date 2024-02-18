# Firehose Partitioning
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