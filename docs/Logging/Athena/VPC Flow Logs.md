# VPC Flow Logs
``` sql
CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs (
  version int,
  account_id string,
  interface_id string,
  srcaddr string,
  dstaddr string,
  srcport int,
  dstport int,
  protocol bigint,
  packets bigint,
  bytes bigint,
  start bigint,
  `end` bigint,
  action string,
  log_status string,
  vpc_id string,
  subnet_id string,
  instance_id string,
  tcp_flags int,
  type string,
  pkt_srcaddr string,
  pkt_dstaddr string,
  az_id string,
  sublocation_type string,
  sublocation_id string,
  pkt_src_aws_service string,
  pkt_dst_aws_service string,
  flow_direction string,
  traffic_path int
)
PARTITIONED BY (accid string, region string, day string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://centralized-logs-demo/vpc-flow/'
TBLPROPERTIES
(
"skip.header.line.count"="1",
"projection.enabled" = "true",
"projection.accid.type" = "enum",
"projection.accid.values" = "073813292468",
"projection.region.type" = "enum",
"projection.region.values" = "ap-northeast-1,ap-northeast-2",
"projection.day.type" = "date",
"projection.day.range" = "2025/01/18,NOW",
"projection.day.format" = "yyyy/MM/dd",
"storage.location.template" = "s3://centralized-logs-demo/vpc-flow/AWSLogs/${accid}/vpcflowlogs/${region}/${day}"
)
```