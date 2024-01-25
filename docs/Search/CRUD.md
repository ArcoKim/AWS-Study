# CRUD
## Create
### With Document ID
``` json
PUT demo/_create/1
{
    "time": "2024-01-25T06:21:32.442423121Z",
    "stream": "stdout",
    "value": "hello",
    "order": 1,
    "tag": {
        "Name": "arcokim",
        "job": "developer"
    }
}
```
### Without document ID
``` json
POST demo/_doc
{
    "time": "2024-01-25T06:21:32.442423121Z",
    "stream": "stdout",
    "value": "hello",
    "order": 1,
    "tag": {
        "Name": "arcokim",
        "job": "developer"
    }
}
```
## Read
``` json
GET demo/_doc/1
```
## Update
### Update All
``` json
PUT demo/_doc/1
{
    "time": "2024-01-25T06:21:32.442423121Z",
    "stream": "stderr",
    "value": "hello [updated]",
    "order": 2,
    "tag": {
        "Name": "arcokim",
        "job": "developer"
    }
}
```
### Only some updates
``` json
POST demo/_update/1
{
    "doc": {
        "stream": "stderr",
        "value": "hello [updated]"
    }
}
```
## Delete
``` json
DELETE demo/_doc/1
```