# OpenSearch Permission
## Grant All Access to IAM Role
Please note that you need to set several variables.
``` bash
ENDPOINT_URL=https://$(aws opensearch describe-domain --domain-name $DOMAIN_NAME --output text --query "DomainStatus.Endpoint")
curl -sS -u "$USERNAME:$PASSWORD" -X PATCH $ENDPOINT_URL/_opendistro/_security/api/rolesmapping/all_access?pretty -H 'Content-Type: application/json' -d '[{"op": "add", "path": "/backend_roles", "value": ["'$IAM_ROLE_ARN'"]}]'
```