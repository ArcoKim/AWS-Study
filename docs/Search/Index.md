# Index
## Create Index
``` json
PUT demo
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "time": {"type": "date"},
      "stream": {"type": "keyword"},
      "value": {"type": "text"},
      "order": {"type": "integer"},
      "tag": {"type": "object"}
    }
  }
}
```