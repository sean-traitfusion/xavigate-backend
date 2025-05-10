from typing import Optional, List
from storage_service.memory.models import SessionRecord, UserProfile, AlignmentTag, AvatarProfile
from pydantic import BaseModel

class PromptExchange(BaseModel):
    user_prompt: str
    assistant_response: str
    tags: List[str] = []

class SessionState(BaseModel):
    session_id: str
    user_id: Optional[str]
    ax: Optional[float]
    aq: Optional[float]
    quadrant: Optional[str]
    avatar_profile: Optional[AvatarProfile]
    recent_tags: List[AlignmentTag] = []
    history: List[PromptExchange] = []
    goal: Optional[str] = None