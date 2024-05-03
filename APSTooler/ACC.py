"""
## Disclaimer

The [Your Python Toolkit Name] ("the toolkit") is provided without any warranties. Its use is at your own risk, and the creator accepts no liability for any damages arising from its use. The toolkit is for informational purposes only and should not be considered professional advice. By using the toolkit, you agree to indemnify the creator against any claims or damages. If you do not agree, please refrain from using the toolkit.

## Documentation

The code is  interface for interacting with the Autodesk Construction Cloud (ACC) API. It includes methods for retrieving information about hubs, projects, folders, and models within a BIM 360 project. Here's a breakdown of its functionality:

Initialization: The class constructor initializes the API token and base URL for ACC API endpoints.
Get Hubs: Retrieves information about hubs, returning the ID and name of the first hub found.
Get Project Details: Fetches details about a specific project within a hub, including its ID and name.
Get Root Folder ID: Obtains the root folder ID for a project, typically named "Project Files".
Get Folder Details: Retrieves details about a specific folder within the project, including its name, ID, version, and description.
Get All Model Details: Retrieves details about all models within the project, including their names, descriptions, and custom attributes like status, revision status, major revision, and MCHW series.
The class uses HTTP requests (GET and POST) to communicate with the ACC API, and it handles authentication using an authentication module named Auth. The code is organized into private methods prefixed with underscores for internal use and public methods for external access. Overall, it provides a convenient abstraction for interacting with ACC API endpoints related to BIM 360 projects.
"""

import requests
from .Auth import Auth

class ACC:

    def __init__(self, token = None):
        self.token = token or Auth.auth2leg()
        self.host = "https://developer.api.autodesk.com"
        self.headers = {'Authorization': f'Bearer {self.token.access_token}'}
    
    def _get(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["data"]
    
    def _post(self, url, data):
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_hubs(self):
        url = f"{self.host}/project/v1/hubs"
        hubs_data = self._get(url)
        hub = hubs_data[0] 
        return hub["id"], hub["attributes"]["name"]
    
    def get_project_details(self, project_name = "UK-Roads-TestProject"):
        hub_id, _ = self.get_hubs() 
        url = f"{self.host}/project/v1/hubs/{hub_id}/projects"
        data = self._get(url)
        project = next(
            (p for p in data 
             if p["attributes"]["name"]== project_name),
            None
            )
        if project is None:
            raise ValueError ("The project does not exist")
        return hub_id, project['id'], project['attributes']['name']
    
    def get_root_folder_id(self): #we expect only one response from  get project details
        hub_id, project_id, _ = self.get_project_details()
        url = f"{self.host}/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()       
        data = response.json()['data']
        for root_folder in data:
            if root_folder['attributes']['displayName'] == 'Project Files' :
                return project_id, root_folder['id']            
        raise ValueError("Error getting folder ID")
    
    def get_folder_details(self, folder_name):
        project_id, root_folder_id = self.get_root_folder_id()
        url = f"{self.host}/data/v1/projects/{project_id}/folders/{root_folder_id}/contents"
        data = self._get(url)
        item_details = []
        for item in data:
            if item['type'] == 'folders':
                if item['attributes']['name'] == folder_name:
                    item_att = item['attributes'].get('extension', {})
                    version = item_att.get('version', None)
                    description = item_att.get('data', {}).get('description', None)
                    item_details.append({
                    'name': item['attributes']['displayName'], 
                    'id': item['id'], 
                    'version': version, 
                    'description': description            
                    })
                    return item_details
                else:
                    return self._get_folder_details(project_id, root_folder_id, folder_name)
    
    def _get_folder_details(self, project_id, root_folder_id, folder_name):
        url = f"{self.host}/data/v1/projects/{project_id}/folders/{root_folder_id}/contents"
        data = self._get(url)
        folder_details = []
        
        for folder in data:
            if folder['type'] == 'folders':
                if folder['attributes']['name'] == folder_name:
                    folder_att = folder['attributes'].get('extension', {})
                    version = folder_att.get('version', None)
                    description = folder_att.get('data', {}).get('description', None)
                    folder_details.append({
                        'name': folder['attributes']['displayName'], 
                        'id': folder['id'], 
                        'version': version, 
                        'description': description            
                    })
                    break
                else:
                    subfolder_models = self._get_folder_details(project_id, folder['id'], folder_name)
                    folder_details.extend(subfolder_models)
        
        return folder_details
 

    def get_all_model_details(self, model_name = None):
        project_id, root_folder_id = self.get_root_folder_id() #gets project id
        model_desc = self._get_model_desc(project_id, root_folder_id, model_name) ### write code to get the details
        model_details = self._get_model_details(project_id, model_desc)
        return model_details
    
    def _get_model_desc(self, project_id, folder_id, model_name):
        url = f"{self.host}/data/v1/projects/{project_id}/folders/{folder_id}/contents"
        data = self._get(url)
        model_details = []
        for item in data:
            if item['type'] == 'folders':
                model_details.extend(self._get_model_desc(project_id, item['id'], model_name))
            elif model_name is None or item['attributes']['name'] == model_name:
                model_attributes = item['attributes'].get('extension', {})
                version = model_attributes.get('version', None)
                description = model_attributes.get('data', {}).get('description', None)
                model_details.append((item['id'], item['attributes']['displayName'], version, description))
                if model_name:
                    break
        return model_details
    
    def _get_model_details(self, project_id, model_desc):
        url = f"{self.host}/bim360/docs/v1/projects/{project_id}/versions:batch-get"
        data = {"urns": [item[0] for item in model_desc]}
        results = self._post(url, data)["results"]
        model_details = []

        for i, result in enumerate(results):
            model_attributes = {attr['name']: attr['value'] for attr in result.get('customAttributes', [])}
            formatted_result = {
                'itemUrn': result.get('itemUrn', ''),
                'name': result.get('name', ''),
                'title': result.get('title', ''),
                'description': model_desc[i][3],
                'Status': model_attributes.get('Status', ''),
                'Revision Status': model_attributes.get('Revision Status', ''),
                'Major Revision': model_attributes.get('Major revision', ''),
                'MCHW Series': model_attributes.get('MCHW Series', '')
            }
            model_details.append(formatted_result)

        return model_details



