# Rsyslog
## Install
``` bash
yum install -y rsyslog
systemctl start rsyslog
systemctl enable rsyslog
```
## Logs
|File Path|Description|
|---|---|
|/var/log/secure|Logs related to authentication-based access|
|/var/log/messages|A file where standard messages occurring on the system are logged.|
|/var/log/dmesg|Log output when the system boots|
|/var/log/xferlog|A file in which actions related to FTP connections are recorded.|
|/var/log/cron|File where cron-related information is recorded|
|/var/log/boot.log|Information related to the daemon that operates during booting is recorded.|
|/var/log/lastlog|A file (binary) in which the last information of each user who connected using telnet or ssh is recorded - lastlog command|
|/var/log/wtmp|Log (binary) including records of users connected using console, telnet, ftp, etc., records of system reboots, etc. - last command|
|/var/log/btmp|A log opposite to wtmp that records connection failures (binary) - lastb command|