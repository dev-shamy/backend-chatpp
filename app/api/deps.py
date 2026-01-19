from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"

def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
