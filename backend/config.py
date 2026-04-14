from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent
load_dotenv(env_path / ".env.backend")

URL = os.environ["URL"]
JWT_SECRET = os.environ["JWT_SECRET"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
APP_KEY = os.environ["APP_KEY"]
APP_SECRET = os.environ["APP_SECRET"]
CLOUD_NAME = os.environ["CLOUD_NAME"]
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
JWT_EXPIRY_TIME_SECONDS = 120
CLOUDINARY_EXPIRY_TIME_SECONDS = 120



class Deployment:
    def __init__(self):
        self.env = os.environ["ENV"]
        if self.env not in ["dev", "prod"]:
            raise ValueError("deployment enviroment can be either dev (development) or prod (production)")
        self.dev_allow_origins = ["*"]
        self.prod_allow_origins = ["https://xuzu.in", "https://www.xuzu.in"]

        self.dev_allow_methods = ["*"]
        self.prod_allow_methods = ["GET", "POST"]

        self.dev_allow_headers = ["*"]
        self.prod_allow_headers = ["*"]

        self.allow_origins = self.dev_allow_origins if self.env == "dev" else self.prod_allow_origins
        self.allow_methods = self.dev_allow_methods if self.env == "dev" else self.prod_allow_methods
        self.allow_headers = self.dev_allow_headers if self.env == "dev" else self.prod_allow_headers

        self.debug_mode = True if self.env == "dev" else False
        self.docs_url = "/docs" if self.env == "dev" else None
        self.redoc_url = "/redoc" if self.env == "dev" else None


deployConfigs = Deployment()