# Java
``` yaml title="buildspec.yml"
version: 0.2

phases:
  install:
    runtime-versions:
      java: corretto17
    commands:
      - wget https://services.gradle.org/distributions/gradle-8.7-bin.zip
      - mkdir /opt/gradle
      - unzip -d /opt/gradle gradle-8.7-bin.zip
      - export PATH=$PATH:/opt/gradle/gradle-8.7/bin
  build:
    commands:
      - gradle clean build

reports:
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/java-test-report:
    files:
      - '*.xml'
    base-directory: 'build/test-results/test'
    discard-paths: yes
    file-format: JUNITXML
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/java-coverage-report:
    files:
      - jacocoTestReport.xml
    base-directory: 'build/reports/jacoco/test'
    discard-paths: yes
    file-format: JACOCOXML

artifacts:
  files:
    - build/libs/*.jar
    - scripts/*
    - appspec.yml
  discard-paths: yes

cache:
  paths:
    - /root/.gradle/caches/**/*
```