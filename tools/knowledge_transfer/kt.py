################################################################################################################
#
#  Tool: Knowledge Transfer... a tool by Cortex!
#  Description: Transfer your catalog descriptors from SaaS to Self-Hosted with style!
#  Author: Mike Moore (mike.moore@cortex.io)
#  Last Update: 20 OCT 2020
#
#  Need help or just want someone to talk to? Reach out to us at help@cortex.io!
#
################################################################################################################

from operator import truediv
import requests
import yaml

WRITE_YAMLS = True
TRANSFER_TO_NEW_INSTANCE = True

CORTEX_API_URL = "https://api.getcortexapp.com"
CORTEX_API_KEY = "" # Get from your Cortex SaaS instance

CORTEX_SELF_API_URL = "[[YOUR CORTEX SELF-HOSTED API URL HERE]]" #
CORTEX_SELF_API_KEY = "" # Get from your Cortex Self-Hosted instance

### NO TOUCHY
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