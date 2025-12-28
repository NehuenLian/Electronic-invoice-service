from os import getenv

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
SECRET = getenv("JWT_SECRET_KEY", "default-secret-change-me")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    if credentials.credentials != SECRET:
        raise HTTPException(status_code=401, detail="Invalid JWT")
    return credentials.credentials