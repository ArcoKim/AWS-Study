# Resource
## Sidecar Injection
### Namespace
``` bash
kubectl label namespace wsi mesh=color
kubectl label namespace wsi appmesh.k8s.aws/sidecarInjectorWebhook=enabled
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
  name: color
spec:
  namespaceSelector:
    matchLabels:
      mesh: color
```
## VirtualNode
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualNode
metadata:
  name: color-count
  namespace: wsi
spec:
  awsName: color-count
  podSelector:
    matchLabels:
      app: count
  listeners:
    - portMapping:
        port: 4000
        protocol: http
  serviceDiscovery:
    dns:
      hostname: count.wsi.svc.cluster.local
  backends:
    - virtualService:
       virtualServiceRef:
          name: color-server
    - virtualService:
       virtualServiceRef:
          name: redis-server
```
## VirtualRouter
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualRouter
metadata:
  name: color-router
  namespace: wsi
spec:
  awsName: color-router
  listeners:
    - portMapping:
        port: 80
        protocol: http
  routes:
    - name: route-to-color-node
      httpRoute:
        match:
          prefix: /
        action:
          weightedTargets:
            - virtualNodeRef:
                name: blue
              weight: 1
            - virtualNodeRef:
                name: green
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
  name: color-svc
  namespace: wsi
spec:
  awsName: color-svc
  provider:
    virtualRouter:
        virtualRouterRef:
            name: color-router
```
### To VirtualNode
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualService
metadata:
  name: redis-server
  namespace: wsi
spec:
  awsName: redis-server
  provider:
    virtualNode:
      virtualNodeRef:
        name: redis
```
## VirtualGateway
``` bash
kubectl label namespace wsi gateway=color
```
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: VirtualGateway
metadata:
  name: color-gateway
spec:
  namespaceSelector:
    matchLabels:
      gateway: color
  podSelector:
    matchLabels:
      app: gateway
  listeners:
    - portMapping:
        port: 80
        protocol: http
```
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: color-gateway
  namespace: wsi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gateway
  template:
    metadata:
      labels:
        app: gateway
    spec:
      containers:
        - name: envoy
          image: public.ecr.aws/appmesh/aws-appmesh-envoy:v1.27.2.0-prod
          ports:
            - containerPort: 80
```
## GatewayRoute
``` yaml
apiVersion: appmesh.k8s.aws/v1beta2
kind: GatewayRoute
metadata:
  name: color-gateway-route
  namespace: wsi
spec:
  httpRoute:
    match:
      prefix: "/"
    action:
      target:
        virtualService:
          virtualServiceRef:
            name: color-ui
```