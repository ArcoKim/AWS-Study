# Advanced Tools
## kubectx + kubens
kubectx is a tool to switch between contexts (clusters) on kubectl faster.  
kubens is a tool to switch between Kubernetes namespaces (and configure them for kubectl) easily.
``` bash
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
kubectx -h
kubens -h
```
## K9s
K9s is a terminal based UI to interact with your Kubernetes clusters. The aim of this project is to make it easier to navigate, observe and manage your deployed applications in the wild.
``` bash
K9S_LATEST=$(curl --silent "https://api.github.com/repos/derailed/k9s/tags" | jq -r '.[0].name')
curl --silent --location "https://github.com/derailed/k9s/releases/download/${K9S_LATEST}/k9s_Linux_amd64.tar.gz" | tar xz -C /tmp
sudo cp /tmp/k9s /usr/local/bin
k9s version
```