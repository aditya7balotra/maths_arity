from dotenv import load_dotenv
import os
from pathlib import Path
from config import ASSETS_METADATA_FOLDER_NAME

ASSETS_METADATA_PATH = Path(__file__).resolve().parent.parent.parent / ASSETS_METADATA_FOLDER_NAME
load_dotenv(Path(__file__).resolve().parent / ".env")

CLOUD_NAME = os.environ["cloud_name"]
API_SECRET = os.environ["api_secret"]
API_KEY = os.environ["api_key"]
DROPBOX_TOKEN = os.environ["dropbox_token"]

