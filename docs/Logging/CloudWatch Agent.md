# CloudWatch Agent
## IAM Role
- CloudWatchAgentServerPolicy
## Install
``` bash
yum install -y amazon-cloudwatch-agent
```
## Configuration
### Wizard
``` bash
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```
### File Example
``` json
{
    "agent": {
        "run_as_user": "cwagent"
    },
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/var/log/myapp.log",
                        "log_group_class": "STANDARD",
                        "log_group_name": "/app/myapp",
                        "log_stream_name": "{instance_id}",
                        "retention_in_days": -1
                    }
                ]
            }
        }
    }
}
```
## Start
``` bash
mv /opt/aws/amazon-cloudwatch-agent/bin/config.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
systemctl restart amazon-cloudwatch-agent
```