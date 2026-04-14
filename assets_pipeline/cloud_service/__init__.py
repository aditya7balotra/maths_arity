from ..logger import logger
import os
from config import *
from .envConfig import ASSETS_METADATA_PATH
from .cloudinary_service import CloudinaryService
from .dropbox_service import DropBoxService
import json

class CloudStorageService:
    def __init__(self, assetPath: str):
        self.assets_path = assetPath
        self.cloudinary_service = CloudinaryService(assets_path= assetPath)
        self.dropbox_service = DropBoxService(asset_path= assetPath)
        

    def traverse_upload_asset_get_urls_and_save_assets_meta(self):
        data = self.traverse_upload_asset_and_get_urls()
        
        logger.info("Saving cloud urls")
        for discipline in data.keys():
            if discipline != "syllabus":
                with open(os.path.join(ASSETS_METADATA_PATH, discipline, URL_FILE_NAME), "w") as file:
                    json.dump(data[discipline], file, indent= 4)
        logger.info("Cloud urls saved successfully")

    def traverse_upload_asset_and_get_urls(self) -> dict:
        logger.info(f"CloudStorage: Pushing data from {self.assets_path} to the cloud storage")
        #format data {"discipline": {"core id": core_data, ..., "syllabus": {"semester" : "url"}}
        data= {}
        try:
            disciplines = os.listdir(self.assets_path)
            for discipline in disciplines:
                # format discipline_data {"core id ": core_data, "syllabus": {"semester": "url"}}
                discipline_data = {"syllabus": {}}
                
                sems = os.listdir(os.path.join(self.assets_path, discipline))
                
                for sem in sems:
                    if sem not in [
                        CORES_FILE_NAME,
                        SYLLABUS_UNIT_FILE_NAME,
                        DISCIPLINE_EXTERNAL_LINKS_FILE_NAME
                    ]:
                        cores = os.listdir(os.path.join(self.assets_path, discipline, sem))
                        
                        for core in cores:
                            
                            #format core_data {
                            #       "notes": {"unit no": "link to the unit", "unit no": "link ..."},
                            #       "pyqs": {"year": "link", "year": link}
                            # }
                            core_data = {"notes": {}, "pyqs": {}}

                            if core != SYLLABUS_FILE_NAME:
                                # notes
                                notes = os.listdir(os.path.join(self.assets_path, discipline, sem, core, "notes"))
                                for note in notes:
                                    if note.endswith(".pdf"):
                                        path = os.path.join(self.assets_path, discipline, sem, core, "notes", note)
                                        # use dropbox
                                        url = self.dropbox_service.dropbox_upload_and_get_sharable_url(filePath= path,
                                            dropBoxPath= f"/{ASSETS_BASE_PATH}/{discipline}/{sem}/{core}/notes/{note}",
                                            )
                                        core_data["notes"][note.removesuffix(".pdf")] = url
                                        
                                    else:
                                        logger.warning(f"Consider removing non pdf files from {discipline}/{sem}/{core}/notes")

                                #pyqs
                                pyqs = os.listdir(os.path.join(self.assets_path, discipline, sem, core, "pyqs"))
                                for pyq in pyqs:
                                    if pyq.endswith(".pdf"):
                                        # cloudinary
                                        # print(os.path.join(self.assets_path, discipline, sem, core, "pyqs", pyq),)
                                        url = self.cloudinary_service.cloudinary_upload_and_get_sharable_url(
                                            filePath = os.path.join(self.assets_path, discipline, sem, core, "pyqs", pyq),
                                            cloudinaryPath = f"{ASSETS_BASE_PATH}/{discipline}/{sem}/{core}/pyqs"
                                        )
                                        core_data["pyqs"][pyq.removesuffix(".pdf")] = url
                                    else:
                                        logger.warning(f"Consider removing non pdf files from {discipline}/{sem}/{core}/pyqs")
                                        
                                    discipline_data[core] = core_data

                            else:
                                # cloudinary
                                url = self.cloudinary_service.cloudinary_upload_and_get_sharable_url(filePath= os.path.join(self.assets_path, discipline, sem, SYLLABUS_FILE_NAME),
                                    cloudinaryPath= f"{ASSETS_BASE_PATH}/{discipline}/{sem}/{SYLLABUS_FILE_NAME}"
                                    )
    
                                discipline_data["syllabus"][sem] = url

                data[discipline] = discipline_data

        except Exception as e:
            logger.critical(f"{e}")
            raise e
        logger.info("Data pushed to the cloud successfully")
        
        return data