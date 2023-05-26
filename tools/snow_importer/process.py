# read the servicenow CMDB table (should we make it configurable?)
# for each entry create a yaml and upload it

import os
import requests
import yaml
import json

# Set your Cortex API Token as Environment Variable COTEX_API_TOKEN
c_token = os.getenv('CORTEX_API_TOKEN')
# ServiceNow token 64-bit encoded username:password for basic auth
s_token = os.getenv('SNOW_API_TOKEN')
# Update the URLs where different
c_url = "https://api.getcortexapp.com/"
s_url = "https://dev93537.service-now.com/"

# We are going to query the CMDB_appl table but will store it as a variable since this is likely to vary from instance to instance
s_table = 'cmdb_ci_appl'

# The full servicenow URL to send the request - note that we are only retrieving the sys_id, name, and owned_by fields (edit as needed)
service_url= s_url + 'api/now/table/' + s_table + '?sysparm_fields=sys_id%2Cname%2Cowned_by'
# The headers
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic ' + s_token}
#Let's get all the records from ServiceNow
response = requests.get(service_url,headers=headers)
print(response.text)
j_response = json.loads(response.text)
services = j_response['result']
for s in services:
    #let's see if we have an owner
    info = {}
    owners = []
    links = []
    if (s['owned_by'] != ""):
        u_sys_id = s['owned_by']['value']
        #print(u_sys_id)
        #we need the email of the user so we can assign it to the user
        user_url = s_url + '/api/now/table/sys_user?sysparm_query=sys_id%3D' + u_sys_id + '&sysparm_fields=email'
        u_headers = headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic ' + s_token}
        u_resp = requests.get(user_url,headers=u_headers)
        j_resp = json.loads(u_resp.text)
        print(j_resp)
        user_email = j_resp['result'][0]['email']
        owners.append({'type': 'email', 'email': user_email})
        info['x-cortex-owners'] = owners
    else:
        print('no owner found, so will not add ownership to service in Cortex')        
    service_name = s['name']
    info['title'] = service_name
    #let's convert the name to a tag
    s_tag = service_name.replace(' ','-').lower()
    print(s_tag)
    info['x-cortex-tag'] = s_tag
    links.append({'name': 'ServiceNow','type':'ServiceNow Link','url': s_url + 'nav_to.do?uri=cmdb_ci_appl.do?sys_id=' + s['sys_id']})
    info['x-cortex-link'] = links
    
    #Let's make sure the service doesn't already exist
    gs_url = c_url + "api/v1/catalog/" + s_tag + "/openapi?yaml=true"
    c_headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + c_token
        }
    s_response = requests.get(gs_url, headers=c_headers)
    print(s_response.status_code)
    #If we get 404, means not found so let's add it
    if s_response.status_code == 404:
        #code to add service
        print("Service not found in Cortex, uploading now...")
        u_url = c_url + 'api/v1/open-api'
        u_headers = {'Content-Type': 'application/openapi;charset=UTF-8', 'Authorization': 'Bearer ' + c_token }
        data= yaml.dump({'openapi': '3.0.1', 'info': info})
        u_response = requests.post(u_url, headers=u_headers, data=data)
        if (u_response.status_code == 200):
            print('Succesfully uploaded service')
            #Let's add custom-data to store the servicenow sys_id
            cd_headers = {
                'Authorization': 'Bearer ' + c_token,
                'Content-Type': 'application/json'
                 }
            cd_url = c_url + 'api/v1/catalog/' + s_tag + '/custom-data'
            json_body = {
                "key":"ServiceNow sys_id",
                "value": s['sys_id']
            }     
            cd_resp = requests.post(url=cd_url, json=json_body, headers=cd_headers)
        #print(u_response.text)

    elif s_response.status_code == 200:
        print('service found! Will not update it')
        #TODO code to update service
        #let's get the service yaml and update only the fields that could have changed (owner?)
