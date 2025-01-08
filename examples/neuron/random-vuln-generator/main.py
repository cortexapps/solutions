from cortex_neuron.handler import cortex_scheduled
from cortex_neuron.neuron_client import NeuronClient
import json
import random


@cortex_scheduled(interval="1000s", run_now=True)
def my_handler(context):
    context.log("Success! Handler called!")
    # API endpoints
    catalog_path = "/api/v1/catalog?types=service"
    #fetch only services
    response = context.cortex_api_call(
                method="GET",
                path=catalog_path
                
            ) 
    j_response = json.loads(response.body)
    entities = j_response["entities"]
    # for each service get the tag so we can send it custom data
    for entity in entities:
        tye = entity["type"]
        print(tye)
        tag = entity["tag"]
        print("Processing " + tag)
        custom_data_path = f"/api/v1/catalog/{tag}/custom-data"
        cd_body = {
        "key": "sonarqube-data",
        "value": {
            "vulnerabilities": {
                "high": random.randint(1, 10),
                "medium": random.randint(1, 10),
                "low": random.randint(1, 10)
            },
            "code_coverage": random.randint(10, 100)
            }
        }
        json_body = json.dumps(cd_body)
        cd_response = context.cortex_api_call(
                method="POST",
                path=custom_data_path,
                body=json_body
                

            )
        print(response.status_code)


def run():
    print("Starting random-vuln-data")
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
