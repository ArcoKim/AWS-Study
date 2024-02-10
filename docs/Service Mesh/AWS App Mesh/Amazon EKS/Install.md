# Install
## App Mesh Controller
### Create CRD
``` bash
sudo yum install -y git

kubectl apply -k "github.com/aws/eks-charts/stable/appmesh-controller/crds?ref=master"
```
### Create Policy
``` bash
curl -o controller-iam-policy.json https://raw.githubusercontent.com/aws/aws-app-mesh-controller-for-k8s/master/config/iam/controller-iam-policy.json
aws iam create-policy \
    --policy-name AWSAppMeshK8sControllerIAMPolicy \
    --policy-document file://controller-iam-policy.json
```
### Create ServiceAccount
``` bash
kubectl create ns appmesh-system

eksctl create iamserviceaccount \
    --cluster $CLUSTER_NAME \
    --namespace appmesh-system \
    --name appmesh-controller \
    --attach-policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSAppMeshK8sControllerIAMPolicy  \
    --override-existing-serviceaccounts \
    --approve
```
### Install with Helm
``` bash
helm repo add eks https://aws.github.io/eks-charts
helm upgrade -i appmesh-controller eks/appmesh-controller \
    --namespace appmesh-system \
    --set region=$AWS_DEFAULT_REGION \
    --set serviceAccount.create=false \
    --set serviceAccount.name=appmesh-controller
```
## Envoy
### Create Policy
``` bash
curl -o envoy-iam-policy.json https://raw.githubusercontent.com/aws/aws-app-mesh-controller-for-k8s/master/config/iam/envoy-iam-policy.json
aws iam create-policy \
    --policy-name AWSAppMeshEnvoyIAMPolicy \
    --policy-document file://envoy-iam-policy.json
```
### Create ServiceAccount
``` bash
eksctl create iamserviceaccount \
    --cluster $CLUSTER_NAME \
    --namespace yelb \
    --name envoy-proxy \
    --attach-policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSAppMeshEnvoyIAMPolicy  \
    --override-existing-serviceaccounts \
    --approve
```