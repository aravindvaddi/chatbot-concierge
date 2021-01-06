import json
import urllib3
import random
import boto3

# TODO edit the below url
URL = "https://<AWS ELASTIC SEARCH URL>/restaurants/"


def getData(cuisine, start, size):
    searchURL = URL + '_search?q=' + cuisine + '&from=' + str(start) + '&size=' + str(size)
    print(searchURL)
    try:
        http = urllib3.PoolManager()
        result = http.request('GET', searchURL).data
        data = json.loads(result.decode('utf-8'))
        return data
    except:
        return None


print(getData('chinese', 100, 3))
