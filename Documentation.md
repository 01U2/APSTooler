## APSTools ToolKit

## Requirements

This Python package facilitates interaction with Autodesk Platform Services, enabling users to programmatically access hubs, projects, folders, and drawings within Autodesk's ecosystem. This DOCUMENTATION provides a comprehensive guide on how to use the package effectively.

## Installation

To install the package, use pip:

```bash
pip install APSTooler
```

- Clone the repository to your local machine.
- Install the required dependencies by running `pip install -r requirements.txt`.
- Set up your environment variables for authentication.

## Usage

Import the package and instantiate the `ACC` class:

```python
from APSTooler import ACC
```

# Classes and Methods

### ACC Class

The ACC (Autodesk Construction Cloud) class provides methods for interacting with the Autodesk BIM 360 API.

### Authentication

The `Auth` class handles authentication with the Autodesk Construction Cloud API using OAuth 2.0 client credentials flow. It retrieves access tokens required for accessing protected resources.

#### Method

- `auth2leg()`: Performs 2-legged OAuth authentication.

#### Example:

```python
from ACC import Auth

# Initialize Auth object
auth = Auth()

# Perform 2-legged OAuth authentication
token = auth.auth2leg()
```
- `token`: An optional parameter for providing the access token. If not provided, the toolkit will attempt to authenticate using 2-legged OAuth.

### Other functions

- `get_hubs()`: Retrieves information about hubs associated with the authenticated account.
  example
  ```python
  hub_id, hub_name = docs.get_hubs()
  print (f"Hub ID: {hub_id}")
  print (f"Hub Name: {hub_name}")
  ```
- `get_project_details(project_name)`: Retrieves details of a specific project.
    ```python
        project_name = "YOUR_PROJECT_NAME"
        project_info = client.get_project_id(project_name)
        print("Project ID:", project_info[0]['Project ID'])
    ```
- `get_root_folder_id()`: Retrieves the root folder ID of the project, root folder is assumed to be 'project files', which is where the cloud models are stored.

- `get_folder_details(folder_name)`: Retrieves details of a specific folder within the project.

    ```python
        folder_name = "YOUR_FOLDER_NAME"
        folder_details = client.get_folder_details(folder_name)
        if folder_details:
            print("Folder ID:", folder_details[0]['Folder ID'])
            print("Folder Name:", folder_details[0]['Folder Name'])
            print("Project Name:", folder_details[0]['Project Name'])
            print("Project ID:", folder_details[0]['Project ID'])
        else:
            print("Folder not found.")
    ```

- `get_all_model_details(model_name)`: Retrieves details of all models or `model_name` within the project, including custom attributes, and model description.

        ```python
            models = docs.get_all_model_details()
            print models
        ```

### Getting Models Custom attributes

To retrieve all models in the folder and sub folders:

us the `.get_all_drawing_attributes` Method


### Conclusion

This documentation provides a basic overview of how to use the Autodesk Platform Services Python client package. For more detailed information about each method and additional functionalities, please refer to the official Autodesk API documentation.
https://aps.autodesk.com/en/docs/acc