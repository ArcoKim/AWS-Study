# Task Definition
## Fargate
``` json
{
    "containerDefinitions": [
        {
            "name": "yelb-appserver",
            "image": "mreferre/yelb-appserver:0.7",
            "essential": true,
            "dependsOn": [
                {
                    "containerName": "envoy",
                    "condition": "HEALTHY"
                }
            ]
        },
        {
            "name": "envoy",
            "image": "public.ecr.aws/appmesh/aws-appmesh-envoy:v1.27.2.0-prod",
            "memory": 512,
            "essential": true,
            "environment": [
                {
                    "name": "APPMESH_VIRTUAL_NODE_NAME",
                    "value": "mesh/yelb/virtualNode/yelb-appserver"
                }
            ],
            "user": "1337",
            "healthCheck": {
                "command": [
                    "CMD-SHELL",
                    "curl -s http://localhost:9901/server_info | grep state | grep -q LIVE"
                ],
                "interval": 5,
                "timeout": 2,
                "retries": 3,
                "startPeriod": 10
            }
        }
    ],
    "taskRoleArn": "arn:aws:iam::073813292468:role/envoy-access-role",
    "proxyConfiguration": {
        "type": "APPMESH",
        "containerName": "envoy",
        "properties": [
            {
                "name": "ProxyIngressPort",
                "value": "15000"
            },
            {
                "name": "AppPorts",
                "value": "4567"
            },
            {
                "name": "EgressIgnoredIPs",
                "value": "169.254.170.2,169.254.169.254"
            },
            {
                "name": "EgressIgnoredPorts",
                "value": "22"
            },
            {
                "name": "IgnoredUID",
                "value": "1337"
            },
            {
                "name": "ProxyEgressPort",
                "value": "15001"
            }
        ]
    }
}
```