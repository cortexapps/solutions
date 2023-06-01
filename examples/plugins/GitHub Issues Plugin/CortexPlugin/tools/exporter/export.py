import requests
import yaml

API_KEY = "<<CORTEX_API_KEY>>"

r = requests.get('https://api.getcortexapp.com/api/v1/catalog', headers={'Authorization': 'Bearer '+API_KEY})
entities = r.json()['entities']

for e in entities:
    req = requests.get('https://api.getcortexapp.com/api/v1/catalog/'+e['tag']+'/openapi', headers={'Authorization': 'Bearer '+API_KEY})
    with open('./yamls/'+e['tag']+'.yaml', 'w') as yaml_file:
        yaml.dump(req.json(), yaml_file)
