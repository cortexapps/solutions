import requests

api_token = '<your-api-token-goes-here>'

caller_tag = 'api-created-svc'
callee_tag = 'my-kafka-api'

api_url = 'https://api.getcortexapp.com/api/v1/catalog/' + caller_tag + '/dependencies/' + callee_tag
headers = {
      'Authorization': 'Bearer ' + api_token,
      'Content-Type': 'application/json'
      }

json_body = {

    "description": "This is a dependency created by the API",
    "metadata": {
        "tags": ["tier1", "external"]
     }


}

resp = requests.post(url=api_url, json=json_body, headers=headers)
print(resp)
print(resp.text)
