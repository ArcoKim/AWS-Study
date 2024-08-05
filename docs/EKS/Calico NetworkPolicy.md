# Calico NetworkPolicy
## Install calicoctl
``` bash
curl -L https://github.com/projectcalico/calico/releases/download/v3.27.2/calicoctl-linux-amd64 -o calicoctl
chmod +x ./calicoctl
sudo mv ./calicoctl /usr/local/bin/calicoctl
```
## Install Calico with Helm
``` bash
helm repo add projectcalico https://docs.tigera.io/calico/charts
echo '{ installation: {kubernetesProvider: EKS }}' > values.yaml
helm install calico projectcalico/tigera-operator \
  --version v3.28.1 -f values.yaml \
  --namespace tigera-operator --create-namespace
```
## Permissions and environment variable settings
``` bash
cat << EOF > append.yaml
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - patch
EOF
kubectl apply -f <(cat <(kubectl get clusterrole aws-node -o yaml) append.yaml)

kubectl set env daemonset aws-node -n kube-system ANNOTATE_POD_IP=true

CALICO_POD_NAME=$(kubectl get pods -n calico-system -o name | grep calico-kube-controllers- | cut -d '/' -f 2)
kubectl delete pod $CALICO_POD_NAME -n calico-system

CALICO_POD_NAME=$(kubectl get pods -n calico-system -o name | grep calico-kube-controllers- | cut -d '/' -f 2)
kubectl describe pod $CALICO_POD_NAME -n calico-system | grep vpc.amazonaws.com/pod-ips
```
## Resource
### Kubernetes NetworkPolicy
[NetworkPolicy Maker](https://editor.networkpolicy.io/)
``` yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: skills
spec:
  podSelector:
    matchLabels:
      app: skills
  policyTypes:
  - Ingress
  - Egress
  ingress:
    - from:
      - ipBlock:
          cidr: 10.0.0.0/24
    - from:
      - ipBlock:
          cidr: 10.0.1.0/24
    - from:
      - ipBlock:
          cidr: 10.0.2.0/24
  egress:
    - to:
      - ipBlock:
          cidr: 0.0.0.0/0
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
        - port: 80
          protocol: TCP
        - port: 443
          protocol: TCP
```
### Calico NetworkPolicy
[GlobalNetworkPolicy](https://docs.tigera.io/calico/latest/reference/resources/globalnetworkpolicy)
``` yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: default-deny
spec:
  selector: projectcalico.org/namespace not in  {'kube-system', 'calico-system', 'calico-apiserver', 'tigera-operator'}
  types:
  - Ingress
  - Egress
```
[NetworkPolicy](https://docs.tigera.io/calico/latest/reference/resources/networkpolicy)
``` yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: match
  namespace: skills
spec:
  selector: app == 'match'
  ingress:
    - action: Deny
      source:
        selector: app == 'stress'
    - action: Allow
      source:
        nets:
          - 10.0.0.0/24
          - 10.0.1.0/24
  egress:
    - action: Allow
      protocol: TCP
      destination:
        ports:
          - 53
          - 80
          - 443
    - action: Allow
      protocol: UDP
      destination:
        ports:
          - 53
```