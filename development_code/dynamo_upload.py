import boto3
import json
import datetime


def buildItem(data, cuisine):
    item = {}

    if 'id' in data:
        item['RestaurantID'] = {'S': data['id']}
    if 'name' in data:
        item['name'] = {'S': data['name']}
    if 'rating' in data:
        item['rating'] = {'S': str(data['rating'])}
    if 'coordinates' in data:
        item['location'] = {'SS': [str(data['coordinates']['latitude']), str(data['coordinates']['longitude'])]}
    if 'price' in data:
        item['price'] = {'S': data['price']}
    if 'location' in data and 'display_address' in data['location']:
        item['address'] = {'S': ", ".join(row for row in data['location']['display_address'])}
    if 'phone' in data:
        item['phone'] = {'S': data['phone']}
    item['cuisine'] = {'S': cuisine}
    item['insertedAtTimestamp'] = {'S': str(datetime.datetime.now())}

    return item


dynamodb = boto3.client('dynamodb')

failCount, passCount = 0, 0
for cname in ('chinese', 'italian', 'japanese','mexican', 'tradamerican'):
    with open(cname, 'r') as f:
        data = json.load(f)[cname]

    for i, business in enumerate(data):
        if not business['is_closed']:
            item = buildItem(business, cname)
            if i == 0 or i == 1:
                print(item)
            try:
                dynamodb.put_item(TableName='yelp-restaurants', Item=item)
                passCount += 1
            except Exception as e:
                print("Failed" + str(e))
                failCount += 1
        print("Processed: {} of {}".format(i, cname))

print("Pass Count: ", passCount)
print("Fail Count: ", failCount)
