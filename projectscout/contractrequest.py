import requests

response = requests.get('https://www.capology.com/api/v2/soccer/contracts/es/la-liga/2020-2021/')
print(response.json())