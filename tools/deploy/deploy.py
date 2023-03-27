# Simple python script to add a Deploy event to a Service in Cortex

import sys, getopt 
import argparse
import requests
import os
import json
from datetime import datetime




# The following are paremeters that are passed with the command
# deployer.py -sha <Commit SHA> -tag <cortex tag> -type <DEPLOY|> -env <environment> -deployer_name <Deployer> -deployer_email <deployer_email> -c <custom JSON data> -u <instance url>

  # commit_sha      -s
  # custom_data     -c
  # cortex_tag      -g
  # cortex_token    -k
  # type            -t 
  # env             -e
  # deployer        -d
  # deployer_email  -l 
  # help            -h    
  
#Let's define the variables

commit_sha = ''      
cortex_tag = ''      
deploy_type = ''
env = ''
#custom_data = ''
deployer  = ''
deployer_email = ''
api_url = ''
api_token = ''
# the timestamp needs to be in the ISO format (i.e. "2019-08-24T14:15:22Z"), Python for some reason does not provide the Z at the end so...
time_stamp= datetime.now().replace(microsecond=0).isoformat() + 'Z'
json_body = ''
instance_url = ''

# let's do the right thing and catch any errors
  
try:
  argParser = argparse.ArgumentParser()
  argParser.add_argument("-k","--api_token", required=True, help='The Cortex API token')
  argParser.add_argument("-s","--commit_sha", required=True, help='The Cortex tag, i.e., the x-cortex-tag: value in the Cortex.yaml file')
  argParser.add_argument("-g","--cortex_tag", required=True, help='')
  argParser.add_argument("-t","--type", required=True, help='')
  argParser.add_argument("-e","--env", required=True, help='')
  argParser.add_argument("-d","--deployer", required=True, help='')
  argParser.add_argument("-l","--deployer_email", required=True, help='')
  argParser.add_argument("-u","--instance_url", required=False, help='Optional - if you are running on prem provide the URL to your Cortex instance (format should be like https://api.getcortexapp.com)')
  argParser.add_argument("-c","--custom_data", required=True, help='Include your custom medatadata in JSON format, i.e., { "fieldname":"fieldvalue"} ')

  args = argParser.parse_args()
  commit_sha = args.commit_sha
  cortex_tag = args.cortex_tag
  deploy_type = args.type
  env = args.env
  custom_data = args.custom_data
  deployer  = args.deployer
  deployer_email = args.deployer_email
  api_token = args.api_token
  instance_url = args.instance_url

  #Now that we have captured all the parameters, let's put our REST call together
  #First we are going to see if we have all the required options
  if (instance_url is None):
    api_url = 'https://api.getcortexapp.com/api/v1/catalog/' + cortex_tag + '/deploys'
  else:
    api_url = instance_url + '/api/v1/catalog/' + cortex_tag + '/deploys'
  
  headers = {
      'Authorization': 'Bearer ' + api_token,
      'Content-Type': 'application/json'
      }
  json_body = {
      "title": "Deployed by Deployer",
      "timestamp": time_stamp,
      "type": deploy_type,
      "sha": commit_sha,
      "deployer": {
        "name": deployer,
       "email": deployer_email
      },
      "environment": env,
      "customData": json.loads(custom_data)
    }
  
  response = requests.post(api_url, json=json_body, headers=headers)
  print(response)
except Exception as e:
  print(e)
