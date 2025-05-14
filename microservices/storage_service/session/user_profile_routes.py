# backend/session/user_profile_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from memory.storage import load_user_profile, save_user_profile

router = APIRouter()

@router.get("/api/user/{user_id}")
async def get_user_profile(user_id: str):
    profile = load_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile.dict()
    
class UserUpdate(BaseModel):
    name: Optional[str]

@router.put("/api/user/{user_id}")
async def update_user_profile(user_id: str, update: UserUpdate):
    """
    Update mutable fields of the user profile (e.g. name).
    """
    profile = load_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    # Update name if provided
    if update.name is not None:
        profile.name = update.name
    # Persist changes
    save_user_profile(profile)
    return profile.dict()
