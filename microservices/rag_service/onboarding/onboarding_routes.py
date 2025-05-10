# backend/onboarding/onboarding_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Set

# Import all necessary functions
from trait_bundle_loader import get_bundle_by_trait
from agents.onboarding_agent import (
    run_trait_bundle,
    ask_onboarding_question,
    process_onboarding_response,
    evaluate_response,  # Import this specifically
    ONBOARDING_PROMPTS
)

from storage_service.memory.storage import (
    load_user_profile, 
    is_user_unlocked,
    store_trait_confidence,  # Import this specifically
    append_trait_evidence,   # Import this specifically
)

router = APIRouter()

class TraitBundleRequest(BaseModel):
    user_id: str
    trait_name: str
    user_reply: Optional[str] = None  # None on first turn (prelude)
    current_question_index: Optional[int] = None
    asked_questions: Optional[List[str]] = None
    confidence: Optional[float] = None

class TraitBundleResponse(BaseModel):
    next_prompt: str
    confidence: Optional[float] = None
    is_complete: bool = False

# Simple evaluation function in case the import fails
def fallback_evaluate_response(user_response: str, trait_name: str):
    """Fallback function if the imported one fails"""
    import random
    return random.uniform(-0.1, 0.2), f"Fallback evaluation for response to {trait_name}"

# Simple storage functions in case the imports fail
def fallback_store_trait_confidence(user_id: str, trait_name: str, confidence: float):
    """Fallback function if the imported one fails"""
    print(f"[FALLBACK] Storing confidence {confidence} for {trait_name}")

def fallback_append_trait_evidence(user_id: str, trait_name: str, evidence_list: list):
    """Fallback function if the imported one fails"""
    print(f"[FALLBACK] Appending evidence for {trait_name}")

@router.post("/onboarding/trait-bundle", response_model=TraitBundleResponse)
def trait_bundle_step(req: TraitBundleRequest):
    try:
        # Initial request with no reply
        if req.user_reply is None:
            bundle = get_bundle_by_trait(req.trait_name)
            return {"next_prompt": bundle.get("prelude", ""), "confidence": 0.5, "is_complete": False}
        
        # Get bundle data
        bundle = get_bundle_by_trait(req.trait_name)
        questions = bundle["questions"]
        
        # Convert asked_questions list to a set for faster lookups
        asked_questions = set(req.asked_questions or [])
        
        # If this is a response to the prelude, return the first question
        if req.current_question_index is None or req.current_question_index < 0:
            if questions and len(questions) > 0:
                return {"next_prompt": questions[0].get("prompt", ""), "confidence": 0.5, "is_complete": False}
            else:
                return {"next_prompt": "Tell me more about yourself.", "confidence": 0.5, "is_complete": False}
        
        # Evaluate the response if possible
        confidence = req.confidence or 0.5
        
        if req.current_question_index >= 0 and req.current_question_index < len(questions):
            try:
                # Use the evaluation function to get a confidence delta
                current_q = questions[req.current_question_index]
                try:
                    # Try to use the imported function
                    delta, evidence = evaluate_response(req.user_reply, req.trait_name)
                except Exception as e:
                    print(f"⚠️ Error with evaluate_response: {e}")
                    # Fallback to the local function
                    delta, evidence = fallback_evaluate_response(req.user_reply, req.trait_name)
                
                confidence += delta
                
                # Try to record evidence but don't depend on it
                try:
                    try:
                        # Try to use the imported function
                        store_trait_confidence(req.user_id, req.trait_name, confidence)
                    except Exception as e:
                        print(f"⚠️ Error with store_trait_confidence: {e}")
                        # Fallback to the local function
                        fallback_store_trait_confidence(req.user_id, req.trait_name, confidence)
                    
                    try:
                        # Try to use the imported function
                        append_trait_evidence(req.user_id, req.trait_name, [{
                            "question_id": current_q.get("id", f"q{req.current_question_index}"),
                            "prompt": current_q.get("prompt", ""),
                            "response": req.user_reply,
                            "delta": delta,
                            "evidence": evidence
                        }])
                    except Exception as e:
                        print(f"⚠️ Error with append_trait_evidence: {e}")
                        # Fallback to the local function
                        fallback_append_trait_evidence(req.user_id, req.trait_name, [{
                            "question_id": current_q.get("id", f"q{req.current_question_index}"),
                            "prompt": current_q.get("prompt", ""),
                            "response": req.user_reply,
                            "delta": delta,
                            "evidence": evidence
                        }])
                except Exception as e:
                    print(f"⚠️ Failed to store evidence: {e}")
            except Exception as e:
                print(f"⚠️ Evaluation error: {e}")
        
        # Find the next unanswered question
        for i, q in enumerate(questions):
            prompt = q.get("prompt", "")
            if prompt and prompt not in asked_questions and i != req.current_question_index:
                # Found a question we haven't asked yet
                return {
                    "next_prompt": prompt,
                    "confidence": confidence,
                    "is_complete": False
                }
        
        # If we reach here, all questions have been asked or we're over threshold
        try:
            try:
                # Try to use the imported function
                store_trait_confidence(req.user_id, req.trait_name, confidence)
            except Exception as e:
                print(f"⚠️ Error with store_trait_confidence: {e}")
                # Fallback to the local function
                fallback_store_trait_confidence(req.user_id, req.trait_name, confidence)
        except Exception as e:
            print(f"⚠️ Failed to store final confidence: {e}")
            
        return {
            "next_prompt": bundle.get("follow_up_suggestion", "Thank you for sharing these insights."),
            "confidence": confidence,
            "is_complete": True
        }
            
    except Exception as e:
        print(f"⚠️ Error in trait_bundle_step: {e}")
        # Emergency fallback
        return {"next_prompt": "Let's continue our conversation. What resonates with you about this trait?", "is_complete": False}

