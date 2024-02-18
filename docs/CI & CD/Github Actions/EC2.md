# EC2
``` yaml
name: Deploy to Amazon EC2

on:
  push:
    branches:
    - main
  workflow_dispatch:

env:
  AWS_REGION: ap-northeast-2
  S3_BUCKET_NAME: deploy-archive-arco
  CODE_DEPLOY_APPLICATION_NAME: ec2-deploy
  CODE_DEPLOY_DEPLOYMENT_GROUP_NAME: ec2-golang-dg

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout release
      uses: actions/checkout@v4
       
    - name: Setup Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'
    
    - name: Build
      run: go build -o main

    - name: AWS configure credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
        
    - name: Upload to AWS S3
      run: |
        aws deploy push \
          --application-name $CODE_DEPLOY_APPLICATION_NAME \
          --s3-location s3://$S3_BUCKET_NAME/$GITHUB_SHA.zip \
          --ignore-hidden-files \
          --source .
      
    - name: Deploy to AWS EC2 from S3
      run: |
        aws deploy create-deployment \
          --application-name $CODE_DEPLOY_APPLICATION_NAME \
          --deployment-config-name CodeDeployDefault.AllAtOnce \
          --deployment-group-name $CODE_DEPLOY_DEPLOYMENT_GROUP_NAME \
          --s3-location bucket=$S3_BUCKET_NAME,key=$GITHUB_SHA.zip,bundleType=zip
```