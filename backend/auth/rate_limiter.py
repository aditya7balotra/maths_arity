from slowapi import Limiter
from fastapi import Request

def limiter_key_func(request: Request):
    token = request.headers.get("Authorization")
    if token:
        return f"{token}:{request.client.host}"
    return request.client.host

limiter = Limiter(key_func= limiter_key_func)
