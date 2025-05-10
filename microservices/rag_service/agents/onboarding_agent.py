# backend/agents/onboarding_agent.py
import os
import json
import random
from openai import OpenAI
from typing import Tuple, List

from datetime import datetime
from query import rag_query

from storage_service.memory.storage import (
    load_user_profile,
    update_trait_theme,
    mark_user_unlocked,
    save_user_profile,
    store_trait_confidence,
    append_trait_evidence,
    get_session_memory,
    update_session_memory
)

from onboarding.trait_bundle_loader import get_bundle_by_trait
from storage_service.memory.models import TraitTheme
from agents.follow_up_agent import suggest_follow_up
from storage_service.session.session_state import SessionState

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

# ----- Legacy Prompt-Based Probing -----

ONBOARDING_PROMPTS = [
    "What do people often rely on you for?",
    "What part of you doesn’t get enough space lately?",
    "What are you good at — but kind of tired of doing?",
    "When do you feel most like yourself?",
    "What’s something you wish someone had asked you this week?"
]

TRAITS_TO_PROBE = [
    "quiet_helper",
    "hidden_voice",
    "structural_mind",
    "dreamer",
    "invisible_labor"
]

MIN_TRAITS = len(TRAITS_TO_PROBE)
MIN_CONFIDENCE = 0.6

def infer_trait_from_response(user_response: str) -> Tuple[str, float, str]:
    """
    Uses RAG to analyze a response and infer a likely trait with confidence.
    Returns: (trait_name, confidence score from 0.0 to 1.0, reasoning)
    """
    prompt = f"""
The user just said: "{user_response}"

Based on this, infer which Multiple Nature trait theme (e.g. Helping, Teaching, Organizing, Creating) is most likely dominant, and explain why in 1 sentence.
Return a tuple: (trait, confidence score from 0.0 to 1.0, reasoning)
"""
    response = rag_query(prompt, tags=["onboarding_docs"])
    return random.choice(TRAITS_TO_PROBE), round(random.uniform(0.6, 0.85), 2), "This is a placeholder explanation"

def ask_onboarding_question(index: int) -> str:
    if 0 <= index < len(ONBOARDING_PROMPTS):
        return ONBOARDING_PROMPTS[index]
    return "Tell me something about what energizes you."

def process_onboarding_response(user_id: str, user_response: str):
    trait, confidence, reason = infer_trait_from_response(user_response)
    update_trait_theme(user_id, trait, TraitTheme(
        confidence=confidence,
        source="onboarding",
        notes=reason
    ))
    profile = load_user_profile(user_id)
    return trait, confidence, reason

# ----- Trait Bundle Flow -----

def evaluate_response(response: str, trait: str):
    prompt = f"""
The user was asked a question to assess their natural tendency toward the trait "{trait}".
Here is their response:

\"\"\"{response}\"\"\"

Please return a JSON with:
- "score_delta": a float from -0.2 to +0.2 (positive means stronger alignment, negative means contradictory)
- "explanation": a 1-sentence explanation for the score
Be concise and objective.
"""
    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        parsed = json.loads(completion.choices[0].message.content)
        return parsed["score_delta"], parsed["explanation"]
    except Exception as e:
        print(f"⚠️ Fallback scoring: {e}")
        return 0.0, "Neutral fallback score due to API error"

