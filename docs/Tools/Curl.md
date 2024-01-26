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
### With Header
``` bash
curl -I google.com  # Only Header
curl -i google.com  # Header with Body
```