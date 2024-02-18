# Python
``` yaml title="buildspec.yml"
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9
  pre_build:
    commands:
      - pip install -r requirements.txt
  build:
    commands:
      - python -m compileall app.py
      - mv __pycache__/app.cpython-37.pyc app.pyc
  post_build:
    commands:
      - pytest --junitxml=test.xml
      - coverage run -m pytest
      - coverage xml

reports:
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/py-test-report:
    files:
      - test.xml
    file-format: JUNITXML
  arn:aws:codebuild:ap-northeast-2:073813292468:report-group/py-coverage-report:
    files:
      - coverage.xml
    file-format: COBERTURAXML

artifacts:
  files:
    - requirements.txt 
    - app.pyc
    - scripts/*
    - templates/*
    - appspec.yml

cache:
  paths:
    - /root/.cache/pip/**/*
```