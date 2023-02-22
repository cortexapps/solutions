import requests

api_token = 'eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAABWLwQrCMAxA_yXnFeKWJu1uHnbwJornEWOFwlgHm6KI_249vsd7H1gfV-ihJYQGtveSKuyPh_FyHk7VWJmmvOYyj_os-aaz_QOlzhg7da1ndnQXcVGSOR-DhBSNPFmds27Q71iYoqCnBtJrqUIwVELk7w_9R3-pfgAAAA.5PYN5rV1ILVHvH5wjBPUK7LrgJJqY7-8pvaTMIMMObAQ7eNM83XjAyK_l5yXIgZlaNcDmxlxG9I9bagFj55JEw'

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