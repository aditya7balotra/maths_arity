import dropbox
from dropbox.files import WriteMode
from .envConfig import *
from ..logger import logger


class DropBoxService:
    def __init__(self, asset_path: str):
        self.asset_path = asset_path
        self._ACCESS_TOKEN= DROPBOX_TOKEN
        self.dbx = dropbox.Dropbox(self._ACCESS_TOKEN)
        
        try:
            logger.info("Initializing dropbox")
            self.dbx.users_get_current_account()
            logger.info("Connected successfully to dropbox")
        except Exception as e:
            logger.critical(f"Cannot connect to dropbox. {e}")
    

    def dropbox_upload(self, filePath: str, dropBoxPath: str) -> None:
        logger.info(f"Dropbox: Uploading {filePath}")
        with open(filePath, "rb") as file:
            self.dbx.files_upload(file.read(), dropBoxPath, mode=WriteMode("overwrite"))
        logger.info(f"Dropbox: Uploaded {filePath}")

    def dropbox_get_sharable_url(self, dropBoxPath: str) -> str:
        links = self.dbx.sharing_list_shared_links(path= dropBoxPath)
        if links.links:
            url = links.links[0].url
        else:
            link = self.dbx.sharing_create_shared_link_with_settings(dropBoxPath)
            url = link.url

        url = url.replace("dl=0", "raw=1")
        return url
    
    def dropbox_upload_and_get_sharable_url(self, filePath: str, dropBoxPath: str) -> str:
        self.dropbox_upload(filePath= filePath, dropBoxPath= dropBoxPath)
        url = self.dropbox_get_sharable_url(dropBoxPath= dropBoxPath)
        return url