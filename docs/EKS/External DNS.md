# External DNS
## Create IAM Policy
``` json title="policy.json"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": [
        "arn:aws:route53:::hostedzone/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets",
        "route53:ListTagsForResource"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```
``` bash
aws iam create-policy --policy-name "AllowExternalDNSUpdates" \
  --policy-document file://policy.json

export POLICY_ARN=$(aws iam list-policies \
  --query 'Policies[?PolicyName==`AllowExternalDNSUpdates`].Arn' --output text)
```
## Create ServiceAccount
``` bash
eksctl create iamserviceaccount \
  --cluster $CLUSTER_NAME \
  --name "external-dns" \
  --namespace externaldns \
  --attach-policy-arn $POLICY_ARN \
  --approve
```
## Install with Helm
``` yaml title="values.yaml"
env:
  - name: AWS_DEFAULT_REGION
    value: ap-northeast-2
```
``` bash
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm upgrade --install external-dns external-dns/external-dns -f values.yaml \
    --version 1.14.3 \
    --namespace externaldns \
    --set serviceAccount.create=false \
    --set serviceAccount.name=external-dns
```
## Use Case
### Ingress
``` yaml
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: test.app.local
```