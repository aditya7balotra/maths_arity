import os, json, shutil
from config import *
from assets_pipeline.cloud_service.envConfig import ASSETS_METADATA_PATH
from .logger import logger
from utils import get_cores_meta, get_v_refs

class MetaDataHandler:
    def __init__(self, assets_path):
        self.assets_path = assets_path


    def calculate_metadata(self, discipline: str) -> dict:
        discipline_metadata = {}       # metadata to store for discipline
        
        # get the semester and the cores id
        data = get_cores_meta(assets_path= self.assets_path, discipline= discipline)

        for sem in data.keys():
            # loop over the core
            for core_id in data[sem].keys():
                total_notes = 0
                total_pyqs = 0
                total_v_refs = 0
                pyqs = []
                
                if os.path.exists(os.path.join(self.assets_path, discipline, sem, core_id)):
                    total_notes = len(os.listdir(os.path.join(self.assets_path ,discipline, sem, core_id, "notes")))
                    pyqs = os.listdir(os.path.join(self.assets_path, discipline, sem, core_id, "pyqs"))
                    pyqs = [pyq.removesuffix(".pdf") for pyq in pyqs]
                    total_pyqs = len(pyqs)
                    
                    total_v_refs = len(get_v_refs(assets_path= self.assets_path, discipline= discipline, sem= sem, core_id= core_id))

                    discipline_metadata[core_id] = {
                        "counts": {
                            "total_notes": total_notes,
                            "total_pyqs": total_pyqs,
                            "total_v_refs": total_v_refs
                            },
                        "pyqs_yrs": pyqs
                    }
                    logger.info(f"METADATA: {discipline} {sem} {core_id} ✅")
                else:
                    discipline_metadata[core_id] = {
                        "counts":{
                            "total_notes": total_notes,
                            "total_pyqs": total_pyqs,
                            "total_v_refs": total_v_refs
                        },
                        "pyqs_yrs": pyqs
                    }
        return discipline_metadata


    def generate_v_refs(self, discipline: str) -> dict:
        data = {}
        try:
            sems = os.listdir(os.path.join(self.assets_path, discipline))
            for sem in sems:
                if sem not in [
                    CORES_FILE_NAME,
                    DISCIPLINE_EXTERNAL_LINKS_FILE_NAME,
                    SYLLABUS_UNIT_FILE_NAME
                ]:
                    cores = os.listdir(os.path.join(self.assets_path, discipline, sem))
                    for core in cores:
                        if core != SYLLABUS_FILE_NAME:
                            with open(os.path.join(self.assets_path, discipline, sem, core, VIDEO_REF_FLE_NAME), "r") as file:
                                core_v_ref_data = json.load(file)
                            data[core] = core_v_ref_data
        except Exception as e:
            logger.critical(f"{e}")
            raise e
        # print(data)
        return data
        


    def create_assets_meta(self):
        # ensure the root assets metadata folder
        if os.path.exists(ASSETS_METADATA_PATH):
            logger.info("assets folder found, deleting")
            shutil.rmtree(ASSETS_METADATA_PATH)
        
        os.makedirs(ASSETS_METADATA_PATH)
        logger.info("assets metadata folder created")

        # to copy metadata file names
        meta_files = [
            CORES_FILE_NAME,
            SYLLABUS_UNIT_FILE_NAME,
            DISCIPLINE_EXTERNAL_LINKS_FILE_NAME
        ]

        # get the list of disciplines
        disciplines = os.listdir(self.assets_path)
        for discipline in disciplines:
            # ensure the sub disciplines folder inside
            os.makedirs(os.path.join(ASSETS_METADATA_PATH, discipline))
            try:
                for file in meta_files:
                    shutil.copy2(
                        os.path.join(self.assets_path, discipline, file),
                        os.path.join(ASSETS_METADATA_PATH, discipline, file)
                        )
                
                # get and save count metadata like pyq yrs, counts, etc
                meta_counts = self.calculate_metadata(discipline= discipline)
                with open(os.path.join(ASSETS_METADATA_PATH, discipline, AUTO_GENERATED_METADATA_FILE_NAME), "w") as file:
                    json.dump(meta_counts, file, indent= 4)
                
                v_refs_data = self.generate_v_refs(discipline= discipline)
                with open(os.path.join(ASSETS_METADATA_PATH, discipline, VIDEO_REF_FLE_NAME), "w") as file:
                    json.dump(v_refs_data, file, indent= 4)

            except Exception as e:
                logger.critical(f"{e}")
                raise e