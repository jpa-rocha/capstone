import requests
import json
url = 'https://www.capology.com/api/v2/soccer/payrolls/de/1-bundesliga/2020-2021/'
headers = {"x-api-key": "828051bb8fcc41189822a19249477ae5"}
r = requests.get(url, headers=headers)
file = r.json()
with open('file.json', 'w') as f:
    json.dump(file, f,indent="")