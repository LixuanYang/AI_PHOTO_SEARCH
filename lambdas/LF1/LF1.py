import json
import boto3
import requests
import datetime
import requests_aws4auth
import base64


url = "https://search-photos-n2bxoybxyv2ezdnr6p4fcgakru.us-east-1.es.amazonaws.com/photos/P"
headers = {"Content-Type": "application/json"}

s3 = boto3.client('s3')
def detect_labels(photo, bucket):

    client=boto3.client('rekognition', region_name="us-east-1")
    '''
    self.rekog_client = boto3.client('rekognition', 'us-east-1')
    with open('cat_pic600.jpg', "rb") as cf:
        base64_image=base64.b64encode(cf.read())
        base_64_binary = base64.decodebytes(base64_image)
    resp = self.rekog_client.detect_labels(Image={'Bytes': base_64_binary})
    
    binaryPhoto = base64.b64encode(photo)
    print("binaryPhoto:",binaryPhoto)
    
    binarydata = base64.b64decode(binaryPhoto)
    print("binarydata:",binarydata)
    '''
    headerresponse = s3.head_object(
        Bucket=bucket,
        Key=photo
    )
    print("headerresponse:", headerresponse)
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=4)

    alllabel=[]
    for label in response['Labels']:
        alllabel.append(label['Name'])
    if "x-amz-meta-customlabels" in headerresponse['ResponseMetadata']["HTTPHeaders"]:
        customlabel = headerresponse['ResponseMetadata']["HTTPHeaders"]["x-amz-meta-customlabels"]
        #print(headerresponse)
        alllabel.append(customlabel)
    
    body={
        'objectKey': photo,
        'bucket': bucket,
        'createdTimestamp': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        'labels': alllabel
    }
    
    print(alllabel)
    es_response = requests.post(url, headers=headers, data=json.dumps(body),auth=("master","52Lxj1314&"))
    print(es_response.text)


def lambda_handler(event, context):
    photo=event["Records"][0]["s3"]["object"]["key"]
    #photo=event["Records"][0]["s3"]["object"]
    print(event)
    print(photo)
    bucket=event["Records"][0]["s3"]["bucket"]["name"]
    #bucket=event["Records"][0]["s3"]["bucket"]
    print(bucket)
    #labels = detect_labels(photo,bucket)
    #print(labels)
    detect_labels(photo,bucket)
  
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'x-amz-meta-customLabels',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET'
        },
        'body': json.dumps("Photo lables added successfully!")
    }