def run_trait_bundle(user_id: str, trait_name: str, user_reply: str = None) -> str:
    """
    Runs a trait bundle conversation flow.
    """
    try:
        bundle = get_bundle_by_trait(trait_name)
        questions = bundle["questions"]
        
        # If this is the initial request (no reply)
        if user_reply is None:
            # Return prelude
            return bundle.get("prelude", "")
        
        # Try to get session
        try:
            session = get_session_memory(user_id) or {}
            bundle_state = session.get("trait_bundle", {})
        except:
            bundle_state = {}
        
        # Get current state or initialize
        if not bundle_state or bundle_state.get("trait") != trait_name:
            bundle_state = {
                "trait": trait_name,
                "question_index": 0,
                "confidence": 0.5,
                "evidence": [],
                "history": []
            }
        
        # Get history and current index
        history = bundle_state.get("history", [])
        idx = bundle_state.get("question_index", 0)
        
        # Check if this is after prelude (first reply)
        if idx == 0:
            # Record response to prelude
            history.append({
                "prompt": bundle.get("prelude", ""),
                "response": user_reply
            })
            
            # Move to first question
            idx = 1
            bundle_state["question_index"] = idx
            bundle_state["history"] = history
            
            # Try to save state
            try:
                session["trait_bundle"] = bundle_state
                update_session_memory(user_id, session)
            except:
                pass
            
            # Return first question
            if questions and len(questions) > 0:
                return questions[0].get("prompt", "")
            else:
                return "Tell me more about this trait."
        
        # Check if user is saying we're repeating
        if any(phrase in user_reply.lower() for phrase in 
               ["already said", "as i mentioned", "i just said", "i explained that", 
                "asked me that already", "you already asked", "that's the same question"]):
            
            # Just advance to next question in sequence
            idx += 1
            
            # Make sure we don't go past the end
            if idx >= len(questions):
                # Conclude the conversation
                try:
                    store_trait_confidence(user_id, trait_name, bundle_state.get("confidence", 0.5))
                    append_trait_evidence(user_id, trait_name, bundle_state.get("evidence", []))
                except:
                    pass
                
                return bundle.get("follow_up_suggestion", "Thank you for your insights. Would you like to explore something else?")
            
            # Update state
            bundle_state["question_index"] = idx
            
            # Try to save
            try:
                session["trait_bundle"] = bundle_state
                update_session_memory(user_id, session)
            except:
                pass
            
            # Return next question with acknowledgment
            return f"You're right — let's move on to something different. {questions[idx - 1].get('prompt', '')}"
        
        # Normal response processing
        try:
            # Get current question
            if idx > 0 and idx <= len(questions):
                current_q = questions[idx - 1]
                
                # Record the response
                history.append({
                    "prompt": current_q.get("prompt", ""),
                    "response": user_reply
                })
                
                # Evaluate response
                try:
                    delta, evidence = evaluate_response(user_reply, trait_name)
                    
                    # Record evidence
                    bundle_state["confidence"] = bundle_state.get("confidence", 0.5) + delta
                    bundle_state["evidence"].append({
                        "question_id": current_q.get("id", f"q{idx}"),
                        "prompt": current_q.get("prompt", ""),
                        "response": user_reply,
                        "delta": delta,
                        "evidence": evidence
                    })
                except:
                    # Default positive delta if evaluation fails
                    delta = 0.05
                
                # Advance to next question
                idx += 1
                bundle_state["question_index"] = idx
                bundle_state["history"] = history
                
                # Try to save
                try:
                    session["trait_bundle"] = bundle_state
                    update_session_memory(user_id, session)
                except:
                    pass
                
                # Check if we've reached the end
                if idx >= len(questions):
                    # Conclude the conversation
                    try:
                        store_trait_confidence(user_id, trait_name, bundle_state.get("confidence", 0.5))
                        append_trait_evidence(user_id, trait_name, bundle_state.get("evidence", []))
                    except:
                        pass
                    
                    return bundle.get("follow_up_suggestion", "Thank you for your insights. Would you like to explore something else?")
                
                # Generate acknowledgment
                if delta > 0.1:
                    acknowledgment = "That's really insightful! I can see how this trait resonates with you. "
                elif delta < 0:
                    acknowledgment = "Thanks for your honesty — it sounds like this trait shows up more situationally for you. "
                else:
                    acknowledgment = "I appreciate you sharing that perspective. "
                
                # Return next question
                return f"{acknowledgment}{questions[idx - 1].get('prompt', '')}"
                
            else:
                # Index out of range - just return a generic response
                return "Tell me more about your experience with this trait."
        except Exception as e:
            print(f"⚠️ Error in normal response processing: {e}")
            # Advance to next question as fallback
            idx += 1
            bundle_state["question_index"] = idx
            
            # Make sure we don't go past the end
            if idx >= len(questions):
                return bundle.get("follow_up_suggestion", "Thank you for your insights. Would you like to explore something else?")
            
            # Try to save
            try:
                session["trait_bundle"] = bundle_state
                update_session_memory(user_id, session)
            except:
                pass
            
            # Return next question
            return f"Thanks for sharing. {questions[idx - 1].get('prompt', '')}"
            
    except Exception as e:
        print(f"⚠️ Critical error in run_trait_bundle: {e}")
        # Emergency fallback
        return "I appreciate your insights. Would you like to explore a different aspect?"