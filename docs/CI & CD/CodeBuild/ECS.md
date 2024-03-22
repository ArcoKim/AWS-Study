# ECS
``` yaml
version: 0.2

env:
  variables:
    AWS_ACCOUNT_ID: 073813292468
    REPOSITORY_NAME: wsi-app

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPOSITORY_NAME
      - aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 073813292468.dkr.ecr.ap-northeast-2.amazonaws.com
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
```
## Rolling
``` yaml
phases:
  post_build:
    commands:
      - echo Writing image definitions file...
      - printf '[{"name":"wsi","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
```
## Blue / Green
``` yaml
phases:
  post_build:
    commands:
      - echo Writing image details file...
      - printf '{"ImageURI":"%s"}' $REPOSITORY_URI:$IMAGE_TAG > imageDetail.json

artifacts:
  files:
    - appspec.yml
    - taskdef.json
    - imageDetail.json
```