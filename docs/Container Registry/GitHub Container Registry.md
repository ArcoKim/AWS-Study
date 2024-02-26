# GitHub Container Registry
## Personal access tokens (classic)
Select scopes
- write:packages
- read:packages
- delete:packages
## Login
``` bash
export CR_PAT=YOUR_TOKEN
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```
## Push
``` bash
docker push ghcr.io/NAMESPACE/IMAGE_NAME:latest
```