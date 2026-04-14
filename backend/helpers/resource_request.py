
from backend.enums import ResourcesRequestType
from config import *
import json
from backend.logs import log
from .url_generators import (
    dropbox_get_temp_url,
    cloudinary_get_temp_url
)



def provide_requested_resources(core_id: int, discipline: str, resource_type: ResourcesRequestType, yr: int, unit: int):
    core_id = str(core_id)
    yr = str(yr)
    unit = str(unit)

    if resource_type == ResourcesRequestType.notes:
        data = provide_requested_resources_notes(core_id= core_id, discipline= discipline, unit= unit)
    elif resource_type == ResourcesRequestType.pyqs:
        data = provide_requested_resources_pyqs(core_id= core_id, discipline= discipline, yr= yr)
    elif resource_type == ResourcesRequestType.syllabus:
        data = provide_requested_resources_syllabus(core_id= core_id, discipline = discipline)
    else:
        # case of v_refs
        data = provide_requested_resources_v_refs(discipline= discipline, core_id= core_id, unit= unit)
    return data

def provide_requested_resources_v_refs(discipline: str, core_id: str, unit: str):
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline, VIDEO_REF_FLE_NAME), 'r') as file:
            data: dict= json.load(file)

    if core_id in data.keys() and unit in data[core_id].keys():
        return data[core_id][unit]

    raise KeyError("requested core_id or unit not found")


def provide_requested_resources_notes(core_id: str, discipline: str, unit: str):
    # in dropbox
    semester = None
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline, CORES_FILE_NAME), "r") as file:
        cores = json.load(file)
    for sem in cores.keys():
        if core_id in cores[sem].keys():
            semester = sem
            break
    if semester:
        url= dropbox_get_temp_url(discipline= discipline, sem= semester, core_id= core_id, unit = unit)
        if url:
            return url
    raise Exception("resource not found")

def provide_requested_resources_pyqs(core_id: str, discipline: str, yr: str):
    # cloudinary
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline, URL_FILE_NAME), "r") as file:
        data: dict = json.load(file)
    if core_id in data.keys() and yr in data[core_id]["pyqs"].keys():
        public_id: str= data[core_id]["pyqs"][yr]
        url = cloudinary_get_temp_url(public_id= public_id)

        return url
    
    raise KeyError("requested core_id or yr not found")

def provide_requested_resources_syllabus(core_id: str, discipline: str):
    # cloudianry
    semester = None
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline, CORES_FILE_NAME), "r") as file:
        cores = json.load(file)
    for sem in cores.keys():
        if core_id in cores[sem].keys():
            semester = sem
    if semester:
        with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline, URL_FILE_NAME), "r") as file:
            data: dict = json.load(file)

        if semester in data["syllabus"].keys():
            public_id= data["syllabus"][semester]
            return cloudinary_get_temp_url(public_id= public_id)
    
    raise KeyError("requested syllabus for the core id not found")