import requests
import json
import yaml

# Replace these values with your Gerrit server details
GERRIT_URL = "http://your-gerrit-server.com"
GERRIT_USERNAME = "your-username"
GERRIT_PASSWORD = "your-password"

# Cortex API details
CORTEX_API_URL = "https://api.getcortexapp.com/api/v1/open-api"
CORTEX_API_KEY = "your-cortex-api-key"

def fetch_project_info():
    print("Fetching project info from Gerrit...")
    # Authenticate with Gerrit
    auth = (GERRIT_USERNAME, GERRIT_PASSWORD)

    # Fetch list of projects from Gerrit
    projects_url = f"{GERRIT_URL}/a/projects/?d"
    response = requests.get(projects_url, auth=auth)

    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to fetch projects: {response.status_code}")
        print(response.text)  # Print the error message from the response
        return None

    # Print the raw response text for debugging
    print("Successfully fetched project info.")
    return response.text

def generate_yaml(project_name, project_url):
    print(f"Generating YAML for project: {project_name}")
    entity = {
        'openapi': '3.0.1',
        'info': {
            'title': project_name,
            'description': project_name,
            'x-cortex-git': {
                'github': {
                    'repository': f"gitiles/{project_name}"
                }
            },
            'x-cortex-tag': project_name,
            'x-cortex-type': 'service',
            'x-cortex-custom-metadata': {
                'Gerrit': True
            }
        },
        'repository': project_url
    }
    return yaml.dump(entity, sort_keys=False)

def send_to_cortex(yaml_content):
    print("Sending YAML to Cortex...")
    headers = {
        'Content-Type': 'APPLICATION/OPENAPI;CHARSET=UTF-8',
        'Authorization': f'Bearer {CORTEX_API_KEY}'
    }
    response = requests.post(CORTEX_API_URL, headers=headers, data=yaml_content)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    if response.status_code == 200:
        print("Successfully created catalog entity in Cortex.")
    else:
        print(f"Failed to create catalog entity: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    project_info = fetch_project_info()
    if project_info:
        # Handle XSSI protection
        if project_info.startswith(")]}'"):
            project_info = project_info[4:].strip()

        projects_info = json.loads(project_info)
        for project_name, project_info in projects_info.items():
            # Skip projects named "All-Projects" and "All-Users"
            if project_name in ["All-Projects", "All-Users"]:
                continue
            if "web_links" in project_info:
                project_url = project_info["web_links"][0]["url"]
                yaml_content = generate_yaml(project_name, project_url)
                send_to_cortex(yaml_content)
            else:
                print(f"Project Name: {project_name}, URL: Not available")