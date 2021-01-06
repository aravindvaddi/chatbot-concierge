import requests
import json

client_id = CLIENT_ID
api_key = API_KEY

url = 'https://api.yelp.com/v3/businesses/search'

headers = {'Authorization' : 'Bearer {}'.format(api_key)}

c = ('chinese', 'japanese', 'tradamerican', 'mexican', 'italian')

bid = set()


def get(cat):
	bus = []
	for i in range(0, 1000, 50):
		if cat == 'japanese' and i >= 950:
			break
		params = {
			'location' : 'New York City',
			'categories' : cat,
			'limit': 50,
			'offset': i}

		res = requests.get(url=url, params=params, headers=headers)
		d = res.json()
		print(d.keys())
		if d.get('error') is not None:
			print(d)
		business = d['businesses']

		for b in business:
			if b['id'] in bid:
				continue
			else:
				bus.append(b)
				bid.add(b['id'])
	return bus


for cat in c:
	data = dict()
	data[cat] = get(cat)
	with open(cat, mode = 'w') as f:
		json.dump(data, f)
