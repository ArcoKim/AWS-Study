# Kyverno
## Install
``` bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm install kyverno kyverno/kyverno -n kyverno --create-namespace \
--set admissionController.replicas=3 \
--set backgroundController.replicas=2 \
--set cleanupController.replicas=2 \
--set reportsController.replicas=2
```
## ClusterPolicy
``` yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  background: false
  rules:
  - name: require-image-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      failureAction: Enforce
      message: "An image tag is required."
      foreach:
        - list: "request.object.spec.containers"
          pattern:
            image: "*:*"
        - list: "request.object.spec.initContainers"
          pattern:
            image: "*:*"
        - list: "request.object.spec.ephemeralContainers"
          pattern:
            image: "*:*"
  - name: validate-image-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      failureAction: Audit
      message: "Using a mutable image tag e.g. 'latest' is not allowed."
      foreach:
        - list: "request.object.spec.containers"
          pattern:
            image: "!*:latest"
        - list: "request.object.spec.initContainers"
          pattern:
            image: "!*:latest"
        - list: "request.object.spec.ephemeralContainers"
          pattern:
            image: "!*:latest"
```