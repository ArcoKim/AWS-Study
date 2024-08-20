# EKS
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
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
      - git config --global credential.helper '!aws codecommit credential-helper $@'
      - git config --global credential.UseHttpPath true
      - git config --global user.name "root"
      - git config --global user.email "root@localhost"
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - git clone https://git-codecommit.ap-northeast-2.amazonaws.com/v1/repos/sample
      - cd sample
      - "sed -i \"s|image: .*|image: $REPOSITORY_URI:$IMAGE_TAG|\" rollouts.yaml"
      - git add .
      - git commit -m "Update Image Tag $IMAGE_TAG"
      - git push origin main
```