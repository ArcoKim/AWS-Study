# Launch Template for Node Group
## Addon
``` json title="addon-config.json"
{
    "TagSpecifications": [{
        "ResourceType":"instance",
        "Tags":[{
            "Key":"Name",
            "Value":"wsi-addon-node"
        }]
    }],
    "BlockDeviceMappings":[{
        "DeviceName":"/dev/xvda",
        "Ebs":{
            "VolumeSize": 30,
            "VolumeType":"gp2",
            "DeleteOnTermination":true
        }
    }]
}
```
``` bash
aws ec2 create-launch-template \
    --launch-template-name wsi-addon-lt \
    --launch-template-data file://addon-config.json
```
## App
``` json title="app-config.json"
{
    "TagSpecifications": [{
        "ResourceType":"instance",
        "Tags":[{
            "Key":"Name",
            "Value":"wsi-app-node"
        }]
    }],
    "BlockDeviceMappings":[{
        "DeviceName":"/dev/xvda",
        "Ebs":{
            "VolumeSize": 30,
            "VolumeType":"gp2",
            "DeleteOnTermination":true
        }
    }],
    "MetadataOptions": {
        "HttpPutResponseHopLimit": 1
    }
}
```
``` bash
aws ec2 create-launch-template \
    --launch-template-name wsi-app-lt \
    --launch-template-data file://app-config.json
```