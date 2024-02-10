# Resource
## Sidecar Injection
### Namespace
``` bash
kubectl label namespace yelb mesh=yelb
kubectl label namespace yelb appmesh.k8s.aws/sidecarInjectorWebhook=enabled
```
### Deployment
``` yaml
spec:
  template:
    spec:
      serviceAccountName: envoy-proxy
```
## Mesh
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: Mesh
metadata:
  name: yelb
spec:
  namespaceSelector:
    matchLabels:
      mesh: yelb
```
## VirtualNode
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualNode
metadata:
  name: yelb-appserver
  namespace: yelb
spec:
  awsName: yelb-appserver-virtual-node
  podSelector:
    matchLabels:
      app: yelb-appserver
  listeners:
    - portMapping:
        port: 4567
        protocol: http
  serviceDiscovery:
    dns:
      hostname: yelb-appserver.yelb.svc.cluster.local
  backends:
    - virtualService:
       virtualServiceRef:
          name: yelb-db
    - virtualService:
       virtualServiceRef:
          name: redis-server
```
## BackendGroup
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: BackendGroup
metadata:
  name: yelb-group
  namespace: yelb
spec:
  virtualservices:
    - name: yelb-db
      namespace: yelb
    - name: redis-server
      namespace: yelb
```
### VirtualNode Example
``` yaml
spec:
  backendGroups:
    - name: yelb-group
      namespace: yelb
```
## VirtualRouter
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualRouter
metadata:
  namespace: yelb
  name: yelb-appserver
spec:
  awsName: yelb-appserver-virtual-router
  listeners:
    - portMapping:
        port: 4567
        protocol: http
  routes:
    - name: route-to-yelb-appserver
      httpRoute:
        match:
          prefix: /
        action:
          weightedTargets:
            - virtualNodeRef:
                name: yelb-appserver
              weight: 1
            - virtualNodeRef:
                name: yelb-appserver-v2
              weight: 1
        retryPolicy:
            maxRetries: 2
            perRetryTimeout:
                unit: ms
                value: 2000
            httpRetryEvents:
                - server-error
                - client-error
                - gateway-error
```
## VirtualService
### To VirtualRouter
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualService
metadata:
  name: yelb-appserver
  namespace: yelb
spec:
  awsName: yelb-appserver
  provider:
    virtualRouter:
        virtualRouterRef:
            name: yelb-appserver
```
### To VirtualNode
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualService
metadata:
  name: yelb-ui
  namespace: yelb
spec:
  awsName: yelb-ui
  provider:
    virtualNode:
      virtualNodeRef:
        name: yelb-ui
```
## VirtualGateway
``` bash
kubectl label namespace yelb gateway=yelb-gateway
```
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualGateway
metadata:
  name: yelb-gateway
  namespace: yelb
spec:
  namespaceSelector:
    matchLabels:
      gateway: yelb-gateway
  podSelector:
    matchLabels:
      app: yelb-gateway
  listeners:
    - portMapping:
        port: 8088
        protocol: http
```
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yelb-gateway
  namespace: yelb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: yelb-gateway
  template:
    metadata:
      labels:
        app: yelb-gateway
    spec:
      containers:
        - name: envoy
          image: public.ecr.aws/appmesh/aws-appmesh-envoy:v1.27.2.0-prod
          ports:
            - containerPort: 8088
```
## GatewayRoute
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: GatewayRoute
metadata:
  name: yelbapp-gatewayroute
  namespace: yelb
spec:
  httpRoute:
    match:
      prefix: "/api"
    action:
      target:
        virtualService:
          virtualServiceRef:
            name: yelb-appserver
```