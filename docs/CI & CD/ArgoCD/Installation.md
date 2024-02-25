# Installation
## Helm
``` yaml title="values.yaml"
configs:
  cm:
    accounts.image-updater: apiKey
    timeout.reconciliation: 60s
  rbac:
    policy.csv: |
      p, role:image-updater, applications, get, */*, allow
      p, role:image-updater, applications, update, */*, allow
      g, image-updater, role:image-updater
    policy.default: role.readonly
  params:
    server.insecure: true
```
``` bash
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

helm repo add argo https://argoproj.github.io/argo-helm
helm repo update argo

helm install argocd argo/argo-cd \
    --create-namespace \
    --namespace argocd \
    --values values.yaml
```
## Port Forward
``` bash
kubectl port-forward svc/argocd-server -n argocd --address=0.0.0.0 8080:443
```
## Login
``` bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
argocd login 127.0.0.1:8080  # ID : admin
argocd account update-password
```