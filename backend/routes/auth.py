from fastapi import APIRouter, Depends, status
from backend.middleware.auth_middleware import get_current_user, CurrentUser
from backend.config.firebase import db
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_user(user: CurrentUser = Depends(get_current_user)):
    """
    Synchronizes the authenticated user with the Firestore database.
    If the user doesn't exist, it creates a new user document.
    """
    user_ref = db.collection("users").document(user.uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        # Create new user profile in Firestore
        user_data = {
            "uid": user.uid,
            "email": user.email,
            "name": user.name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "meeting_count": 0,
            "is_active": True
        }
        user_ref.set(user_data)
        return {"status": "created", "user": user_data}
    
    return {"status": "synced", "user": user_doc.to_dict()}

@router.get("/me")
async def get_me(user: CurrentUser = Depends(get_current_user)):
    """Returns the current authenticated user profile."""
    return user
