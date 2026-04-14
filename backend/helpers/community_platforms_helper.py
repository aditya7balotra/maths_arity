import json
from config import COMMUNITY_PLATFORM_FILE_NAME

def get_community_platforms():
    with open(COMMUNITY_PLATFORM_FILE_NAME, "r") as file:
        return json.load(file)