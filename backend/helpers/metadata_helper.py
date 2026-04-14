from backend.enums import Discipline, MetaData
from config import *
from utils import *
import json
from backend.logs import log

@handle_file_reading_errors
def get_metadata(discipline: Discipline, of: MetaData, core_id : int | None):
    if of.value == MetaData.cores:
        data= provide_cores(discipline_value= discipline.value)
    elif of.value == MetaData.counts:
        data= provide_counts(discipline_value= discipline.value, core_id= str(core_id))
    elif of.value == MetaData.global_links:
        data = provide_external_discipline_global_links(discipline_value= discipline.value)
    elif of.value == MetaData.units:
        data = provide_units(discipline_value= discipline.value, core_id= str(core_id))
    else:
        data= provide_pyq_years(discipline_value= discipline.value, core_id = str(core_id))

    log.info(f"Metadata of {discipline.value} for {of.value} is provided successfully")
    return data

def provide_units(discipline_value: str, core_id : str):
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline_value, SYLLABUS_UNIT_FILE_NAME), "r") as file:
        data = json.load(file)

    if core_id in data.keys():
        return data[core_id]
    
    log.warning(f"Core id {core_id} not found in {SYLLABUS_UNIT_FILE_NAME}. Make sure you have things updated")
    return []
    # raise KeyError(f"core id {core_id} don't exists in {SYLLABUS_UNIT_FILE_NAME}. Make sure you have things updated")

# not used yet in frontend
def provide_external_discipline_global_links(discipline_value: str):
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline_value, DISCIPLINE_EXTERNAL_LINKS_FILE_NAME), "r") as file:
        return json.load(file)

def provide_cores(discipline_value: str):
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline_value, CORES_FILE_NAME)) as file:
        return json.load(file)

# not implemented in frontend
def provide_counts(discipline_value: str, core_id: str):
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline_value, AUTO_GENERATED_METADATA_FILE_NAME), "r") as file:
        data= json.load(file)[core_id]["counts"]

    if core_id in data.keys() and "counts" in data[core_id].keys():
        return data[core_id]["counts"]
    
    log.warning(f"counts not found in {AUTO_GENERATED_METADATA_FILE_NAME} {discipline_value}. Make sure you have things updated")
    return {}


def provide_pyq_years(discipline_value: str, core_id: str):
    with open(os.path.join(ASSETS_METADATA_FOLDER_NAME, discipline_value, AUTO_GENERATED_METADATA_FILE_NAME), "r") as file:
        data= json.load(file)

    if core_id in data.keys() and "pyqs_yrs" in data[core_id].keys():
        return data[core_id]["pyqs_yrs"]
    
    log.warning(f"pyqs not found in {AUTO_GENERATED_METADATA_FILE_NAME} {discipline_value}. Make sure you have things updated")
    return []
    