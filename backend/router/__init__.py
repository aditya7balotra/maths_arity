from fastapi import APIRouter
from .auth import authRouter
from .community import communityRouter
from .metadata import metaRouter
from .resources import resourceRouter
from .review import reviewRouter


router = APIRouter()

router.include_router(authRouter, prefix= "/auth")
router.include_router(communityRouter, prefix= "/community")
router.include_router(metaRouter, prefix= "/metadata")
router.include_router(resourceRouter, prefix= "/resource")
router.include_router(reviewRouter, prefix= "/review")