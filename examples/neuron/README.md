# Overview

This folder includes examples in Python that you can copy and past into your `main.py` file.

# How to use these examples

Initialize a new project using the docker image

`docker run -v "$pwd:/src" ghcr.io/cortexapps/cortex-neuron-agent:latest init --language python --name my-project-name`

replace the contents of the `main.py` file with the context of the example file.

Replace the requirements.txt file if one included in a folder with the python file.