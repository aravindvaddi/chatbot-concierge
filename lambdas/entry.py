import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('lex-runtime')
    msg = json.loads(event['body'])['messages'][0]['unstructured']['text']
    
    res = client.post_text(botName='nyu_order', botAlias='bot', userId='test', inputText=msg)
    
    response = {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps({"messages": [
            {
                "type": "unstructured",
                "unstructured": {
                    "text": res['message']
                }
            },
        ]})
    }
    
    return response
