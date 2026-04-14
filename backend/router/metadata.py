from fastapi import APIRouter, status
from backend.enums import Discipline, MetaData
from fastapi.exceptions import HTTPException
from backend.helpers import (
    get_metadata
)

metaRouter = APIRouter()


@metaRouter.get("/{discipline}", description= "get metadata", tags= ["metadata"])
def metadata(discipline : Discipline, of: MetaData, core_id : int | None = None):
    if ((of.value == MetaData.counts) or (of.value == MetaData.pyqs) or (of.value == MetaData.units)) and core_id is None:
        raise HTTPException(
            status_code= 400,
            detail= "core_id is required when requesting counts, pyqs and units"
        )
    try:
        return get_metadata(discipline= discipline, of= of, core_id= core_id)
    except KeyError as ke:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "resources for the requested core_id not found")
    