# Systemctl Daemon
Create file /etc/systemd/system/servicename.service
## Application
``` bash
[Unit]
Description=foo/bar service

[Service]
Type=simple
EnvironmentFile=/opt/foobar/.env
ExecStart=/opt/foobar/app
WorkingDirectory=/opt/foobar
Restart=on-failure
StandardOutput=file:/var/log/foobar.log
StandardError=file:/var/log/foobar.log

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
ExecStop=/opt/scripts/terminate.sh
RemainAfterExit=yes
Type=oneshot

[Install]
WantedBy=multi-user.target
```

## Timer
``` bash title="interval.service"
[Unit]
Description=my_interval service

[Service]
Type=oneshot
ExecStart=/opt/scripts/interval.sh

[Install]
WantedBy=multi-user.target
```
``` bash title="interval.timer"
[Unit]
Description=my_interval timer

[Timer]
OnCalendar=minutely

[Install]
WantedBy=timers.target
```

## Start Daemon
``` bash
systemctl daemon-reload
systemctl start servicename
systemctl status servicename
systemctl enable servicename
```