from fastapi import APIRouter, status, Depends, Request
from backend.enums import Discipline, ResourcesRequestType
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from backend.helpers import provide_requested_resources
from backend.auth.rate_limiter import limiter
from .auth import check_token


resourceRouter = APIRouter()


@resourceRouter.get(
        "/{discipline}/{core_id}/{resource_type}",
          description= "get resources url (notes, pyqs and syllabus) in pdf format and get references in json format",
          tags= ["resources"]
        )
@limiter.limit("10/minute")
def handle_resources_request(
    request: Request,
    core_id: int, 
    discipline: Discipline, 
    resource_type: ResourcesRequestType,
    yr: int | None = None, 
    unit: int | None = None, 
    token= Depends(check_token)
    ):

    if (resource_type.value == ResourcesRequestType.pyqs and yr is None):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "yr query parameter is required when requesting pyqs")
    elif (
        (resource_type.value == ResourcesRequestType.notes or 
         resource_type == ResourcesRequestType.v_ref) and 
        unit is None
        ):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "unit query is required")

    try:
        url = provide_requested_resources(core_id= core_id, discipline= discipline.value, resource_type= resource_type, yr= yr, unit = unit)
        # if (resource_type == ResourcesRequestType.v_ref):
        #     return {
        #         "resource_url": url
        #     }

        # return RedirectResponse(url, status_code = 307)
        return {
            "resource_url": url
        }


    except Exception as e:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Requested resources not found")