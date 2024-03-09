# Data Partitioning Example
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