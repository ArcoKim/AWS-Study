# DynamoDB

## GET (GetItem)
### Integration request
``` json
{
    "TableName": "serverless-user-table",
    "Key": {
    	"id": {
            "S": "$input.params('id')"
        }
    }
}
```

### Integration response
``` json
{
    "id": $input.json('$.Item.id.S'),
    "age": $input.json('$.Item.age.S'),
    "company": $input.json('$.Item.company.S')
}
```

## POST (PutItem)
### Integration request
``` json
#if($input.params("id").contains("admin"))
#set($context.responseOverride.status = 500)
#else
{ 
    "TableName": "serverless-user-table",
    "Item": {
    	"id": {
            "S": "$input.params('id')"
        },
        "age": {
            "S": "$input.params('age')"
        },
        "company": {
            "S": "$input.params('company')"
        }
    }
}
#end
```

### Integration response
``` json
#if($context.responseOverride.status == 500)
{
    "message": "Internal server error"
}
#else
{
    "msg": "Success insert data"
}
#end
```