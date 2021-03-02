import requests


url = "https://apis.tracker.delivery/carriers/kr.cjlogistics/tracks/359920496655"
response = requests.get(url)

carrier = response.json()['carrier']['name']
# number =
status = response.json()['state']['text']
# desc = response.json()['progresses'][0]['description']
descs = response.json()['progresses']
for d in descs:
    desc = d['description']
    loca = d['location']['name']
    print(desc, loca)


# loca = response.json()['progresses'][0]['location']['name']

# print(carrier, status, desc, loca)

