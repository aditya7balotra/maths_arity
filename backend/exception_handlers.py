from fastapi.exceptions import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

def exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code= exception.status_code,
        content={
            "success": False,
            "detail": exception.detail
        }
    )

def rate_limit_handler(request: Request, rateLimitException: RateLimitExceeded):
    return JSONResponse(
        status_code= rateLimitException.status_code,
        content= {
            "success": False,
            "detail": "Too many requests"
        }
    )