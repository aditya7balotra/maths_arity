from fastapi import HTTPException, status
from enum import Enum
from config import *
import os

class Discipline(str, Enum):
    maths = "maths"

class ResourcesRequestType(str, Enum):
    notes = "notes"
    pyqs = "pyqs"
    v_ref = "v_refs"
    syllabus = "syllabus"

    def file_path(self, discipline, sem, resource_type: ResourcesRequestType, core_id, yr: int | None = None, unit: int | None = None):
        if resource_type.value != ResourcesRequestType.syllabus:
            path_map = {
                "notes" : os.path.join("notes", f"{unit}.pdf"),
                "pyqs": os.path.join("pyqs", f"{yr}.pdf"),
                "v_refs": "v_refs.json"
            }
            return os.path.join(ASSETS_BASE_PATH, discipline, sem, core_id , path_map[resource_type.value])
        
        return os.path.join(ASSETS_BASE_PATH, discipline, sem, SYLLABUS_FILE_NAME)
    

class MetaData(str, Enum):
    cores= "cores"
    pyqs = "pyqs"
    counts = "counts"
    global_links = "global_links"
    units= "units"
