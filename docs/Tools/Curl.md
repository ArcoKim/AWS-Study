# Curl
## GET
``` bash
curl "http://localhost:8080/data?key1=value1&key2=value2"
```
## POST
``` bash
curl -d '{"key1":"value1", "key2":"value2"}' \
-H "Content-Type: application/json" \
-X POST http://localhost:8080/data
```