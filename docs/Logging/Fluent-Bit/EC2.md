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
    Tag kinesis
    Parser color-kd
```
### FILTER Example
``` bash
[FILTER]
    Name    grep
    Match   *
    Exclude log /healthcheck
```
### OUTPUT Example
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
    Name color-kd
    Format regex
    Regex ^\[(?<time>[^\]]*)\] (?<host>[^ ]*) - - (?<method>[^ ]*) (?<path>[^ ]*) (?<HTTP>[^ ]*) (?<code>[^ ]*)
    Time_Key time
    Time_Format %Y-%m-%d %H:%M:%S,%L
    Time_Keep Off
    Types code:integer

# 127.0.0.1 - [14/Aug/2024:23:54:45 +0900] "GET /log HTTP/1.1" 200 "curl/7.54.1"
[PARSER]
    Name   logParser
    Format regex
    Regex  ^(?<clientip>[^ ]*) - \[(?<time>[^\]]*)\] "(?<method>[^ ]*) (?<path>[^ ]*) (?<protocol>[^"]*)" (?<responsecode>[^ ]*) "(?<useragent>[^"]*)"
    Time_Key time
    Time_Keep   On
    Time_Format %d/%b/%Y:%H:%M:%S %z
```