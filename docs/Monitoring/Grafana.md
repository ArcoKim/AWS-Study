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
## Grafana Dashboard Examples (Using Prometheus)
|Title|Import|
|---|---|
|Kubernetes cluster monitoring (via Prometheus)|3119|
|Kubernetes Pods Monitoring|6417|
|Kubernetes Deployment Statefulset Daemonset metrics|8588|
|Kubernetes Cluster|7249|
|Kubernetes All-in-one Cluster Monitoring KR|13770|