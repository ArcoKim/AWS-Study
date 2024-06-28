# EC2
``` yaml title="appspec.yml"
version: 0.0
os: linux
files:
  - source: /
    destination: /home/ec2-user
hooks:
  ApplicationStop:
    - location: scripts/stop.sh
      timeout: 60
      runas: root
  AfterInstall:
    - location: scripts/install.sh
      timeout: 60
      runas: root
  ApplicationStart:
    - location: scripts/start.sh
      timeout: 60
      runas: root
```
## Scripts
### Stop
``` yaml title="stop.sh"
#!/bin/bash
fuser -k 8080/tcp && echo "Stop Server" || echo "Not Running"
```
### Install
- Python
``` yaml title="install.sh"
#!/bin/bash
cd /home/ec2-user
/root/.local/bin/pip install -r requirements.txt
```
### Start
- Python
``` yaml title="start.sh"
#!/bin/bash
cd /home/ec2-user
nohup python3 -u app.pyc > nohup.out 2>&1 &
```
- Java
``` yaml title="start.sh"
#!/bin/bash
cd /home/ec2-user
filename=$(ls *.jar)
nohup java -jar $filename > nohup.out 2>&1 &
```
- Golang
``` yaml title="start.sh"
#!/bin/bash
cd /home/ec2-user
nohup ./main > nohup.out 2>&1 &
```