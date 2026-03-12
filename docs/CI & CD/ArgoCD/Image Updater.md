# Image Updater
## Helm Override Value
``` yaml title="values.yaml"
config:
  argocd:
    grpcWeb: true
    serverAddress: "http://argocd-server.argocd"
    insecure: true
    plaintext: true
  logLevel: debug
  registries:
    - name: ECR
      api_url: "https://ACCOUNT_ID.dkr.ecr.REGION_CODE.amazonaws.com"
      prefix: "ACCOUNT_ID.dkr.ecr.REGION_CODE.amazonaws.com"
      ping: true
      insecure: false
      credentials: "ext:/scripts/auth1.sh"
      credsexpire: 10h
authScripts:
  enabled: true
  scripts:
    auth1.sh: |
      #!/bin/sh
      aws ecr --region REGION_CODE get-authorization-token --output text --query 'authorizationData[].authorizationToken' | base64 -d
```
``` bash
sed -i "s|ACCOUNT_ID|$AWS_ACCOUNT_ID|g" values.yaml
sed -i "s|REGION_CODE|$AWS_DEFAULT_REGION|g" values.yaml
```
## Install with Helm
``` bash
helm install argocd-image-updater argo/argocd-image-updater \
    --namespace argocd \
    --values values.yaml
```
## ImageUpdater Example
- semver : update to highest allowed version according to given image constraint,
- newest-build : update to the most recently created image tag,
- alphabetical : update to the last tag in an alphabetically sorted list
- digest : update to the most recent pushed version of a mutable tag

``` yaml
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: product-updater
spec:
  namespace: argocd
  applicationRefs:
    - namePattern: "product"
      images:
        - alias: "org-app"
          imageName: "073813292468.dkr.ecr.ap-northeast-2.amazonaws.com/product"
          commonUpdateSettings:
            updateStrategy: "newest-build"
            allowTags: "any"
            pullSecret: "ext:/scripts/auth1.sh"
```