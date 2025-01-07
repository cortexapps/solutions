from cortex_neuron.handler import cortex_scheduled
from cortex_neuron.neuron_client import NeuronClient


@cortex_scheduled(interval="1s", run_now=True)
def my_handler(context):
    context.log("Success! Handler called!")


def run():
    print("Starting {{.ProjectName}}")
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
