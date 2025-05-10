# backend/memory/storage.py
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from typing import List
from .models import UserProfile, SessionRecord
import os
import time
import psycopg2
from psycopg2 import OperationalError
import psycopg2.extras
from dotenv import load_dotenv
load_dotenv()

USE_DB = os.getenv("ENV") != "dev"

if USE_DB:
    
    def wait_for_postgres(url, retries=10):
        for i in range(retries):
            try:
                return psycopg2.connect(url)
            except OperationalError as e:
                print(f"⏳ Waiting for Postgres... ({i+1}/{retries})")
                time.sleep(2)
        raise RuntimeError("Postgres did not become available")

    conn = wait_for_postgres(os.getenv("DATABASE_URL"))
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # ← Use DictCursor

DATA_DIR = Path("backend/memory/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

from storage_service.session.session_state import PromptExchange

def get_session_memory(user_id: str) -> dict:
    filepath = DATA_DIR / f"user_{user_id}.json"
    if not filepath.exists():
        return {}
    with open(filepath, "r") as f:
        data = json.load(f)
        return data.get("session_state", {})

def update_session_memory(user_id: str, session_state: dict):
    filepath = DATA_DIR / f"user_{user_id}.json"
    if not filepath.exists():
        print("⚠️ User profile not found for session update.")
        return
    with open(filepath, "r") as f:
        data = json.load(f)
    data["session_state"] = session_state
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
        
def load_session_history(user_id: str) -> List[PromptExchange]:
    if not USE_DB:
        print("🧪 Returning mock session history")
        return []

    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (user_id,))
    result = cursor.fetchone()
    if not result or not result["conversation_log"]:
        return []

    try:
        exchanges = result["conversation_log"].get("exchanges", [])
        return [
            PromptExchange(
                user_prompt=entry.get("user_prompt", ""),
                assistant_response=entry.get("assistant_response", ""),
                tags=entry.get("tags", [])
            )
            for entry in exchanges
        ]
    except Exception as e:
        print(f"⚠️ Failed to parse conversation_log: {e}")
        return []

def get_user_filepath(user_id: str) -> Path:
    return DATA_DIR / f"user_{user_id}.json"


def load_user_profile(user_id: str) -> Optional[UserProfile]:
    filepath = get_user_filepath(user_id)
    if filepath.exists():
        with open(filepath, "r") as f:
            data = json.load(f)
            return UserProfile(**data)

    if USE_DB:
        cursor.execute("SELECT * FROM user_memory WHERE uuid = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            trait_history = result["trait_history"] or {}
            return UserProfile(
                user_id=result["uuid"],
                name=result.get("name", "User"), # Default name if not found
                onboarding_date=result["created_at"],
                alignment_index_history=[],  # placeholder
                quadrant_history=[],         # placeholder
                avatar_profile=None,
                dominant_traits=trait_history.get("dominant_traits", []),
                suppressed_traits=trait_history.get("suppressed_traits", []),
                trust_established_flag=True,
                alignment_tags=[],
                alignment_stage="Imported from DB"
            )
    return None

    if USE_DB:
        cursor.execute("SELECT * FROM user_memory WHERE uuid = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            # TODO: map DB row into UserProfile fields
            ...
    return None


def save_user_profile(profile: UserProfile):
    filepath = get_user_filepath(profile.user_id)
    with open(filepath, "w") as f:
        json.dump(profile.dict(), f, indent=2, default=str)


def save_session_record(record: SessionRecord):
    session_log_path = DATA_DIR / f"sessions_{record.user_id}.jsonl"
    with open(session_log_path, "a") as f:
        json.dump(record.dict(), f, default=str)
        f.write("\n")


def get_alignment_history(user_id: str) -> list:
    filepath = DATA_DIR / f"sessions_{user_id}.jsonl"
    if not filepath.exists():
        return []
    with open(filepath, "r") as f:
        return [json.loads(line) for line in f.readlines()]
    
def purge_expired_session_memory():
    if not USE_DB:
        print("🧪 Skipping purge in dev mode")
        return

    cursor.execute("DELETE FROM session_memory WHERE expires_at < NOW();")
    print("🧹 Expired session memory purged")

from .models import TraitTheme

def update_trait_theme(user_id: str, trait_name: str, new_theme: TraitTheme):
    profile = load_user_profile(user_id)
    if not profile:
        print(f"❌ User profile not found for {user_id}")
        return

    profile.trait_themes[trait_name] = new_theme
    save_user_profile(profile)
    print(f"✅ Updated trait theme: {trait_name} → {new_theme.confidence}")

def store_trait_confidence(user_id: str, trait_name: str, confidence: float):
    profile = load_user_profile(user_id)
    if not profile:
        print(f"❌ No profile found for {user_id}")
        return

    if trait_name not in profile.trait_themes:
        profile.trait_themes[trait_name] = TraitTheme(
            confidence=confidence,
            source="bundle",
            notes="Trait inferred via bundle interaction"
        )
    else:
        profile.trait_themes[trait_name].confidence = confidence
        profile.trait_themes[trait_name].source = "bundle"

    save_user_profile(profile)
    print(f"📊 Stored {trait_name} confidence for {user_id}: {confidence:.2f}")

def append_trait_evidence(user_id: str, trait_name: str, evidence_list: list):
    profile = load_user_profile(user_id)
    if not profile:
        print(f"❌ No profile found for {user_id}")
        return

    notes = "\n".join(f"- {e['evidence']}" for e in evidence_list)
    if trait_name not in profile.trait_themes:
        profile.trait_themes[trait_name] = TraitTheme(
            confidence=0.5,
            source="bundle",
            notes=notes
        )
    else:
        existing_notes = profile.trait_themes[trait_name].notes or ""
        profile.trait_themes[trait_name].notes = f"{existing_notes}\n{notes}".strip()

    save_user_profile(profile)
    print(f"🧾 Appended evidence to {trait_name} for {user_id}")

def mark_user_unlocked(user_id: str):
    profile = load_user_profile(user_id)
    if not profile:
        print(f"❌ User profile not found for {user_id}")
        return

    profile.unlocked = True
    save_user_profile(profile)
    print(f"🔓 User {user_id} is now marked as unlocked.")

def is_user_unlocked(user_id: str) -> bool:
    profile = load_user_profile(user_id)
    return profile.unlocked if profile else False

# Dev test hook
def init_test_user():
    profile = UserProfile(
        user_id="test123",
        name="Test User",
        onboarding_date=datetime.now(),
        dominant_traits=["Creative", "Healing"],
        alignment_stage="Early Discovery",
        trust_established_flag=True
    )
    save_user_profile(profile)
    print("✅ Test user initialized")
