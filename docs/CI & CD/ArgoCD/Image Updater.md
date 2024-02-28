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
TOKEN=$(argocd account generate-token --account image-updater --id image-updater)

sed -i "s|ARGOCD_TOKEN|$TOKEN|g" values.yaml
sed -i "s|ACCOUNT_ID|$AWS_ACCOUNT_ID|g" values.yaml
sed -i "s|REGION_CODE|$AWS_DEFAULT_REGION|g" values.yaml
```
## Install with Helm
``` bash
helm install argocd-image-updater argo/argocd-image-updater \
    --namespace argocd \
    --values values.yaml
```
## Annotation Example
- semver: update to highest allowed version according to given image constraint,
- latest: update to the most recently created image tag,
- name: update to the last tag in an alphabetically sorted list
- digest: update to the most recent pushed version of a mutable tag

``` yaml
argocd-image-updater.argoproj.io/image-list: org/app=<IMAGE_REPOSITORY_URL>/<IMAGE_REPOSITORY_NAME>
argocd-image-updater.argoproj.io/org_app.allow-tags: any
argocd-image-updater.argoproj.io/org_app.pull-secret: ext:/scripts/auth1.sh
argocd-image-updater.argoproj.io/org_app.update-strategy: semver
```