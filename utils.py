from backend.enums import Discipline, MetaData
from functools import wraps
# from backend.logs import log
import os, json
from config import *


## -------
# decorator
def handle_file_reading_errors(func):
    @wraps(func)
    def wrapper(discipline: Discipline, of: MetaData, core_id: int | None):
        try:
            return func(discipline, of, core_id)
        except FileNotFoundError as e:
            # log.critical(e)
            raise FileNotFoundError(f"{e}")
        except KeyError as e:
            # log.critical(e)
            raise KeyError(f"{e}")

    return wrapper


#-------


def get_cores_meta(assets_path:str, discipline: str) -> dict:
    try:
        with open(os.path.join(assets_path, discipline, CORES_FILE_NAME), "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        # log.critical(str(e))
        raise FileNotFoundError(e)

def get_v_refs(assets_path: str, discipline: str, sem: str, core_id: str) -> dict:
    try:
        with open(os.path.join(assets_path, discipline, sem,core_id, VIDEO_REF_FLE_NAME), "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        # log.critical(str(e))
        raise FileNotFoundError(e)