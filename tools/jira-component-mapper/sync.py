
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

# Iterate through all projects
for project in projects:
    try:
        # Get all components in the project
        components = jira.project_components(project=str(project))
        for item in catalog:
            # For **EVERY** item in the catalog, let's try and create a component (if it doesn't exist!)
            newComponent = item['tag']
            exists = False
            for component in components:
                if component.name == newComponent:
                    exists = True
            if not exists:
                # Component does not exist. Let's create it.
                res = jira.create_component(name=newComponent, project=str(project))
                print("Did not find", res, ". Creating component in", project)
    except:
        next