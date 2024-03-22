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
  name: skills
spec:
  selector:
    matchLabels:
      app: skills
  template:
    metadata:
      labels:
        app: skills
    spec:
      terminationGracePeriodSeconds: 60
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
            memory: 512Mi
          limits:
            cpu: 500m
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
  name: skills
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
## StatefulSet
``` yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mysql
  serviceName: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql
          imagePullPolicy: IfNotPresent
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: root1234!
            - name: MYSQL_USER
              value: admin
            - name: MYSQL_PASSWORD
              value: admin1234!
            - name: MYSQL_DATABASE
              value: demo
          ports:
            - name: mysql
              containerPort: 3306
              protocol: TCP
          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: gp2
        resources:
          requests:
            storage: 10Gi
```
## Kustomize
``` yaml title="kustomization.yaml"
resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - hpa.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
```