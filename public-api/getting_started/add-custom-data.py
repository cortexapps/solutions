import requests
from datetime import datetime

cortex_tag = 'api-created-svc'
time_stamp= datetime.now().replace(microsecond=0).isoformat() + 'Z'

api_token = '<your-api-token-goes-here>'

api_url = 'https://api.getcortexapp.com/api/v1/catalog/' + cortex_tag + '/custom-data'
headers = {
      'Authorization': 'Bearer ' + api_token,
      'Content-Type': 'application/json'
      }

json_body = {

    "key": "some-internal-tool",
    "value": {
        "tool": "home-grown build tool",
        "custom scan result": "failed!",
        "details": { "scan-id": "456", "branch" : "main", "timestamp" : time_stamp }
    },
    "description": "Scan data uploaded by REST API"
    }


resp = requests.post(url=api_url, json=json_body, headers=headers)
print(resp)
print(resp.text)
