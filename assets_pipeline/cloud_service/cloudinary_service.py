import cloudinary
import cloudinary.uploader
from .envConfig import *
from ..logger import logger

class CloudinaryService:
    def __init__(self, assets_path: str):
        self.assets_path = assets_path
        logger.info("Initializing cloudinary")
        cloudinary.config( 
        cloud_name = CLOUD_NAME,
        api_key = API_KEY, 
        api_secret = API_SECRET,
        secure= True
        )
        logger.info("Cloudinary initialized successfully")

    def cloudinary_upload_and_get_sharable_url(self, filePath: str, cloudinaryPath: str) -> str:
        logger.info(f"Cloudinary: Uploading {filePath}")
        upload_data= cloudinary.uploader.upload(
            filePath,
            resource_type="raw",
            folder= cloudinaryPath,
            type= "private"
        )
        return upload_data["public_id"]
