# Publish Function
``` bash
zip -r function.zip .
aws lambda update-function-code --function-name myFunction --zip-file fileb://myFunction.zip
```