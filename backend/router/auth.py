from fastapi import APIRouter, Request, Depends, status
from backend.enums import Discipline, ResourcesRequestType
from backend.auth.jwt import create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from backend.auth.jwt import verify_token
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

authRouter = APIRouter()

@authRouter.post("/init", description="get access token", tags= ["auth"])
def init(request: Request, discipline: Discipline, core_id: str, type: ResourcesRequestType):
    return {"token": create_access_token(
        {"ip": request.client.host,
         "discipline": discipline,
         "core_id": core_id,
         "type": type.value}
        )
    }


security = HTTPBearer()


def check_token(request: Request, core_id: int, discipline: Discipline, resource_type: ResourcesRequestType, token: HTTPAuthorizationCredentials = Depends(security)):
    if not token.credentials:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    
    try:
        if not verify_token(token= token.credentials, data = {
            "ip": request.client.host,
            "discipline": discipline,
            "core_id": str(core_id),
            "type": resource_type.value
        }):
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    except (ExpiredSignatureError, InvalidSignatureError):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    
    return None