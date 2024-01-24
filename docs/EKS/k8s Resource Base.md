# k8s Resource Base
## Pod
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```
## Deployment
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skills-deployment
spec:
  selector:
    matchLabels:
      app: skills
  template:
    metadata:
      labels:
        app: skills
    spec:
      nodeSelector:
        node: app
      tolerations:
      - key: node
        operator: Equal
        value: app
        effect: NoSchedule
      containers:
      - name: nginx
        image: nginx:1.14.2
        resources:
          requests:
            cpu: 500m
            memory: 256Mi
          limits:
            cpu: 1
            memory: 512Mi
        ports:
        - containerPort: 80
      topologySpreadConstraints:
      - maxSkew: 1
        minDomains: 2
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: skills
```
## Service
``` yaml
apiVersion: v1
kind: Service
metadata:
  name: skills-service
spec:
  type: NodePort
  selector:
    app: skills
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```
## Secret
``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-basic-auth
type: Opaque
stringData:
  username: admin
  password: t0p-Secret
```