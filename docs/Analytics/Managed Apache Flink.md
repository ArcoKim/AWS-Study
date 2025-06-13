# Managed Apache Flink
## Kinesis Data Stream
### CREATE TABLE - Source
``` sql
%flink.ssql
CREATE TABLE input_table (
    id INTEGER,
    level VARCHAR(5),
    path VARCHAR(13),
    status INTEGER,
    event_time TIMESTAMP(0),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
)
PARTITIONED BY (id)
WITH (
    'connector' = 'kinesis',
    'stream' = 'input-stream',
    'aws.region' = 'ap-northeast-2',
    'scan.stream.initpos' = 'LATEST',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);
```
### CREATE TABLE - Sink
``` sql
%flink.ssql
CREATE TABLE output_table (
    level VARCHAR(5),
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    counts BIGINT
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
### TUMBLE
``` sql
%flink.ssql
INSERT INTO output_table
SELECT level, window_start, window_end, count(*) AS counts
FROM TABLE(TUMBLE(TABLE input_table, DESCRIPTOR(event_time), INTERVAL '20' SECONDS))
GROUP BY level, window_start, window_end;
```
### HOP
``` sql
%flink.ssql
INSERT INTO output_table
SELECT level, window_start, window_end, count(*) AS counts
FROM TABLE(HOP(TABLE input_table, DESCRIPTOR(event_time), INTERVAL '10' SECONDS, INTERVAL '30' SECONDS))
GROUP BY level, window_start, window_end;
```
### CUMULATE
``` sql
%flink.ssql
INSERT INTO output_table
SELECT level, window_start, window_end, count(*) AS counts
FROM TABLE(CUMULATE(TABLE input_table, DESCRIPTOR(event_time), INTERVAL '20' SECONDS, INTERVAL '1' MINUTE))
GROUP BY level, window_start, window_end;
```
### SESSION
``` sql
INSERT INTO output_table
SELECT level,
    SESSION_START(event_time, INTERVAL '30' SECONDS) AS window_start,
    SESSION_ROWTIME(event_time, INTERVAL '30' SECONDS) AS window_end,
    COUNT(*) AS counts
FROM input_table
GROUP BY level, SESSION(event_time, INTERVAL '30' SECONDS);
```