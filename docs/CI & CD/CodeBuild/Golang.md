# Golang
``` yaml title="buildspec.yml"
version: 0.2

phases:
  install:
    runtime-versions:
      golang: 1.18
  pre_build:
    commands:
      - go mod download
      - go install github.com/jstemmer/go-junit-report/v2@latest
      - go install github.com/axw/gocov/gocov@latest
      - go install github.com/AlekSi/gocov-xml@latest
  build:
    commands:
      - go build -o main main.go
  post_build:
    commands:
      - go test -v 2>&1 ./... | go-junit-report -set-exit-code > test.xml
      - gocov test | gocov-xml > coverage.xml

reports:
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/go-test-report:
    files:
      - test.xml
    file-format: JUNITXML
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/go-coverage-report:
    files:
      - coverage.xml
    file-format: COBERTURAXML

artifacts:
  files:
    - main
    - scripts/*
    - templates/*
    - appspec.yaml

cache:
  paths:
    - /go/pkg/**/*
```