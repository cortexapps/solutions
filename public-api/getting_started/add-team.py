import requests

api_token = '<your-api-token-goes-here>'

api_url = 'https://api.getcortexapp.com/api/v1/teams'
headers = {
      'Authorization': 'Bearer ' + api_token,
      'Content-Type': 'application/json'
      }

json_body = {

    "type": "cortex",
    "teamTag": "cortex-team",
    "metadata": {
        "name": "Cortex Managed Team",
        "description": "Example of Cortex Managed Team created by API",
        "summary": "API created team"
    },
    "links": [],
    "slackChannels": [],
    "additionalMembers": [],
    "cortexTeam": {
        "members": []
    }
}

resp = requests.post(url=api_url, json=json_body, headers=headers)
print(resp)
print(resp.text)
