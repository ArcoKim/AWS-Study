# CloudWatch Dashboard
## Example
``` json
{
    "widgets": [
        {
            "type": "metric",
            "x": 0,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
                "metrics": [
                    [ "AWS/ApplicationELB", "TargetResponseTime", "TargetGroup", "targetgroup/k8s-app-employee-3dd8ce8439/cf2005fe3a318a42", "LoadBalancer", "app/apdev-alb/f5e30a3118cfc1ef", { "label": "employee" } ],
                    [ "...", "targetgroup/k8s-app-token-d80a9ff87a/eb1b3626febc6905", ".", ".", { "label": "token" } ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "ap-northeast-2",
                "stat": "Average",
                "period": 60,
                "title": "Target Response Time"
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
                "metrics": [
                    [ "AWS/ApplicationELB", "RequestCountPerTarget", "TargetGroup", "targetgroup/k8s-app-employee-3dd8ce8439/cf2005fe3a318a42", "LoadBalancer", "app/apdev-alb/f5e30a3118cfc1ef", { "label": "employee", "region": "ap-northeast-2" } ],
                    [ "...", "targetgroup/k8s-app-token-d80a9ff87a/eb1b3626febc6905", ".", ".", { "label": "token", "region": "ap-northeast-2" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "region": "ap-northeast-2",
                "title": "Request Count Per Target",
                "stat": "Sum",
                "period": 60
            }
        },
        {
            "type": "log",
            "x": 0,
            "y": 6,
            "width": 8,
            "height": 5,
            "properties": {
                "query": "SOURCE '/app/employee' | fields time, log\n| filter log like /\\| 2[0-9][0-9] \\|/\n| sort time desc\n| limit 10000",
                "region": "ap-northeast-2",
                "stacked": false,
                "title": "Employee 2XX",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 8,
            "y": 6,
            "width": 8,
            "height": 5,
            "properties": {
                "query": "SOURCE '/app/employee' | fields time, log\n| filter log like /\\| 4[0-9][0-9] \\|/\n| sort time desc\n| limit 10000",
                "region": "ap-northeast-2",
                "stacked": false,
                "title": "Employee 4XX",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 16,
            "y": 6,
            "width": 8,
            "height": 5,
            "properties": {
                "query": "SOURCE '/app/employee' | fields time, log\n| filter log like /\\| 5[0-9][0-9] \\|/\n| sort time desc\n| limit 10000",
                "region": "ap-northeast-2",
                "stacked": false,
                "title": "Employee 5XX",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 0,
            "y": 11,
            "width": 8,
            "height": 5,
            "properties": {
                "query": "SOURCE '/app/token' | fields time, log\n| filter log like /\\| 2[0-9][0-9] \\|/\n| sort time desc\n| limit 10000",
                "region": "ap-northeast-2",
                "stacked": false,
                "title": "Token 2XX",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 8,
            "y": 11,
            "width": 8,
            "height": 5,
            "properties": {
                "query": "SOURCE '/app/token' | fields time, log\n| filter log like /\\| 4[0-9][0-9] \\|/\n| sort time desc\n| limit 10000",
                "region": "ap-northeast-2",
                "stacked": false,
                "title": "Token 4XX",
                "view": "table"
            }
        },
        {
            "type": "log",
            "x": 16,
            "y": 11,
            "width": 8,
            "height": 5,
            "properties": {
                "query": "SOURCE '/app/token' | fields time, log\n| filter log like /\\| 5[0-9][0-9] \\|/\n| sort time desc\n| limit 10000",
                "region": "ap-northeast-2",
                "stacked": false,
                "title": "Token 5XX",
                "view": "table"
            }
        }
    ]
}
```