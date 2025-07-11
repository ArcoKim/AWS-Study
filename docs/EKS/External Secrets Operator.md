# External Secrets Operator
## Install
``` bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
   external-secrets/external-secrets \
   -n external-secrets \
   --create-namespace \
   --set installCRDs=true \
   --set webhook.port=9443
```
## Create ServiceAccount
### Secrets Manager
Please note that you need to set SECRET_ARN and KEY_ARN.
``` json title="iam_policy.json"
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
        "Resource": ["$SECRET_ARN"]
    },
    {
        "Effect": "Allow",
        "Action": ["kms:Decrypt"],
        "Resource": ["$KEY_ARN"]
    }]
}
```
### Command
Please note that you need to set NAMESPACE.
``` bash
POLICY_ARN=$(aws --region "$AWS_DEFAULT_REGION" --query Policy.Arn --output text iam create-policy --policy-name secretsmanager-policy --policy-document file://iam_policy.json)
eksctl create iamserviceaccount --name access-secrets --cluster $CLUSTER_NAME --namespace $NAMESPACE --attach-policy-arn $POLICY_ARN --approve --override-existing-serviceaccounts
```
## SecretStore
SecretStore is used to define the external secrets store and the authentication mechanisms to access the declared store.
``` yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: aws-secrets
spec:
  provider:
    aws:
      service: SecretsManager
      region: ap-northeast-2
      auth:
        jwt:
          serviceAccountRef:
            name: access-secrets
```
## ExternalSecret
ExternalSecret defines what data to fetch from the secret store defined in the SecretStore resource.
### data
``` yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: db-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: db-secret
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: cred/mysql
      property: username
  - secretKey: password
    remoteRef:
      key: cred/mysql
      property: password
```
### dataFrom
``` yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: db-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: db-secret
    creationPolicy: Owner
  dataFrom:
  - extract:
      key: cred/mysql
```