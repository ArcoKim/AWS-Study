# Setting
## Install istioctl
``` bash
curl -L https://istio.io/downloadIstio | sh -
sudo cp istio-*/bin/istioctl /usr/local/bin/istioctl
istioctl version
```
## Istio profile
||default|demo|minimal|remote|empty|preview|ambient|
|---|---|---|---|---|---|---|---|
|Core components||||||||
|istio-egressgateway||✔||||||
|istio-ingressgateway|✔|✔||||✔||
|istiod|✔|✔|✔|||✔|✔|
|CNI|||||||✔|
|Ztunnel|||||||✔|

``` bash
istioctl install --set profile=demo -y
kubectl -n istio-system get pod,svc
```
## Istio operator
``` bash
istioctl operator init
kubectl -n istio-operator get all
```
### Profile Example
``` yaml title="profile.yaml"
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-profile
  namespace: istio-system
spec:
  profile: demo
  components:
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
        k8s:
          service:
            type: NodePort
```
## Install Sidecar
|Resource|Label|Enabled value|Disabled value|
|---|---|---|---|
|Namespace|istio-injection|enabled|disabled|
|Pod|sidecar.istio.io/inject|"true"|"false"|

### Namespace Config
``` bash
kubectl label namespace default istio-injection=enabled --overwrite
```
### Pod Config
``` bash
spec:
  template:
    metadata:
      labels:
        sidecar.istio.io/inject: "false"
```