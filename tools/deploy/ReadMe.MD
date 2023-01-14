## Deployer App

Basic Python 3 application that uses the `requests` library to send a REST call using the Cortex API to add a Deploy event to a service.

![Deploy Event](img/deploy-event.png)

The [test.md](test.md) file provides a test command to run a test locally.

A Dockerfile is also included for your convenience so you don't have to worry about setting up Python and dependencies.

## Usage

```bash

usage: deploy.py [-h] -k API_TOKEN -s COMMIT_SHA -g CORTEX_TAG -t TYPE -e ENV
                 -u STATUS -m STATUS_MSG -d DEPLOYER -l DEPLOYER_EMAIL

```