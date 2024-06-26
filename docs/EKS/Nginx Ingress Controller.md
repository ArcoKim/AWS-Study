# Nginx Ingress Controller
## Install
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/aws/deploy.yaml
```
## NLB
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: skills
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /
            pathType: Exact
            backend:
              service:
                name: skills
                port:
                  number: 80
```