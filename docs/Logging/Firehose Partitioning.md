# Firehose Partitioning
## Not Use Dynamic Partitioning
year={timestamp:yyyy}/month={timestamp:MM}/day={timestamp:dd}/

## partitionKeyFromQuery
### Year
.time| strptime("%Y-%m-%dT%H:%M:%S")| strftime("%Y")

### Month
.time| strptime("%Y-%m-%dT%H:%M:%S")| strftime("%m")

### Day
.time| strptime("%Y-%m-%dT%H:%M:%S")| strftime("%d")

### Hour
.time| strptime("%Y-%m-%dT%H:%M:%S")| strftime("%H")

### Minute
.time| strptime("%Y-%m-%dT%H:%M:%S")| strftime("%M")

### Second
.time| strptime("%Y-%m-%dT%H:%M:%S")| strftime("%S")

### S3 Bucket Prefix
year=!{partitionKeyFromQuery:year}/month=!{partitionKeyFromQuery:month}/day=!{partitionKeyFromQuery:day}/hour=!{partitionKeyFromQuery:hour}/