import json
import boto3
import os
import sys
import uuid
import time
import requests
import datetime
import requests_aws4auth


#ElasticSearch
url = "https://search-photos-n2bxoybxyv2ezdnr6p4fcgakru.us-east-1.es.amazonaws.com/photos/P"
HEADERS = {"Content-Type": "application/json"}

#s3
S3_BUCKET = 'lixuanyanghw2'


#Lex
lex_client = boto3.client('lexv2-runtime')


def get_slots(query):
    
    response = lex_client.recognize_text(
        botId='TN1TXW6ZBX', # MODIFY HERE
        botAliasId='IENBVIPEFR', # MODIFY HERE
        localeId='en_US',
        sessionId='testuser',
        text=query
        )
    
    if 'interpretations' in response.keys():
        slots = response['interpretations'][0]['intent']['slots']
        if (slots['slot1']!=None) and (slots["slot2"]!=None):
            slotOne = slots['slot1']['value']['interpretedValue']
            slotTwo = slots['slot2']['value']['interpretedValue']
            slotlist = [slotOne,slotTwo]
        else:
            slotOne = slots['slot1']['value']['interpretedValue']
            slotlist = [slotOne]
        res = slotlist, True
    else:
        res = {}, False
    
    return res


def get_response(code, body):
    response = {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT',
            'Access-Control-Allow-Headers': 'Content-Type'
            
        },
        'body': json.dumps(body),
        'isBase64Encoded': False
    }
    print('get_response:', response)
    return response


def search_intent(slots):
    img_list = []
    objKeys = set()
    print('search intent, slots: {}'.format(slots))
    for tag in slots:
        if tag:
            tag = plural(tag)
            searchurl = url + '/_search?q=' + tag +"&size=50"
            #print('ES URL --- {}'.format(searchurl))
            '''
            query = {
                "query": {
                    "multi_match": {
                        "query": tag
                    }
                }
            }
            '''
            #es_response = requests.get(searchurl, headers=HEADERS, auth =("master","52Lxj1314&"),data=json.dumps(query))
            es_response = requests.get(searchurl, headers=HEADERS, auth =("master","52Lxj1314&")).json()
            print('ES RESPONSE --- {}'.format(json.dumps(es_response)))

            if 'hits' in es_response:
                es_src = es_response['hits']['hits']
                print('ES HITS --- {}'.format(json.dumps(es_src)))
                for photo in es_src:
                    labels = [obj.lower() for obj in photo['_source']['labels']]
                    if tag.lower() in labels:
                        objKey = photo['_source']['objectKey']
                        if objKey not in objKeys:
                            objKeys.add(objKey)
                            img_url = "https://lixuanyanghw2.s3.amazonaws.com/" + objKey
                            img_list.append(img_url)
    print('img_list: {}'.format(img_list))
    return img_list





def plural(word):
    if word.endswith('s'):
        return word[:-1]
    return word


def lambda_handler(event, context):
    # recieve from API Gateway
    print("event:",event)
    queryParam = event['queryStringParameters']
    
    if not queryParam:
        return get_response(400, 'Bad request, nothing in query params.')
    query = queryParam['q']
    print(query)


    slots, valid = get_slots(query)
    if not valid:
        get_response(200, 'Lex does not comprehend.')
        
    print(slots)
    
    #return get_response(200, 'Good')
    
    img_list = search_intent(slots)
    
    print('img_list:{}'.format(img_list))
    if img_list:
        return get_response(200, img_list)
    else:
        res = 'slots: ' + json.dumps(slots) + ', no photos matching the keyword.'
        return get_response(200, res)