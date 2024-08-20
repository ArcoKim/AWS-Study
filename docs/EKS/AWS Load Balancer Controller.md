# AWS Load Balancer Controller
## Subnet Tag
|Subnet|Key|Value|
|---|---|---|
|Private|kubernetes.io/role/internal-elb|1|
|Public|kubernetes.io/role/elb|1|

## Create Policy
``` bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json
```
## Create ServiceAccount
``` bash
eksctl create iamserviceaccount \
  --cluster=$CLUSTER_NAME \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
```
## Install with Helm
``` bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=$CLUSTER_NAME \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```
## Resources
### Ingress
``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: skills
  annotations:
    alb.ingress.kubernetes.io/load-balancer-name: skills-alb
    alb.ingress.kubernetes.io/load-balancer-attributes: access_logs.s3.enabled=true,access_logs.s3.bucket=my-access-log-bucket,access_logs.s3.prefix=my-app
    alb.ingress.kubernetes.io/target-type: instance
    alb.ingress.kubernetes.io/target-node-labels: node=app
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/security-groups: sg-xxxx
    alb.ingress.kubernetes.io/healthcheck-path: /health
    alb.ingress.kubernetes.io/certificate-arn: $CERTIFICATE_ARN
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/actions.response-403: >
      {"type":"fixed-response","fixedResponseConfig":{"contentType":"text/plain","statusCode":"403","messageBody":"403 Forbidden"}}
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /
            pathType: Exact
            backend:
              service:
                name: skills
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: response-403
                port:
                  name: use-annotation
```
### Service
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: skills
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-name: skills-nlb
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: instance
    service.beta.kubernetes.io/aws-load-balancer-target-node-labels: node=app
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-protocol: http
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-path: /health
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: $CERTIFICATE_ARN
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "443"
spec:
  type: LoadBalancer
  loadBalancerClass: service.k8s.aws/nlb
  selector:
    app: skills
  ports:
    - protocol: TCP
      port: 443
      targetPort: 80
```
### TargetGroupBinding
``` yaml
apiVersion: elbv2.k8s.aws/v1beta1
kind: TargetGroupBinding
metadata:
  name: skills
spec:
  nodeSelector:
    matchLabels:
      node: app
  serviceRef:
    name: skills-service
    port: 80
  targetGroupARN: $TARGET_ARN
```