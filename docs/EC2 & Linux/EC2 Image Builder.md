# EC2 Image Builder
## Build
### Python
``` yaml
name: myapp
description: This is myapp document.
schemaVersion: 1.0

phases:
  - name: build
    steps:
      - name: InstallPip
        action: ExecuteBash
        inputs:
          commands:
            - yum install -y python3-pip
      - name: CreateAppDirectory
        action: CreateFolder
        inputs:
          - path: /opt/myapp
      - name: DownloadApp
        action: S3Download
        inputs:
          - source: s3://application-bucket-arco/app/*
            destination: /opt/myapp/
      - name: DownloadService
        action: S3Download
        inputs:
          - source: s3://application-bucket-arco/daemon/myapp.service
            destination: /etc/systemd/system/myapp.service
      - name: DownloadCWAgentConfig
        action: S3Download
        inputs:
          - source: s3://application-bucket-arco/daemon/config.json
            destination: /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
      - name: StartCWAgent
        action: ExecuteBash
        inputs:
          commands:
            - systemctl start amazon-cloudwatch-agent
            - systemctl enable amazon-cloudwatch-agent
      - name: InstallModule
        action: ExecuteBash
        inputs:
          commands:
            - pip install -r /opt/myapp/requirements.txt
      - name: LoadService
        action: ExecuteBash
        inputs:
          commands:
            - systemctl daemon-reload
            - systemctl start myapp
            - systemctl enable myapp
  - name: validate
    steps:
      - name: ValidateApp
        action: ExecuteBash
        inputs:
          commands:
            - curl localhost:8080/healthcheck
```

## Test
```yaml
name: MyappTestingDocument
description: This is myapp testing document.
schemaVersion: 1.0

phases:
  - name: test
    steps:
      - name: TestApp
        action: ExecuteBash
        inputs:
          commands:
            - curl localhost:8080/healthcheck
```