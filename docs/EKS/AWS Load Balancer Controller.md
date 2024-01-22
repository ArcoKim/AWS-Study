# AWS Load Balancer Controller
## Create Policy
``` bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json
```
## Create ServiceAccount
``` bash
eksctl utils associate-iam-oidc-provider --cluster ${CLUSTER_NAME} --approve

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
  name: skills-ingress
  annotations:
    alb.ingress.kubernetes.io/load-balancer-name: skills-alb
    alb.ingress.kubernetes.io/target-type: instance
    alb.ingress.kubernetes.io/subnets: skills-public-a, skills-public-c
    alb.ingress.kubernetes.io/target-node-labels: node=app
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/healthcheck-path: /health
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
                name: skills-service
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
  name: skills-svc
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-name: skills-nlb
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: instance
    service.beta.kubernetes.io/aws-load-balancer-subnets: skills-public-a, skills-public-b
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
spec:
  type: LoadBalancer
  loadBalancerClass: service.k8s.aws/nlb
  selector:
    app: skills
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```