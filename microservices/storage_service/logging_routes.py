"""
Logging API routes for storing chat interaction logs and prompts
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import json
from memory.db import get_connection

router = APIRouter()


class InteractionLog(BaseModel):
    """Model for logging chat interactions"""
    interaction_id: str
    user_id: str
    session_id: str
    timestamp: str
    user_message: str
    assistant_response: str
    rag_context: str
    strategy: str = "chat"
    model: str
    tools_called: str  # JSON string with metrics and error info


class PromptLog(BaseModel):
    """Model for logging prompts for debugging"""
    user_id: str
    session_id: str
    timestamp: str
    system_prompt: str
    persistent_summary: str
    session_context: str
    final_prompt: str
    prompt_length: int
    estimated_tokens: int
    strategy: str = "chat"
    model: str
    metadata: str  # JSON string with additional metadata


@router.post("/interaction")
def save_interaction_log(log: InteractionLog):
    """Log a chat interaction to the database"""
    try:
        query = """
            INSERT INTO interaction_logs (
                uuid, interaction_id, created_at, user_message, 
                assistant_response, rag_context, strategy, model, tools_called
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (interaction_id) DO NOTHING
        """
        
        params = (
            log.user_id,
            log.interaction_id,
            datetime.fromisoformat(log.timestamp),
            log.user_message,
            log.assistant_response,
            log.rag_context,
            log.strategy,
            log.model,
            log.tools_called
        )
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                print(f"Successfully saved interaction log: {log.interaction_id}")
        
        return {"status": "success", "interaction_id": log.interaction_id}
        
    except Exception as e:
        print(f"Error logging interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to log interaction: {str(e)}")


@router.post("/prompt")
def save_prompt_log(log: PromptLog):
    """Log prompt details for debugging"""
    try:
        # Parse metadata to extract session_id if needed
        metadata_dict = json.loads(log.metadata)
        
        query = """
            INSERT INTO session_prompts (
                uuid, system_prompt, persistent_summary, session_context,
                final_prompt, prompt_length, estimated_tokens, strategy, 
                model, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            log.user_id,
            log.system_prompt,
            log.persistent_summary,
            log.session_context,
            log.final_prompt,
            log.prompt_length,
            log.estimated_tokens,
            log.strategy,
            log.model,
            datetime.fromisoformat(log.timestamp)
        )
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                print(f"Successfully saved prompt log for user: {log.user_id}")
        
        return {"status": "success", "timestamp": log.timestamp}
        
    except Exception as e:
        print(f"Error logging prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to log prompt: {str(e)}")


@router.get("/interactions/{user_id}")
def get_user_interactions(
    user_id: str, 
    limit: int = 50,
    offset: int = 0
):
    """Retrieve interaction logs for a user"""
    try:
        query = """
            SELECT 
                interaction_id,
                created_at,
                user_message,
                assistant_response,
                rag_context,
                model,
                tools_called
            FROM interaction_logs
            WHERE uuid = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id, limit, offset))
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
        
        interactions = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            # Handle tools_called safely
            tools_data = {}
            if row_dict['tools_called']:
                try:
                    tools_data = json.loads(row_dict['tools_called'])
                except json.JSONDecodeError:
                    tools_data = {"raw": row_dict['tools_called']}
            interactions.append({
                "interaction_id": row_dict['interaction_id'],
                "timestamp": row_dict['created_at'].isoformat(),
                "user_message": row_dict['user_message'],
                "assistant_response": row_dict['assistant_response'],
                "rag_context": row_dict['rag_context'],
                "model": row_dict['model'],
                "metrics": tools_data.get('metrics', {}),
                "error": tools_data.get('error')
            })
            
        return {"interactions": interactions, "count": len(interactions)}
        
    except Exception as e:
        print(f"Error retrieving interactions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve interactions: {str(e)}")


@router.get("/prompts/{user_id}")
def get_user_prompts(
    user_id: str,
    limit: int = 20,
    offset: int = 0
):
    """Retrieve prompt logs for a user"""
    try:
        query = """
            SELECT 
                created_at,
                system_prompt,
                persistent_summary,
                session_context,
                final_prompt,
                prompt_length,
                estimated_tokens,
                model
            FROM session_prompts
            WHERE uuid = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id, limit, offset))
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
        
        prompts = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            prompts.append({
                "timestamp": row_dict['created_at'].isoformat(),
                "system_prompt": row_dict['system_prompt'],
                "persistent_summary": row_dict['persistent_summary'],
                "session_context": row_dict['session_context'],
                "final_prompt": row_dict['final_prompt'],
                "prompt_length": row_dict['prompt_length'],
                "estimated_tokens": row_dict['estimated_tokens'],
                "model": row_dict['model']
            })
            
        return {"prompts": prompts, "count": len(prompts)}
        
    except Exception as e:
        print(f"Error retrieving prompts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve prompts: {str(e)}")


@router.get("/all-interactions")
def get_all_interactions(
    limit: int = 100,
    offset: int = 0
):
    """Retrieve all interaction logs (for admin dashboard)"""
    try:
        query = """
            SELECT 
                uuid,
                interaction_id,
                created_at,
                user_message,
                assistant_response,
                rag_context,
                model,
                tools_called
            FROM interaction_logs
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (limit, offset))
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                
                # Get total count
                cur.execute("SELECT COUNT(*) FROM interaction_logs")
                total_count = cur.fetchone()[0]
        
        interactions = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            # Handle tools_called safely
            tools_data = {}
            if row_dict['tools_called']:
                try:
                    tools_data = json.loads(row_dict['tools_called'])
                except json.JSONDecodeError:
                    tools_data = {"raw": row_dict['tools_called']}
            interactions.append({
                "user_id": row_dict['uuid'],
                "interaction_id": row_dict['interaction_id'],
                "timestamp": row_dict['created_at'].isoformat(),
                "user_message": row_dict['user_message'],
                "assistant_response": row_dict['assistant_response'],
                "rag_context": row_dict['rag_context'],
                "model": row_dict['model'],
                "metrics": tools_data.get('metrics', {}),
                "error": tools_data.get('error')
            })
            
        return {
            "interactions": interactions, 
            "count": len(interactions),
            "total": total_count
        }
        
    except Exception as e:
        print(f"Error retrieving all interactions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve interactions: {str(e)}")