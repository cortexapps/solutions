import requests

api_token = 'eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAABWLwQrCMAxA_yXnFeKWJu1uHnbwJornEWOFwlgHm6KI_249vsd7H1gfV-ihJYQGtveSKuyPh_FyHk7VWJmmvOYyj_os-aaz_QOlzhg7da1ndnQXcVGSOR-DhBSNPFmds27Q71iYoqCnBtJrqUIwVELk7w_9R3-pfgAAAA.5PYN5rV1ILVHvH5wjBPUK7LrgJJqY7-8pvaTMIMMObAQ7eNM83XjAyK_l5yXIgZlaNcDmxlxG9I9bagFj55JEw'

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