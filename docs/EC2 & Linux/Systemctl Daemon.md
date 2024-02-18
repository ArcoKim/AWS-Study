# Systemctl Daemon
Create file /etc/systemd/system/servicename.service
## Application
``` bash
[Unit]
Description=foo/bar service

[Service]
Type=simple
ExecStart=/home/ec2-user/app/app
WorkingDirectory=/home/ec2-user/app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
## Instance Restart / Terminate
``` bash
[Unit]
Description=my_shutdown Service
Before=shutdown.target reboot.target halt.target
Requires=network-online.target network.target

[Service]
KillMode=none
ExecStart=/bin/true
ExecStop=/home/ec2-user/scripts/terminate.sh
RemainAfterExit=yes
Type=oneshot

[Install]
WantedBy=multi-user.target
```
## Start Daemon
``` bash
systemctl daemon-reload
systemctl start servicename
systemctl status servicename
systemctl enable servicename
```