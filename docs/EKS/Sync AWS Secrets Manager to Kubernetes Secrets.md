# Sync AWS Secrets Manager to Kubernetes Secrets
## Install with Helm
Secrets Store CSI driver : Secrets Store CSI Driver for Kubernetes secrets - Integrates secrets stores with Kubernetes via a Container Storage Interface (CSI) volume.
``` yaml title="values.yaml"
syncSecret:
  enabled: true
```
``` bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install -n kube-system csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver -f values.yaml
```
AWS provider for the Secrets Store CSI Driver : Provider for the Secrets Store CSI driver that integrates with AWS Secrets Manager
``` yaml title="values.yaml"
tolerations:
- key: node
  operator: Equal
  value: app
  effect: NoSchedule
```
``` bash
helm repo add aws-secrets-manager https://aws.github.io/secrets-store-csi-driver-provider-aws
helm install -n kube-system secrets-provider-aws aws-secrets-manager/secrets-store-csi-driver-provider-aws
```
## Create ServiceAccount
Please note that you need to set SECRET_ARN.
``` bash
cat <<EOF > iam_policy.json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
        "Resource": ["$SECRET_ARN"]
    }]
}
EOF

POLICY_ARN=$(aws --region "$AWS_DEFAULT_REGION" --query Policy.Arn --output text iam create-policy --policy-name eksdemo-secretsmanager-policy --policy-document file://iam_policy.json)
eksctl create iamserviceaccount --name eksdemo-secretmanager-sa --region="$AWS_DEFAULT_REGION" --cluster "$CLUSTER_NAME" --namespace=wsi --attach-policy-arn "$POLICY_ARN" --approve --override-existing-serviceaccounts
```
## Apply SecretProviderClass
To use the Secrets Store CSI driver, create a SecretProviderClass custom resource to provide driver configurations and provider-specific parameters to the CSI driver.
``` yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: eks-demo-aws-secrets
spec:
  provider: aws
  secretObjects:
  - data:
    - key: DB_CONFIG_JSON
      objectName: dbsecret
    secretName: dbinfo
    type: Opaque
  parameters:
    objects: |
        - objectName: "dbsecret"
          objectType: "secretsmanager"
```
## Pod Test
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
spec:
  serviceAccountName: eksdemo-secretmanager-sa
  volumes:
  - name: secrets-store-inline
    csi:
       driver: secrets-store.csi.k8s.io
       readOnly: true
       volumeAttributes:
         secretProviderClass: "eks-demo-aws-secrets"
  containers:
  - image: public.ecr.aws/docker/library/busybox:1.36
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
    name: busybox
    volumeMounts:
    - name: secrets-store-inline
      mountPath: "/mnt/secrets-store"
      readOnly: true
    env:
    - name: DB_CONFIG_JSON
      valueFrom:
        secretKeyRef:
          name: dbinfo
          key: DB_CONFIG_JSON
```