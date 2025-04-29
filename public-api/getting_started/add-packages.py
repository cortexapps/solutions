import requests

cortex_tag = 'api-created-svc'
api_token = ''<your-api-token-goes-here>''
api_url = 'https://api.getcortexapp.com/api/v1/catalog/' + cortex_tag + '/packages/python/requirements'
headers = {
      'Authorization': 'Bearer ' + api_token,
      'Content-Type': 'application/json'
      }
json_body = ''
with open('requirements.txt') as f:
    body = f.read()
    resp = requests.post(url=api_url, data=body, headers=headers)
    print(resp)
    print(resp.text)






