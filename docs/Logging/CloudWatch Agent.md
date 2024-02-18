# CloudWatch Agent
## IAM Role
- CloudWatchAgentServerPolicy
## Install
``` bash
yum install -y amazon-cloudwatch-agent
```
## Wizard
``` bash
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```
## Start
``` bash
amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```