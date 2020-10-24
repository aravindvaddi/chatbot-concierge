import json
import urllib3
import random
import boto3

global URL
URL = "https://search-index-2vgxmbvfaf5nr3rrf3u7f2a4ye.us-east-1.es.amazonaws.com/restaurants/"


def getData(cuisine, start, size):
    searchURL = URL + '_search?q=' + cuisine + '&from=' + str(start) + '&size=' + str(size)
    try:
        http = urllib3.PoolManager()
        result = http.request('GET', searchURL).data
        data = json.loads(result.decode('utf-8'))
        return data
    except:
        return None


def getValidRestaurants(IDs):
    client = boto3.client('dynamodb')

    restaurants = []

    for id in IDs:
        data = client.get_item(TableName='yelp-restaurants',
                               Key={'RestaurantID': {'S': id}})

        data = data['Item']
        name = data['name']['S']
        address = data['address']['S']
        rating = data['rating']['S']
        phoneNumber = data['phone']['S']
        restaurants.append([name, address, rating, phoneNumber])

    restaurants.sort(key=lambda x: x[2], reverse=True)
    return restaurants[:3]


def getRestaurantIDs(hits):
    return [item['_source']['RestaurantID'] for item in hits]


def buildMessage(people, diningTime, data):
    base = "Here are top suggestions for {} people, for today at {}. ".format(people, diningTime)
    # base = ""
    i = 0
    flag = True
    while flag and i < 3:
        temp = "{} located at {} reachable at {}. ".format(data[i][0], data[i][1][:-6], data[i][3])
        if len(temp) + len(base) < 480:
            base += temp
            i += 1
        else:
            flag = False
    return base


def sendMessage(message, phoneNumber):
    client = boto3.client('sns')
    response = client.publish(PhoneNumber=phoneNumber, Message=message)
    return response


def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    queue = 'https://sqs.us-east-1.amazonaws.com/231323952634/custQ'
    res = sqs.receive_message(
        QueueUrl = queue,
        MaxNumberOfMessages=10
    )
    
    print(res)
    
    for message in res['Messages']:
        details = json.loads(message['Body'])
        cuisine = details['cuisine']
        people = details['people']
        phoneNumber = "+1" + details['number']
        diningTime = details['time']
    
        size = 3
        start = random.randrange(700)
    
        data = getData(cuisine=cuisine, start=start, size=size)
        hits = data['hits']['hits']
        IDs = getRestaurantIDs(hits=hits)
    
        data = getValidRestaurants(IDs)
        message = buildMessage(people, diningTime, data)
        try:
            response = sendMessage(message, phoneNumber)
        except Exception as e:
            print(e)
            print("Sending message failed")
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
    }
