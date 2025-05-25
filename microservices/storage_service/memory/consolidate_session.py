# /backend/memory/consolidate_session.py
from memory.models import UserMemory
from uuid import UUID
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def synthesize_persistent_update(uuid: UUID, plan: dict, critique: str, transcript: str = "") -> UserMemory:
    try:
        prompt = (
            "From this chat transcript, extract any personal information the user shared "
            "such as job, location, family, or friends. Focus on what's relevant to their identity "
            "or ongoing context.\n\n" + transcript
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3,
        )
        extracted = response.choices[0].message.content.strip()
    except Exception as e:
        extracted = "Extraction unavailable."

    return UserMemory(
        uuid=uuid,
        initial_personality_scores={"context_capture": 1.0},
        score_explanations={"context_capture": "Derived from session summarization process"},
        trait_history={"context_extracted": [extracted]},
        preferences={},
    )