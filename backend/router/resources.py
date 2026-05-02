from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.responses import StreamingResponse
from backend.enums import Discipline, ResourcesRequestType
from fastapi.exceptions import HTTPException
from backend.helpers import provide_requested_resources
from backend.auth.rate_limiter import limiter
from .auth import check_token
import requests


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
    mode: str = Query("preview", enum=["preview", "download"]),
    token=Depends(check_token)
):

    # 🔒 Validation
    if (resource_type.value == ResourcesRequestType.pyqs and yr is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="yr query parameter is required when requesting pyqs"
        )

    elif (
        (resource_type == ResourcesRequestType.notes or 
         resource_type == ResourcesRequestType.v_ref) and 
        unit is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unit query is required"
        )

    try:
        url = provide_requested_resources(
            core_id=core_id,
            discipline=discipline.value,
            resource_type=resource_type,
            yr=yr,
            unit=unit
        )

        # 🔥 Stream from external source
        r = requests.get(url, stream=True)

        if r.status_code != 200:
            raise HTTPException(status_code=404, detail="File not accessible")

        # 🎯 Control preview vs download
        filename = f"xuzu_{discipline}_{core_id + unit}"

        if mode == "download":
            content_disposition = f'attachment; filename="{filename}"'
        else:
            content_disposition = f'inline; filename="{filename}"'

        headers = {
            "Content-Disposition": content_disposition
        }

        return StreamingResponse(
            r.iter_content(chunk_size=1024 * 1024),  # 1MB chunks (better)
            media_type=r.headers.get("Content-Type", "application/octet-stream"),
            headers=headers
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested resources not found"
        )