# ECS
``` yaml title="appspec.yaml"
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: <TASK_DEFINITION>
        LoadBalancerInfo:
          ContainerName: wsi-app
          ContainerPort: 8080
```