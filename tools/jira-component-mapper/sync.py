
from dotenv import dotenv_values
from jira import JIRA
import requests

# Load .env into environment
config = dotenv_values(".env")

# Connect to JIRA
jira = JIRA(server=config["JIRA_URL"], basic_auth=(config['JIRA_EMAIL'], config['JIRA_TOKEN']))

projects = jira.projects()

# Get all Cortex entitites
c_token = config['CORTEX_API_KEY']
headers = {
            'Content-Type': "application/openapi;charset=UTF-8",
            'Authorization': 'Bearer ' + c_token
        }
response = requests.get(url=config['CORTEX_API_URL'], headers=headers)
catalog = response.json()['entities']

for project in projects:
    try:
        print("Listing components in", project)
        components = jira.project_components(project=str(project))
        for item in catalog:
            newComponent = item['tag']
            exists = False
            for component in components:
                if component.name == newComponent:
                    exists = True
                    print("Found ",newComponent, ". Will not create!")
            if not exists:
                res = jira.create_component(name=newComponent, project=str(project))
                print("Did not find", res, ". Creating component in", project)
    except:
        next