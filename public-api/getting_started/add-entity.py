import requests

api_token = '<your-api-token-goes-here>'

with open('./service-w-owner.yaml', 'rb') as f:
    data = f.read()

api_url = 'https://api.getcortexapp.com/api/v1/open-api'
headers = {
      'Authorization': 'Bearer ' + api_token,
      'Content-Type': 'application/openapi'
      }


resp = requests.post(url=api_url, data=data, headers=headers)
print(resp)
