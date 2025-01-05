from cortex_neuron.handler import cortex_scheduled
from cortex_neuron.neuron_client import NeuronClient
from generated import cortex_api_pb2
import os
import sys
import jinja2
from jinja2 import Template
import requests
import json
import yaml
import re



@cortex_scheduled(interval="1s", run_now=True)
def my_handler(context):
    context.log("Success! Handler called!")
    if not (jira_project_key := os.environ.get('JIRA_PROJECT_KEY')):
        print("JIRA_PROJECT_KEY environment varriable not set. Exiting Application...")
        sys.exit()

    if not (jira_api_token := os.environ.get('JIRA_API_TOKEN')):
        print("JIRA_API_TOKEN environment varriable not set. Exiting Application...")
        sys.exit()

    if not (jira_domain := os.environ.get("JIRA_DOMAIN")):     
        print("JIRA_DOMAIN Environment Variable not set. Exiting Application...")
        sys.exit()

    open_api_template = """openapi: 3.0.1
info:
  x-cortex-tag: {{ tag }}
  x-cortex-type: service
  title: {{ title }}
  x-cortex-issues:
    jira:
      components:
      - name: {{ title }}
    """
    jira_api_url = f'https://{jira_domain}.atlassian.net/rest/api/3/project/{jira_project_key}/components'
    headers = {
            'Authorization': f'Basic {jira_api_token}',
            'Accept': 'application/json'
            }
    response = requests.get(jira_api_url,headers=headers)
    if (response.status_code == 200):
        j_response = json.loads(response.text)
        if (len(j_response) > 0):
            for elem in j_response:
                component_name = elem["name"]
                print(f"processing {component_name}...")
                component_tag = tagify(component_name)
                template = Template(open_api_template)
                rendered_yaml = template.render({"tag":component_tag,"title":component_name})
                response = context.cortex_api_call(
                        method="PATCH",
                        path=f"/api/v1/open-api",
                        body=rendered_yaml,
                        content_type="application/openapi;charset=UTF-8"
                        
                    ) 
                print(response.status_code)

        else:
            print("No components found")        
    else:
        print("Something went wrong reaching out to JIRA " + response.status + " - " + response.text)

    
def run():
    print("Starting my-first-agent")
    # Connect to the gRPC server
    client = NeuronClient(
        scope=globals(),
        agent_host="localhost",
        agent_port=50051,
        cortex_host="localhost",
        cortex_port=50051
    )
    client.run()

def tagify(name: str):
    out = re.sub(r"[^a-zA-Z\d]", ' ', name.strip()).lower().strip()
    return re.sub(r'\s+', '-', out)

    

if __name__ == '__main__':
    run()