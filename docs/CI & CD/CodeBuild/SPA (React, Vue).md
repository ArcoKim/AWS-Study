# SPA (React, Vue)
## Install jest-junit
``` bash
npm install --save jest-junit
```
### Yaml File
``` yaml title="buildspec.yml"
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 16
  pre_build:
    commands:
      - npm install
  build:
    commands:
      - npm run build
  post_build:
    commands:
      - npm test -- --testResultsProcessor="jest-junit" --watchAll=false --ci --coverage

reports:
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/spa-report:
    files:
      - junit.xml
    file-format: JUNITXML
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/spa-coverage:
    files:
      - coverage/clover.xml
    file-format: CLOVERXML

artifacts:
  files:
    - build/**/*
  base-directory: 'build'

cache:
  paths:
    - node_modules/**/*
```