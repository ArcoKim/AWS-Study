# CodeDeploy Agent
## Install Ruby
``` bash
yum update -y
yum install -y ruby
```
## Install CodeDeploy Agent
``` bash
AWS_DEFAULT_REGION="ap-northeast-2"
cd /home/ec2-user
wget https://aws-codedeploy-$AWS_DEFAULT_REGION.s3.$AWS_DEFAULT_REGION.amazonaws.com/latest/install
chmod +x ./install
./install auto
systemctl status codedeploy-agent.service
```