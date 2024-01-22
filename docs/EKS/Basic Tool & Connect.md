# Basic Tool & Connect
## Install AWS CLI V2
``` bash
yum update -y
yum remove -y awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
```
## Install Docker
Docker is responsible for pushing images to ECR.
``` bash
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
```
## Install Kubectl
Kubectl is a command line tool for communicating with a Kubernetes cluster's control plane, using the Kubernetes API.
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
```

- 1.28 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl
```

- 1.27 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.27.1/2023-04-19/bin/linux/amd64/kubectl
```

- 1.26 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.26.4/2023-05-11/bin/linux/amd64/kubectl
```

- 1.25 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.25.9/2023-05-11/bin/linux/amd64/kubectl
```

- 1.24 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.13/2023-05-11/bin/linux/amd64/kubectl
```

- 1.23 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.17/2023-05-11/bin/linux/amd64/kubectl
```

## Install Helm
Helm is the package manager for Kubernetes.
``` bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
## Install eksctl
eksctl is a simple CLI tool for creating and managing clusters on EKS.
``` bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
mv /tmp/eksctl /usr/local/bin
```
## Install All (EC2 User Data Script)
Please note that the HOME path must be set to /home/ec2-user.
``` bash
#!/bin/bash
yum update -y
yum remove -y awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl
chmod +x ./kubectl
HOME=/home/ec2-user
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
kubectl completion bash | tee /etc/bash_completion.d/kubectl > /dev/null
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
mv /tmp/eksctl /usr/local/bin
```
## Connect to EKS Cluster
### Set frequently used environment variables
```bash
echo "CLUSTER_NAME=$(eksctl get clusters -o json | jq -r '.[0].Name')" >> ~/.bashrc
echo "AWS_DEFAULT_REGION=ap-northeast-2" >> ~/.bashrc
echo "AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)" >> ~/.bashrc
source ~/.bashrc
```
### Update Kubeconfig
``` bash
aws eks update-kubeconfig --name $CLUSTER_NAME
```