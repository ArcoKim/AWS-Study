# Grafana
## Install with Helm
``` yaml title="values.yaml"
adminUser: admin
adminPassword: admin1234!

service:
  type: NodePort

persistence:
  enabled: true
```
``` bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install grafana grafana/grafana -n monitoring -f values.yaml
```