# Multi-platform images
## Installing emulators
``` bash
docker run --privileged --rm tonistiigi/binfmt --install all
```
## Create
``` bash
docker buildx create --use --name multiarch
```
## Build & Push
``` bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t 073813292468.dkr.ecr.ap-northeast-2.amazonaws.com/demo \
  --push .
```