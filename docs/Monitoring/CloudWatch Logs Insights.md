# CloudWatch Logs Insights

# 2XX Filter
``` bash
fields @timestamp, @message
| filter @message like /\| 2[0-9][0-9] \|/
| filter @message not like /\/healthcheck/
| sort @timestamp desc
| limit 100
```