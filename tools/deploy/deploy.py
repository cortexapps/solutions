# Simple python script to add a Deploy event to a Service in Cortex

import sys, getopt 
import argparse
import requests
import os
import json
from datetime import datetime




# The following are paremeters that are passed with the command
# deployer.py -sha <Commit SHA> -tag <cortex tag> -type <DEPLOY|> -env <environment> -status <status> -status_msg <status message> -deployer_name <Deployer> - deployer_email <deployer_email>

  # commit_sha      -s
  # cortex_tag      -g
  # cortex_token    -k
  # type            -t 
  # env             -e
  # status          -u
  # status_msg      -m
  # deployer        -d
  # deployer_email  -l 
  # help            -h    
  
#Let's define the variables

commit_sha = ''      
cortex_tag = ''      
deploy_type = ''
env = ''
status = ''
status_msg = ''
deployer  = ''
deployer_email = ''
api_url = ''
api_token = ''
# the timestamp needs to be in the ISO format (i.e. "2019-08-24T14:15:22Z"), Python for some reason does not provide the Z at the end so...
time_stamp= datetime.now().replace(microsecond=0).isoformat() + 'Z'
json_body = ''
  
argParser = argparse.ArgumentParser()
argParser.add_argument("-k","--api_token", required=True, help='The Cortex API token')
argParser.add_argument("-s","--commit_sha", required=True, help='The Cortex tag, i.e., the x-cortex-tag: value in the Cortex.yaml file')
argParser.add_argument("-g","--cortex_tag", required=True, help='')
argParser.add_argument("-t","--type", required=True, help='')
argParser.add_argument("-e","--env", required=True, help='')
argParser.add_argument("-u","--status", required=True, help='')
argParser.add_argument("-m","--status_msg", required=True, help='')
argParser.add_argument("-d","--deployer", required=True, help='')
argParser.add_argument("-l","--deployer_email", required=True, help='')

args = argParser.parse_args()
commit_sha = args.commit_sha
cortex_tag = args.cortex_tag
deploy_type = args.type
env = args.env
status = args.status
status_msg = args.status_msg
deployer  = args.deployer
deployer_email = args.deployer_email
api_token = args.api_token

#Now that we have captured all the parameters, let's put our REST call together
#First we are going to see if we have all the required options
api_url = 'https://api.getcortexapp.com/api/v1/catalog/' + cortex_tag + '/deploys'
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
    "customData": {
      "Status": status,
      "status message": status_msg
    }
  }
response = requests.post(api_url, json=json_body, headers=headers)
