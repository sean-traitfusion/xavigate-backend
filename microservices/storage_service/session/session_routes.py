# backend/session/session_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from session.flow import handle_reflection

router = APIRouter()

class ReflectionInput(BaseModel):
    user_id: str
    reflection: str

@router.post("/api/session/reflection")
async def reflection_handler(payload: ReflectionInput):
    result = handle_reflection(
        user_id=payload.user_id,
        reflection_text=payload.reflection
    )
    return result