# Add an endpoint to fetch bundle data:
@router.get("/api/trait-bundle-data")
def get_trait_bundle_data(trait_name: str):
    try:
        bundle = get_bundle_by_trait(trait_name)
        return {"questions": bundle.get("questions", [])}
    except Exception as e:
        print(f"⚠️ Error fetching bundle data: {e}")
        # Return empty questions as fallback
        return {"questions": []}
    
@router.post("/api/onboarding/reset")
def reset_onboarding(user_id: str):
    """
    Reset onboarding progress: clear traits, reset index and lock status.
    """
    from storage_service.memory.storage import load_user_profile, save_user_profile
    profile = load_user_profile(user_id)
    if profile:
        profile.unlocked = False
        setattr(profile, 'onboarding_index', 0)
        profile.trait_themes = {}
        save_user_profile(profile)
    return {"status": "reset"}

# Onboarding progress is persisted per user in their profile (onboarding_index)

class OnboardingResponseInput(BaseModel):
    user_id: str
    response: str

@router.get("/api/onboarding/next-question")
def get_next_onboarding_question(user_id: str):
    from storage_service.memory.storage import load_user_profile, save_user_profile
    from storage_service.memory.models import UserProfile
    from datetime import datetime

    # Load or initialize user profile
    profile = load_user_profile(user_id)
    if not profile:
        profile = UserProfile(user_id=user_id, name=None, onboarding_date=datetime.utcnow())
        save_user_profile(profile)

    # Determine next prompt index
    index = getattr(profile, "onboarding_index", 0)
    total = len(ONBOARDING_PROMPTS)
    if index >= total:
        return {"message": "All onboarding prompts completed."}

    question = ask_onboarding_question(index)
    return {
        "question": question,
        "next_prompt_index": index,
        "total_prompts": total
    }

@router.post("/api/onboarding/respond")
def submit_onboarding_response(payload: OnboardingResponseInput):
    user_id = payload.user_id
    response = payload.response

    # Process user reply and update memory
    process_onboarding_response(user_id, response)

    # Load and update user profile for persistent onboarding index
    from storage_service.memory.storage import load_user_profile, save_user_profile
    from storage_service.memory.models import UserProfile

    profile = load_user_profile(user_id)
    # Increment onboarding index for next question
    current_index = getattr(profile, "onboarding_index", 0)
    if current_index < len(ONBOARDING_PROMPTS):
        profile.onboarding_index = current_index + 1
        save_user_profile(profile)

    unlocked = is_user_unlocked(user_id)

    return {
        "message": "Response processed",
        "trait_themes": {k: v.dict() for k, v in profile.trait_themes.items()},
        "next_prompt_index": profile.onboarding_index,
        "total_prompts": len(ONBOARDING_PROMPTS)
    }

class FeedbackInput(BaseModel):
    user_id: str
    feedback: str
    confirmation: str

@router.post("/api/onboarding/feedback")
def submit_onboarding_feedback(payload: FeedbackInput):
    """
    Receive user feedback on summary and log or store it as needed.
    """
    # Log feedback
    print(f"📝 Onboarding feedback from {payload.user_id}: {payload.confirmation} — {payload.feedback}")
    # Treat feedback as a new trait response to adaptively probe
    process_onboarding_response(payload.user_id, payload.feedback)
    # Advance onboarding index
    from storage_service.memory.storage import load_user_profile, save_user_profile
    from storage_service.memory.models import UserProfile
    profile = load_user_profile(payload.user_id)
    if profile:
        idx = getattr(profile, 'onboarding_index', 0)
        if idx < len(ONBOARDING_PROMPTS):
            profile.onboarding_index = idx + 1
            save_user_profile(profile)
    # Prepare next question or summary if unlocked
    profile = load_user_profile(payload.user_id)
    unlocked = is_user_unlocked(payload.user_id)
    # Serialize trait themes
    themes = {k: v.dict() for k, v in profile.trait_themes.items()} if profile else {}
    # Next question if not unlocked
    next_q = None
    if not unlocked and profile and profile.onboarding_index < len(ONBOARDING_PROMPTS):
        next_q = ask_onboarding_question(profile.onboarding_index)
    return {
        "status": "feedback received",
        "unlocked": unlocked,
        "trait_themes": themes,
        "next_question": next_q
    }
    
class CompleteInput(BaseModel):
    user_id: str
    summary: str
    confidence: float
    confirmation: str

@router.post("/api/onboarding/complete")
def complete_onboarding(payload: CompleteInput):
    """
    Finalize onboarding: save summary, mark user unlocked permanently.
    """
    from storage_service.memory.storage import load_user_profile, save_user_profile
    profile = load_user_profile(payload.user_id)
    if not profile:
        return {"error": "User profile not found"}
    # Save summary and unlock
    profile.summary = payload.summary
    profile.unlocked = True
    profile.trust_established_flag = True
    profile.last_session_summary = payload.summary  # optional semantic field
    profile.alignment_index_history.append(payload.confidence)  # if numeric   
    save_user_profile(profile)
    return {"status": "completed", "summary": payload.summary}

print("✅ Modern onboarding_routes loaded")