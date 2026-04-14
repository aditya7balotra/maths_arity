import jwt
from backend.config import *
from datetime import datetime, timedelta

ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRY_TIME_SECONDS)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str, data: dict):
    decoded= jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    parms= ["ip", "discipline", "core_id", "type"]
    for i in parms:
        if decoded[i] != data[i]:
            print(decoded[i], data[i])
            return False
    
    return True