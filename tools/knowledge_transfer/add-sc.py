# script to add scorecards from a folder
import os
import requests
import json
import yaml
import io

#Api token and url for destination instance
c_url = 'https://api.getcortexapp.com/'
c_token = os.getenv('CORTEX_API_TOKEN')

#Before we get started let's make sure API tokens are set
if (c_token is None):
    print("Api Token must be set")
else:    
    #Let's open the 'yamls' directory and look for scorecards
    for filename in os.listdir('yamls'):
        full_path = os.path.join('yamls', filename)
        print("Processing file " + full_path)
        with open(full_path, 'r') as stream:
            sc_file = yaml.safe_load(stream)
            #for some reason the above loads it as JSON so we need to transform it to yml
            sc_yaml = yaml.dump(sc_file)
            #print("The Contents of " + full_path + " are " + sc_yaml)
            #Now we can upload the scorecard to the destination instance
            u_url = c_url + 'api/v1/scorecards/descriptor'
            u_headers = {
                    'Content-Type': 'application/yaml;charset=UTF-8',
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + c_token
                }
            u_response = requests.post(u_url, headers=u_headers, data=sc_yaml)
            print(u_response.text)        
        
