from operator import truediv
import requests
import yaml

WRITE_YAMLS = True
TRANSFER_TO_NEW_INSTANCE = True

CORTEX_API_URL = "https://api.getcortexapp.com"
CORTEX_API_KEY = "<INSERT ORIGIN API KEY>"


## For self-hosted instances, ensure the backend pods' DNS below is accurate 
CORTEX_SELF_API_URL = "https://api.getcortexapp.com"
CORTEX_SELF_API_KEY = "<INSERT DESTINATION API KEY>"

CATALOG_API_URL = "%s/api/v1/catalog" % CORTEX_API_URL
CATALOG_SELF_API_URL = "%s/api/v1/open-api" % CORTEX_SELF_API_URL

# Retrieve all entities
response = requests.get(CATALOG_API_URL, headers={"Authorization": "Bearer %s" % CORTEX_API_KEY})
list = response.json()
for entity in list['entities']:
    try:
        # Retrieve the OpenAPI spec
        res = requests.get("%s/%s/openapi" % (CATALOG_API_URL, entity['tag']), headers={"Authorization": "Bearer %s" % CORTEX_API_KEY})
        spec = yaml.dump(res.json())

        # Write the spec to the YAMLs folder if enabled.
        if WRITE_YAMLS:
            try:
                ymlFile = open("./yamls/%s.yaml" % entity['tag'], "w")
                ymlFile.write(spec)
                ymlFile.close()
            except:
                print("Could not write spec to YAML file.")

        # Push YAML to new instance if enabled.
        if TRANSFER_TO_NEW_INSTANCE:
            try:
                resp = requests.post("%s" % CATALOG_SELF_API_URL, data=spec, headers={"Authorization": "Bearer %s" % CORTEX_SELF_API_KEY, 'Content-Type': "application/openapi;charset=UTF-8"})
                print(resp.json())
            except:
                print("Could not import service to self-hosted instance.")
        print("Transferred service %s to new instance and saved YAML to ./yamls folder." % entity['tag'])
    except:
        # Something unexpected happened.
        print("[Error]: Unable to import entity - %s" % entity['tag'])
    