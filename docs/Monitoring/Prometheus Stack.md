# Prometheus Stack
## Install with Helm
``` yaml title="values.yaml"
grafana:
  adminPassword: admin1234!
```
``` bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml
```