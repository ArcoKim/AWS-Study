# S3 Access Logs
``` sql
CREATE EXTERNAL TABLE s3_access_logs (
 `bucketowner` STRING, 
 `bucket_name` STRING, 
 `requestdatetime` STRING, 
 `remoteip` STRING, 
 `requester` STRING, 
 `requestid` STRING, 
 `operation` STRING, 
 `key` STRING, 
 `request_uri` STRING, 
 `httpstatus` STRING, 
 `errorcode` STRING, 
 `bytessent` BIGINT, 
 `objectsize` BIGINT, 
 `totaltime` STRING, 
 `turnaroundtime` STRING, 
 `referrer` STRING, 
 `useragent` STRING, 
 `versionid` STRING, 
 `hostid` STRING, 
 `sigv` STRING, 
 `ciphersuite` STRING, 
 `authtype` STRING, 
 `endpoint` STRING, 
 `tlsversion` STRING,
 `accesspointarn` STRING,
 `aclrequired` STRING)
 PARTITIONED BY (
   `timestamp` string)
ROW FORMAT SERDE 
 'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDEPROPERTIES ( 
 'input.regex'='([^ ]*) ([^ ]*) \\[(.*?)\\] ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (\"[^\"]*\"|-) (-|[0-9]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (\"[^\"]*\"|-) ([^ ]*)(?: ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*))?.*$') 
STORED AS INPUTFORMAT 
 'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
 's3://centralized-logs-demo/static-s3/073813292468/ap-northeast-2/static-demo-s3/'
 TBLPROPERTIES (
  'projection.enabled'='true', 
  'projection.timestamp.format'='yyyy/MM/dd', 
  'projection.timestamp.interval'='1', 
  'projection.timestamp.interval.unit'='DAYS', 
  'projection.timestamp.range'='2025/01/18,NOW', 
  'projection.timestamp.type'='date', 
  'storage.location.template'='s3://centralized-logs-demo/static-s3/073813292468/ap-northeast-2/static-demo-s3/${timestamp}')
```