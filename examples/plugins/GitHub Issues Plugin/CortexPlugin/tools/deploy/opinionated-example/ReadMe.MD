## Deployer App

Basic Python 3 application that uses the `requests` library to send a REST call using the Cortex API to add a Deploy event to a service.

![Deploy Event](img/deploy-event.png)

The [test.md](test.md) file provides a test command to run a test locally.

A Dockerfile is also included for your convenience so you don't have to worry about setting up Python and dependencies.

## Usage

```bash

usage: 

deploy.py [-h] -k API_TOKEN -s COMMIT_SHA -g CORTEX_TAG -t TYPE -e ENV
                 -u STATUS -m STATUS_MSG -d DEPLOYER -l DEPLOYER_EMAIL
or

docker run deployer:latest [-h] -k API_TOKEN -s COMMIT_SHA -g CORTEX_TAG -t TYPE -e ENV
                 -u STATUS -m STATUS_MSG -d DEPLOYER -l DEPLOYER_EMAIL
```

## Integrating with CD tools

Most CD tools provide a way to run a container. Each one may have different ways to pass the arguments, especially when using dynamic values (i.e., sha, tokens, etc... ). Here are some snippets to help you get started using the docker image. Not all deploy tools may support running a container as a step in the pipeline, so in that case using the Python script may be a better option.

### Jenkinsfile

In this example, we have added Jenkins [credentials](https://www.jenkins.io/doc/book/using/using-credentials/) to store information like the Cortex API token and Cortex tag.

```shell
pipeline {
  environment {

    CORTEX_API_TOKEN= credentials ('cortex-api-token')
    CORTEX_TAG = credentials ('cortex-tag')
  }
  stages {
    stage ('deploying') {
      steps {
        sh '''
        echo "This step is where the app is deployed
        '''
      }
    }
    stage ('dockerization') {
      steps {
        sh '''
       docker run cremerfc/deploy -s ${ env.BUILD_TAG } -g $CORTEX_TAG -k $CORTEX_API_TOKEN -t "DEPLOY"
        '''
      }
    }
  }
}
```

## GitHub Actions

Here is an sample GitHub Action. This example deploys to an EC2 instance and then updates Cortex using the result of the deploy step :

```yaml
name: deploy
on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy to EC2 on main branch push
    runs-on: ubuntu-latest

    steps:
      - name: Checkout the files
        uses: actions/checkout@v2

      - name: Deploy to Server 1
        id: deploy
        uses: easingthemes/ssh-deploy@main
        env:
          SSH_PRIVATE_KEY: ${{ secrets.EC2_SSH_KEY }}
          REMOTE_HOST: ${{ secrets.HOST_DNS }}
          REMOTE_USER: ${{ secrets.USERNAME }}
          TARGET: ${{ secrets.TARGET_DIR }}
      - name: Update Cortex
        run: docker run cremerfc/deploy:0.2 -k ${{ secrets.CORTEX_API_TOKEN }} -s ${{ github.sha }} -d "GitHub Actions" -g ${{ secrets.CORTEX_TAG}} -t "DEPLOY" -e Prod -u ${{ steps.deploy.outcome }} -l email@example.com -m "Trying this"
  


```

## Azure DevOps

Azure DevOps has a conatiner job available, however it does require Node.js to be in the image (it is currently not). Would probably need to modify the image based on https://learn.microsoft.com/en-us/azure/devops/pipelines/process/container-phases?view=azure-devops

## Spinnaker

Spinnaker has a [Run job](https://spinnaker.io/docs/reference/pipeline/stages/#run-job) step in their pipeline. This will require to create a Kubernetes Job manifest, similar to the one found [here](https://docs.liquibase.com/workflows/liquibase-community/using-the-run-job-pipeline-stage-with-spinnaker.html).

However, spinnaker does also have a [webhook](https://spinnaker.io/docs/reference/pipeline/stages/#webhook) that allows you to send a REST call to an external system. In this case, it may be simpler to use this native functionality instead of using the image.
