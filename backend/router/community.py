from fastapi import APIRouter
from backend.helpers import get_community_platforms

communityRouter = APIRouter()

@communityRouter.get("/", description= "get community platform links", tags= ["community"])
def community_platforms():
    return get_community_platforms()
