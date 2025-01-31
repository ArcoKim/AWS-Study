# Reloader
Reloader can watch changes in ConfigMap and Secret and do rolling upgrades on Pods with their associated DeploymentConfigs, Deployments, Daemonsets Statefulsets and Rollouts.

## Install
``` bash
helm repo add stakater https://stakater.github.io/stakater-charts
helm install reloader stakater/reloader --namespace reloader --create-namespace
```

## Usage
``` yaml
kind: Deployment
metadata:
  annotations:
    reloader.stakater.com/auto: "true"
```