"""
Chat Pipeline Logger - Captures comprehensive logging data for the chat pipeline
"""

import httpx
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio
import json


class ChatPipelineLogger:
    """Logger for capturing chat pipeline data including prompts, responses, and metrics"""
    
    def __init__(self, storage_url: str):
        self.storage_url = storage_url
        self.start_time = None
        self.metrics = {}
        
    def start_request(self):
        """Mark the start of a request for timing"""
        self.start_time = datetime.utcnow()
        self.metrics = {
            "memory_fetch_ms": 0,
            "rag_fetch_ms": 0,
            "llm_call_ms": 0,
            "total_ms": 0
        }
        
    def log_timing(self, metric_name: str, start_time: datetime):
        """Log timing for a specific operation"""
        if metric_name in self.metrics:
            elapsed_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.metrics[metric_name] = round(elapsed_ms, 2)
            
    async def log_chat_interaction(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        assistant_response: str,
        system_prompt: str,
        final_prompt: str,
        rag_context: str,
        model: str,
        model_params: Dict[str, Any],
        session_memory: str,
        persistent_memory: str,
        error: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """Log complete chat interaction to storage service"""
        
        # Calculate total time
        if self.start_time:
            self.metrics["total_ms"] = round(
                (datetime.utcnow() - self.start_time).total_seconds() * 1000, 2
            )
        
        # Debug logging
        print(f"Debug - Session memory length: {len(session_memory) if session_memory else 0}")
        print(f"Debug - Persistent memory length: {len(persistent_memory) if persistent_memory else 0}")
        print(f"Debug - RAG context length: {len(rag_context) if rag_context else 0}")
        
        # Use same timestamp for both logs to ensure matching
        current_timestamp = datetime.utcnow().isoformat()
        
        # Prepare interaction log
        interaction_log = {
            "interaction_id": str(uuid.uuid4()),
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": current_timestamp,
            "user_message": user_message,
            "assistant_response": assistant_response,
            "rag_context": rag_context,
            "strategy": "chat",
            "model": model,
            "tools_called": json.dumps({
                "model_params": model_params,
                "metrics": self.metrics,
                "error": error
            })
        }
        
        # Prepare session prompts log for debugging
        prompt_log = {
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": current_timestamp,  # Use same timestamp as interaction log
            "system_prompt": system_prompt,
            "persistent_summary": persistent_memory,
            "session_context": session_memory,
            "final_prompt": final_prompt,
            "prompt_length": len(final_prompt),
            "estimated_tokens": len(final_prompt) // 4,  # Rough estimate
            "strategy": "chat",
            "model": model,
            "metadata": json.dumps({
                "model_params": model_params,
                "metrics": self.metrics,
                "rag_chunks": len(rag_context.split("\n\n")) if rag_context else 0
            })
        }
        
        # Log to storage service asynchronously (fire-and-forget to avoid blocking)
        asyncio.create_task(self._send_logs(interaction_log, prompt_log, headers))
        
    async def _send_logs(self, interaction_log: Dict, prompt_log: Dict, headers: Optional[Dict]):
        """Send logs to storage service"""
        try:
            print(f"Attempting to log interaction for user: {interaction_log['user_id']}")
            async with httpx.AsyncClient() as client:
                # Log interaction
                resp1 = await client.post(
                    f"{self.storage_url}/api/logging/interaction",
                    json=interaction_log,
                    headers=headers or {},
                    timeout=5.0
                )
                print(f"Interaction log response: {resp1.status_code}")
                
                # Log prompts for debugging
                resp2 = await client.post(
                    f"{self.storage_url}/api/logging/prompt",
                    json=prompt_log,
                    headers=headers or {},
                    timeout=5.0
                )
                print(f"Prompt log response: {resp2.status_code}")
        except Exception as e:
            # Still log the error for debugging
            print(f"Failed to log chat interaction: {e}")