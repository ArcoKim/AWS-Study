# Helm Chart
## Command
### Create
``` bash
helm create [product]
```
### Check
``` bash
helm lint [Root Path]
helm template [Root Path]
```
### Install / Upgrade
``` bash
helm install [Release Name] . --set version=latest -n wsi --create-namespace
helm upgrade [Release Name] . --set version=latest -n wsi
```
### Delete
``` bash
helm delete [Release Name]
```
## File Example
### Chart.yaml
``` yaml
apiVersion: v2

name: product
description: Product Helm Chart (Using MySQL Aurora)
type: application

version: 0.1.0
appVersion: "1.0.0"
```
### values.yaml
``` yaml
image.tag: "1.0.0"
```
### templates/NOTES.txt
```
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}
```
### templates/*.yaml
``` yaml
metadata:
  name: {{ .Release.Name }}
  namespace: {{ .Release.Namespace }}
```
### templates/deployment.yaml
``` yaml
spec:
  template:
    spec:
      containers:
      - name: nginx
        image: {{ .Values.image.name }}:{{ .Values.image.tag }}
```