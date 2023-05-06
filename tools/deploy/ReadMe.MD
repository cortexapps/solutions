## Deployer App

Basic Python 3 application that uses the `requests` library to send a REST call using the [Cortex API](https://docs.cortex.io/docs/api/save-deploy) to add a Deploy event to a service.

![Deploy Event](img/deploy-event.png)

The [test.md](test.md) file provides a test command to run a test locally.

A Dockerfile is also included for your convenience so you don't have to worry about setting up Python and dependencies.

## Usage

```bash

usage: 

deploy.py [-h] -k API_TOKEN -s COMMIT_SHA -g CORTEX_TAG -t TYPE -e ENV
                 -d DEPLOYER -l DEPLOYER_EMAIL -c CUSTOM_DATA
or

docker run deployer:latest [-h] -k API_TOKEN -s COMMIT_SHA -g CORTEX_TAG -t TYPE -e ENV
                 -d DEPLOYER -l DEPLOYER_EMAIL -c CUSTOM_DATA
```

For the 'custom data' option you must provide a key value pair in json format, noting that it does not support multi level json. 

Here is an example command (cortex tag and API token are set as environment variables):

```shell
python3 deploy.py -k $CORTEX_TOKEN -s 1234 -t DEPLOY -e Prod -c '{"cluster": "Prod"}' -d deploy-person -l deploy.person@example.com  -g $CORTEX_TAG
```

If you want to be more specific on the type of custom data that should be provided, you can modify the script to fit your needs. As an example, the script in the 'opinionated-example' folder there is a version of the script that instead of custom data, it takes "Status" and "Status Message".


## Integrating with CD tools

Most CD tools provide a way to run a container. Each one may have different ways to pass the arguments, especially when using dynamic values (i.e., sha, tokens, etc... ). Here are some snippets to help you get started using the docker image. Not all deploy tools may support running a container as a step in the pipeline, so in that case using the Python script may be a better option.

### Jenkinsfile

In this example, we have added Jenkins [credentials](https://www.jenkins.io/doc/book/using/using-credentials/) to store information like the Cortex API token and Cortex tag. In the example below we pass the Jenkins build number as part of the custom meta-data:

```shell
pipeline {
    agent any
    environment {
        CORTEX_TAG    = credentials('CORTEX_TAG')
        CORTEX_API = credentials('CORTEX_API')
    }
    stages {
        stage('trying') { 
            steps {
                sh "docker run cremerfc/deployer:0.1 -k $CORTEX_API -s 1234 -t DEPLOY -e Prod -c '{\"cluster\": \"Prod\", \"Jenkins Job\": $BUILD_NUMBER }' -d deploy-person -l deploy.person@example.com -g $CORTEX_TAG" 
            }
        }
    }
}

```
Note that for the above example you will need to have Docker installed and running wherever the job executes.

## GitHub Actions

Here is an sample GitHub Action. This example deploys to an EC2 instance and then updates Cortex using the result of the deploy step :

```yaml
name: deploy
on:
  push:
    branches:
      - master

jobs:
  deploy:
    name: Deploy to EC2 on master branch push
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
        run: "docker run cremerfc/deployer:0.1 -k ${{ secrets.CORTEX_API_TOKEN }} -s ${{ github.sha }} -d 'GitHub Actions' -g ${{ secrets.CORTEX_TAG}} -t 'DEPLOY' -e Prod -c '{\"cluster\": \"Prod\" , \"status\": ${{ steps.deploy.outcome }}}' -l email@example.com"


```

## ArgoCD

There are two ways that you can send information to Cortex in Argo CD:
* Webhooks
* Resource Hooks

### Webhooks

[Webhooks](https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/services/webhook/) is probably the prefered way as this allows you to send dynamic data about the sync to Cortex.

Using the example found [here](https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/services/webhook/#examples) you can make some modifications to send information to Cortex. Here is an example of what your `argocd-notifications-cm' ConfigMap may look like:

```yaml

apiVersion: v1
kind: ConfigMap
data:
  context: |
    argocdUrl: http://localhost:8080 
  service.webhook.cortex-webhook: |
    url: https://api.getcortexapp.com
    headers:
    - name: Content-Type
      value: application/json
    - name: Accept
      value: application/json
    - name: Authorization
      value: Bearer $token 
    subscriptions: |
      - recipients:
        - cortex-webhook
        triggers:
        - on-sync-succeeded
  template.app-sync-succeeded: |
    webhook:
      cortex-webhook:
        method: POST
        path: /api/v1/catalog/{{.app.metadata.name}}/deploys 
        body: |
          { "customData": { "Sync Status": "{{.app.status.sync.status}}","Sync Details": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}?operation=true" },
            "environment": "{{.app.spec.destination.name}}",
            "sha": "{{.app.status.operationState.operation.sync.revision}}",
            "timestamp": "{{.app.status.operationState.finishedAt}}",
            "title": "Sync by ArgoCD",
            "type": "DEPLOY"
          }
  trigger.on-sync-succeeded: |
    - send:
      - app-sync-succeeded
      when: app.status.operationState.phase in ['Succeeded']
        

```

Please note the following on the ConfigMap above:
* The ArgoCD URL in the `context` section needs to be changed to your ArgoCD URL. This only works if you have used `kubectl port-forward` to access your instance.
* The token variable ($token) is getting the value from the `argocd-notifications-secret` secret. You can either put your Cortex API Key in the ConfigMap, or in the Secret and reference it in the ConfigMap using the field name in the Secret.
* The `path` will only work if your service tag in Cortex matches the app name in ArgoCD. If it does not, then you may be able to use the `if` statements in the examples to set the path based on the application name.
* The `environment` field is set to the destination cluster name. Check your Application Manifest in ArgoCD to see how the Destination is set. You can either use the cluster url or the name in the ArgoCD spec.

### Resource Hooks

ArgoCD has [Resource Hooks](https://argo-cd.readthedocs.io/en/stable/user-guide/resource_hooks/#resource-hooks), which allow you to run a Kubernetes job, pod or other Kubernetes kinds. In the example below, a Kubernetes Job is run after the Sync to update Cortex. Note that the Cortex Api Token is stored in a k8s secret created manually in the cluster in the same namespace as the app to be synced.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: cortex-notification
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    metadata:
        labels:
          name: cortex-update
    spec:      
      containers:
      - name: cortex-deployer
        image: "cremerfc/deployer:0.1"
        imagePullPolicy: IfNotPresent
        env:
        - name: CORTEX_TOKEN
          valueFrom:
            secretKeyRef:
              name: cortex
              key: CORTEX_TOKEN       
        args:
          - -k 
          - "$(CORTEX_TOKEN)"
          - -s  
          - "1234"
          - -g 
          - "app-direct"
          - -t
          - "DEPLOY"
          - -e
          - "PROD"
          - -d 
          - "ArgoCD"
          - -l 
          - "ops@example.com"
          - -c 
          - '{"cluster": "Prod" , "status": "Success"}'
      restartPolicy: Never         
  backoffLimit: 0 
  
```

The only challenge is that it appears that ArgoCD does not make available any information about the sync to the hook.

## Azure DevOps

Azure DevOps has a conatiner job available, however it does require Node.js to be in the image (it is currently not). Would probably need to modify the image based on https://learn.microsoft.com/en-us/azure/devops/pipelines/process/container-phases?view=azure-devops

## Spinnaker

Spinnaker has a [Run job](https://spinnaker.io/docs/reference/pipeline/stages/#run-job) step in their pipeline. This will require to create a Kubernetes Job manifest, similar to the one found [here](https://docs.liquibase.com/workflows/liquibase-community/using-the-run-job-pipeline-stage-with-spinnaker.html).

However, spinnaker does also have a [webhook](https://spinnaker.io/docs/reference/pipeline/stages/#webhook) that allows you to send a REST call to an external system. In this case, it may be simpler to use this native functionality instead of using the image.
