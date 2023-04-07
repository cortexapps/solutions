import requests
import json
import yaml
from github import Github

# We need a token to talk to Cortex so let's get a token set    
c_token = '<your_cortex_token>'
# Let's get all the entities, shall we?
url = "https://api.getcortexapp.com/api/v1/catalog"
payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + c_token
}

response = requests.request("GET", url, headers=headers, data=payload)

#now that we have a list of our entities in JSON, let's get the tag for each one
#and then get the yaml for each one
#let's get the json response so we can easily find the tag
j_response = response.json()
for entity in j_response['entities']:
    tag = entity['tag']
    #ok, we have the tag, not let's get the yaml for it
    url = "https://api.getcortexapp.com/api/v1/catalog/" + tag + "/openapi?yaml=true"
    payload={}
    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer '+ token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    #now that we have the yaml, let's find the github repo 
    
    data = yaml.safe_load(response.text)
    reponame = ''
    #will use a try/catch to be safe 
    try:
        reponame = data["info"]["x-cortex-git"]["github"]["repository"]
    except( KeyError ):
        print("no github repo found")
    if reponame != '':
        print(reponame) 
        print(data)
        #now let's create a branch, add the file, and create PR
        #set your GH token
        gh_token = '<GitHub Token>'
        #log in
        try:
            api = Github(gh_token)
            #set the repo
            site = api.get_repo(reponame)
            branch_name = "cortex-entity-descriptor-" + tag        
            site.create_git_ref('refs/heads/{branch_name}'.format(**locals()), site.get_branch('main').commit.sha)
            f = open("cortex.yaml", "a")
            f.write(response.text)
            f.close()
            site.create_file( path='cortex.yaml', message='Adding cortex file', content=response.text, branch=branch_name)
            site.create_pull(title="Add cortex yaml",body=(
            "# Description\n\nAdd Cortex.yalm file."
                ),base="main",head=branch_name)
        except
            print("Something went wrong. Make sure your token has access to the repo. If your default branch is master, change the script to main")
