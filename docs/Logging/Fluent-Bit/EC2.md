# EC2
## Install
``` bash
curl https://raw.githubusercontent.com/fluent/fluent-bit/master/install.sh | sh

systemctl start fluent-bit
systemctl enable fluent-bit

ln -s /opt/fluent-bit/bin/fluent-bit /usr/local/bin/fluent-bit
```
## Write Config File
``` bash
cd /etc/fluent-bit
vim fluent-bit.conf
```
### INPUT Example
``` bash
[INPUT]
    Name tail
    Path /app/app.log
    Tag i-005c3f6eec2ed4a8e
    Parser color-cw

[INPUT]
    Name tail
    Path /app/app.log
    Tag kinesis
    Parser color-kd
```
### OUTPUT Example
- CloudWatch
``` bash
[OUTPUT]
    Name cloudwatch_logs
    Match i-*
    region ap-northeast-2
    log_group_name wsi/app/accesslog
    log_stream_prefix ec2_
    auto_create_group On
```
- Kinesis Data Stream
``` bash
[OUTPUT]
    Name kinesis_streams
    Match kinesis
    region ap-northeast-2
    stream wsi-log
    time_key time
    time_key_format %Y-%m-%d %H:%M:%S.%3N
```
## Write Parser File
``` bash
cd /etc/fluent-bit
vim parsers.conf
```
``` bash
# [2023-08-21 20:51:47,662] 127.0.0.1 - - GET /v1/color/red HTTP/1.1 200
[PARSER]
    Name color-cw
    Format regex
    Regex ^\[(?<time>[^\]]*)\] (?<host>[^ ]*) - - (?<method>[^ ]*) (?<path>[^ ]*) (?<HTTP>[^ ]*) (?<code>[^ ]*)
    Types code:integer

[PARSER]
    Name color-kd
    Format regex
    Regex ^\[(?<time>[^\]]*)\] (?<host>[^ ]*) - - (?<method>[^ ]*) (?<path>[^ ]*) (?<HTTP>[^ ]*) (?<code>[^ ]*)
    Time_Key time
    Time_Format %Y-%m-%d %H:%M:%S,%L
    Time_Keep Off
    Types code:integer
```