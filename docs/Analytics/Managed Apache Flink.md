# Managed Apache Flink
## Kinesis Data Stream
### CREATE TABLE - Source
``` sql
%flink.ssql
CREATE TABLE demo_table (
    id INTEGER,
    level VARCHAR(5),
    path VARCHAR(13),
    status INTEGER,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
)
PARTITIONED BY (id)
WITH (
    'connector' = 'kinesis',
    'stream' = 'demo-stream',
    'aws.region' = 'ap-northeast-2',
    'scan.stream.initpos' = 'LATEST',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);
```
### CREATE TABLE - Sink
``` sql
%flink.ssql(type=update)
CREATE TABLE output_table (
    level VARCHAR(5),
    counts INTEGER,
    hop_time TIMESTAMP(3)
)
WITH (
    'connector' = 'kinesis',
    'stream' = 'output-stream',
    'aws.region' = 'ap-northeast-2',
    'sink.partitioner' = 'random',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);
```
### INSERT & SELECT
``` sql
%flink.ssql(type=update)
INSERT INTO output_table
SELECT level,
       COUNT(*) AS counts,
       HOP_ROWTIME(event_time, INTERVAL '10' second, INTERVAL '1' minute) AS hop_time
FROM demo_table
GROUP BY HOP(event_time, INTERVAL '10' second, INTERVAL '1' minute), level;
```