import os
from dotenv import load_dotenv
from pprint import pprint

from cvat_sdk.api_client import Configuration, ApiClient, exceptions


from cvat_sdk.api_client.models import *

# load .env file to environment
load_dotenv()
# Initialize configuration
configuration = Configuration(
    host=os.getenv("CVAT_HOST"),
    username=os.getenv("CVAT_USERNAME"),
    password=os.getenv("CVAT_PASSWORD"),
)

# Get the list of users
print("List of users:")
with ApiClient(configuration) as api_client:
    # Get list of users
    data,response = api_client.users_api.list()
    # Get results
    results = data.get("results")
    # print names of users
    for user in results:
        print(user.get("username"))
    
print("\nList of groups:")
# Get the list of projects
with ApiClient(configuration) as api_client:
    # Get list of projects
    data,response = api_client.projects_api.list()
    # Get results
    results = data.get("results")
    # print names of projects
    for project in results:
        print(project.get("name"))
print("\nList of tasks:")
# Get the list of tasks
with ApiClient(configuration) as api_client:
    # Get list of tasks
    data,response = api_client.tasks_api.list()
    # Get results
    results = data.get("results")
    # print names of tasks
    for task in results:
        print(task.get("name"))
