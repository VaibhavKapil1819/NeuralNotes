from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from backend.config.firebase import db
from pydantic import BaseModel

security = HTTPBearer()

class CurrentUser(BaseModel):
    uid: str
    email: str
    name: str | None = None

async def get_current_user(res: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    """
    FastAPI dependency to verify the Firebase ID Token from the Authorization header.
    Returns the CurrentUser object if valid, otherwise raises 401.
    """
    token = res.credentials
    try:
        # Verify the ID token using Firebase Admin
        decoded_token = auth.verify_id_token(token)
        
        return CurrentUser(
            uid=decoded_token['uid'],
            email=decoded_token.get('email', ''),
            name=decoded_token.get('name')
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
