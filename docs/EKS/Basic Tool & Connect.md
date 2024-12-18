# Basic Tool & Connect

## Install AWS CLI V2
``` bash
pip3 install awscli --upgrade
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
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.31.2/2024-11-15/bin/linux/amd64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
kubectl completion bash | tee /etc/bash_completion.d/kubectl > /dev/null
```

- 1.30 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.30.6/2024-11-15/bin/linux/amd64/kubectl
```

- 1.29 Version
``` bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.29.10/2024-11-15/bin/linux/amd64/kubectl
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
pip3 install awscli --upgrade
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.31.2/2024-11-15/bin/linux/amd64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
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
echo "export CLUSTER_NAME=$(eksctl get clusters -o json | jq -r '.[0].Name')" >> ~/.bashrc
echo "export AWS_DEFAULT_REGION=$(aws configure get region)" >> ~/.bashrc
echo "export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)" >> ~/.bashrc
source ~/.bashrc
```
### Update Kubeconfig
``` bash
aws eks update-kubeconfig --name $CLUSTER_NAME
```