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
with ApiClient(configuration) as api_client:
    # Get list of users
    data,response = api_client.users_api.list()
    pprint(data)

# Get the list of projects
with ApiClient(configuration) as api_client:
    # Get list of projects
    data,response = api_client.projects_api.list()
    pprint(data)
