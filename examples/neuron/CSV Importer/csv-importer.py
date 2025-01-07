from cortex_neuron.handler import cortex_scheduled
from cortex_neuron.neuron_client import NeuronClient
import os
import sys
import csv
import jinja2
from jinja2 import Template


@cortex_scheduled(interval="1s", run_now=True)
def my_handler(context):
    context.log("Success! Handler called!")
    file_path="entities.csv"
    open_api_template = """openapi: 3.0.1
info:
  x-cortex-tag: {{ tag }}
  x-cortex-type: service
  title: {{ title }}
  x-cortex-git:
    github:
      repository: {{ gh_repo}}
  x-cortex-link:    
  - url: {{ rb_link }}
    name: Runbook
    type: RUNBOOK
  x-cortex-groups:
  - PCI:{{pci}}

    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tag =  row['tag']
            title = row['title']
            gh_repo = row['github']
            rb_link = row['runbook']
            pci = row['PCI']
            template = Template(open_api_template)
            rendered_yaml = template.render({"tag":tag,"title":title,"gh_repo":gh_repo,"rb_link":rb_link,"pci":pci})
            response = context.cortex_api_call(
                method="PATCH",
                path=f"/api/v1/open-api",
                body=rendered_yaml,
                content_type="application/openapi;charset=UTF-8"
                
            ) 
            print(response.status_code)
                
            


def run():
    print("Starting csv-entity-creator")
    # Connect to the gRPC server
    client = NeuronClient(
        scope=globals(),
        agent_host="localhost",
        agent_port=50051,
        cortex_host="localhost",
        cortex_port=50051
    )
    client.run()


if __name__ == '__main__':
    run()
