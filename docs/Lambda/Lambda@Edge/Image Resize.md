# Image Resize
## IAM Role
### Trust Policy
``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "edgelambda.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
### Inline Policy
``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:GetFunction",
                "lambda:EnableReplication",
                "iam:CreateServiceLinkedRole",
                "cloudfront:UpdateDistribution",
                "s3:GetObject",
				"kms:Decrypt"
            ],
            "Resource": "*"
        }
    ]
}
```
## Install
``` bash
npm init -y
npm install sharp
npm install aws-sdk
```
## Function
``` javascript
import querystring from 'querystring';
import AWS from 'aws-sdk';
import Sharp from 'sharp';

const S3 = new AWS.S3({
  region: 'ap-northeast-2'
});

const BUCKET = 'wsi-static-coar';

const supportImageTypes = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'tiff'];

export const handler = async(event, context, callback) => {
  const { request, response } = event.Records[0].cf;

  const { uri } = request;
  
  const ObjectKey = decodeURIComponent(uri).substring(1);
  const params = querystring.parse(request.querystring);
  const { w, h, q, f } = params;

  /**
   * ex) https://dilgv5hokpawv.cloudfront.net/dev/thumbnail.png?w=200&h=150&f=webp&q=90
   * - ObjectKey: 'dev/thumbnail.png'
   * - w: '200'
   * - h: '150'
   * - f: 'webp'
   * - q: '90'
   */
  
  if (!(w || h)) {
    return callback(null, response);
  }

  const extension = uri.match(/\/?(.*)\.(.*)/)[2].toLowerCase();
  const width = parseInt(w, 10) || null;
  const height = parseInt(h, 10) || null;
  
  let format = (f || extension).toLowerCase();
  let s3Object;
  let resizedImage;

  if (extension === 'gif' && !f) {
    return callback(null, response);
  }

  format = format === 'jpg' ? 'jpeg' : format;

  if (!supportImageTypes.some(type => type === extension )) {
    responseHandler(
      403,
      'Forbidden',
      'Unsupported image type', [{
        key: 'Content-Type',
        value: 'text/plain'
      }],
    );

    return callback(null, response);
  }

  console.log(`parmas: ${JSON.stringify(params)}`);
  console.log('S3 Object key:', ObjectKey)

  try {
    s3Object = await S3.getObject({
      Bucket: BUCKET,
      Key: ObjectKey
    }).promise();

    console.log('S3 Object:', s3Object);
  }
  catch (error) {
    responseHandler(
      404,
      'Not Found',
      'The image does not exist.', [{ key: 'Content-Type', value: 'text/plain' }],
    );
    return callback(null, response);
  }

  try {
    resizedImage = await Sharp(s3Object.Body)
      .resize(width, height)
      .withMetadata()
      .toBuffer();
  }
  catch (error) {
    responseHandler(
      500,
      'Internal Server Error',
      'Fail to resize image.', [{
        key: 'Content-Type',
        value: 'text/plain'
      }],
    );
    return callback(null, response);
  }
  
  if (Buffer.byteLength(resizedImage, 'base64') >= 1048576) {
    return callback(null, response);
  }

  responseHandler(
    200,
    'OK',
    resizedImage.toString('base64'), [{
      key: 'Content-Type',
      value: `image/${format}`
    }],
    'base64'
  );

  function responseHandler(status, statusDescription, body, contentHeader, bodyEncoding) {
    response.status = status;
    response.statusDescription = statusDescription;
    response.body = body;
    response.headers['content-type'] = contentHeader;
    if (bodyEncoding) {
      response.bodyEncoding = bodyEncoding;
    }
  }
  
  console.log('Success resizing image');

  return callback(null, response);
};
```