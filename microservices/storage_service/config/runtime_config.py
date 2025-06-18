# runtime_config.py
"""
Runtime configuration management for memory system
Based on Mobeus architecture but adapted for Xavigate
"""
import os
import json
from typing import Any, Dict
from pathlib import Path

# In-memory config store
_config_store: Dict[str, Any] = {}
_is_initialized: bool = False

# Default configuration values
DEFAULT_CONFIG = {
    # Memory limits
    "SESSION_MEMORY_CHAR_LIMIT": 15000,
    "PERSISTENT_MEMORY_CHAR_LIMIT": 8000,
    "PERSISTENT_MEMORY_COMPRESSION_RATIO": 0.6,
    "PERSISTENT_MEMORY_COMPRESSION_MODEL": "gpt-4",
    "PERSISTENT_MEMORY_MIN_SIZE": 1000,
    "PERSISTENT_MEMORY_MAX_COMPRESSIONS": 3,
    "MAX_PROMPT_CHARS": 20000,
    "RAG_CONTEXT_CHAR_LIMIT": 4000,
    
    # Summarization settings
    "SESSION_SUMMARY_PROMPT": """Please summarize the following conversation between a user and an AI assistant. Focus on:

1. **Personal Information**: Name, job, location, family, friends, interests, preferences
2. **User's Goals & Inquiries**: What they're trying to achieve, questions they've asked
3. **Key Context**: Important facts, decisions made, ongoing projects or topics
4. **Trait Analysis**: Their personality traits, strengths, areas of growth
5. **Action Items**: Any tasks, follow-ups, or commitments mentioned

Keep the summary concise but comprehensive. Maintain the user's voice and perspective where relevant.

Conversation to summarize:
{conversation_text}

Summary:""",
    
    "PERSISTENT_MEMORY_COMPRESSION_PROMPT": """You are an AI assistant tasked with compressing a user's long-term memory profile.
The current profile contains multiple conversation summaries accumulated over time. Your goal is to create a more concise version that preserves ALL critical information.

CRITICAL: You must preserve:
1. **Personal Information**: Full name, occupation, company, location, family members, relationships
2. **Trait Profile**: Their dominant traits, suppressed traits, alignment metrics
3. **Goals and Objectives**: Both short-term and long-term goals, personal growth areas
4. **Preferences and Patterns**: Communication style, expertise level, working style
5. **Important History**: Key decisions made, major milestones, important context from past conversations
6. **Specific Details**: Any specific names, dates, numbers, or details mentioned

Compression Guidelines:
- Merge redundant information intelligently
- Maintain chronological context where important
- Use clear, concise language
- Preserve the user's voice and terminology
- Aim to reduce by {compression_ratio}% while keeping ALL important facts
- If you see [COMPRESSED SUMMARY as of DATE] markers, this indicates previous compressions

Current profile to compress:
{current_summary}

Compressed profile:""",
    
    # Model settings
    "GPT_MODEL": "gpt-4",
    "TEMPERATURE": 0.7,
    "SUMMARY_TEMPERATURE": 0.3,
    
    # Feature flags
    "AUTO_SUMMARY_ENABLED": True,
    "AUTO_COMPRESSION_ENABLED": True,
    
    # OpenAI Settings (for future expansion)
    "OPENAI_MODEL": "gpt-3.5-turbo",
    "OPENAI_MAX_TOKENS": 2000,
    "OPENAI_TEMPERATURE": 0.7,
    "OPENAI_TOP_P": 1.0,
    "OPENAI_FREQUENCY_PENALTY": 0.0,
    "OPENAI_PRESENCE_PENALTY": 0.0,
    "OPENAI_TIMEOUT": 30,
    
    # Chat Service Settings
    "SYSTEM_PROMPT": """You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

CORE PRINCIPLES:
- Every person has 19 distinct traits that form their Multiple Natures profile
- Traits scored 7-10 are dominant traits (natural strengths)
- Traits scored 1-3 are suppressed traits (areas needing attention)
- Traits scored 4-6 are balanced traits
- True alignment comes from expressing all traits appropriately, not just dominant ones

YOUR APPROACH:
1. ALWAYS reference the user's specific trait scores when giving advice
2. Connect their challenges/questions to their trait profile
3. Suggest concrete actions that engage both dominant AND suppressed traits
4. Use the MN glossary context to ground advice in Multiple Natures methodology
5. Build on previous conversations using session memory and persistent summaries

CONVERSATION STYLE:
- Be warm, insightful, and encouraging
- Use specific examples related to their traits
- Avoid generic advice - everything should be personalized
- Reference their past conversations and progress when relevant

Remember: You're not just answering questions - you're helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment.""",
    
    "CONVERSATION_HISTORY_LIMIT": 5,
    "TOP_K_RAG_HITS": 5,
    "PROMPT_STYLE": "default",
    "CUSTOM_STYLE_MODIFIER": None,
    
    # Additional model settings for chat
    "CHAT_MODEL": "gpt-3.5-turbo",
    "CHAT_TEMPERATURE": 0.7,
    "CHAT_MAX_TOKENS": 1000,
    "CHAT_PRESENCE_PENALTY": 0.1,
    "CHAT_FREQUENCY_PENALTY": 0.1,
}

def _load_from_env():
    """Load configuration from environment variables"""
    global _config_store, _is_initialized
    _config_store = DEFAULT_CONFIG.copy()
    _is_initialized = True
    
    # First, try to load from .env file directly for multiline strings
    _load_multiline_from_env_file()
    
    # Override with environment variables if they exist
    for key, default_value in DEFAULT_CONFIG.items():
        env_value = os.getenv(key)
        if env_value is not None:
            # Skip if this is a multiline key that was already loaded from .env file
            if key in ["SESSION_SUMMARY_PROMPT", "PERSISTENT_MEMORY_COMPRESSION_PROMPT"]:
                if key in _config_store and len(_config_store[key]) > len(env_value):
                    continue
            
            # Try to convert to appropriate type
            if isinstance(default_value, bool):
                _config_store[key] = env_value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(default_value, int):
                try:
                    _config_store[key] = int(env_value)
                except ValueError:
                    print(f"Warning: Could not parse {key}={env_value} as int, using default")
                    _config_store[key] = default_value
            elif isinstance(default_value, float):
                try:
                    _config_store[key] = float(env_value)
                except ValueError:
                    print(f"Warning: Could not parse {key}={env_value} as float, using default")
                    _config_store[key] = default_value
            elif isinstance(default_value, list):
                try:
                    if env_value.startswith('['):
                        _config_store[key] = json.loads(env_value)
                    else:
                        _config_store[key] = [x.strip() for x in env_value.split(',')]
                except (json.JSONDecodeError, ValueError):
                    print(f"Warning: Could not parse {key}={env_value} as list, using default")
                    _config_store[key] = default_value
            else:
                _config_store[key] = env_value

def _load_multiline_from_env_file(filepath: str = ".env"):
    """Load multiline string values directly from .env file"""
    # Look for .env file in service directory first, then parent directories
    service_env = Path(__file__).parent.parent / filepath
    root_env = Path(__file__).parent.parent.parent.parent / filepath
    
    env_path = None
    if service_env.exists():
        env_path = service_env
    elif root_env.exists():
        env_path = root_env
    
    if not env_path:
        return
    
    # Keys that are known to be multiline
    multiline_keys = [
        "SESSION_SUMMARY_PROMPT", 
        "PERSISTENT_MEMORY_COMPRESSION_PROMPT"
    ]
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Parse each multiline key
        for key in multiline_keys:
            if key not in content:
                continue
                
            # Find the key and extract its value
            pattern = f'{key}='
            start = content.find(pattern)
            if start == -1:
                continue
                
            start += len(pattern)
            
            # Handle quoted strings
            if content[start] == '"':
                # Find the closing quote, handling escaped quotes
                end = start + 1
                while end < len(content):
                    if content[end] == '"' and content[end-1] != '\\':
                        break
                    end += 1
                
                if end < len(content):
                    value = content[start+1:end]
                    # Unescape the value
                    try:
                        value = json.loads('"' + value + '"')
                        _config_store[key] = value
                    except json.JSONDecodeError:
                        # Fall back to the raw value
                        _config_store[key] = value.replace('\\r\\n', '\n').replace('\\n', '\n')
    except Exception as e:
        print(f"Warning: Error loading multiline values from .env: {e}")

def get(key: str, default: Any = None) -> Any:
    """Get a configuration value"""
    if not _is_initialized:
        _load_from_env()
    return _config_store.get(key, default)

def set_config(key: str, value: Any) -> None:
    """Set a configuration value"""
    if not _is_initialized:
        _load_from_env()
    _config_store[key] = value

def all_config() -> Dict[str, Any]:
    """Get all configuration values"""
    if not _is_initialized:
        _load_from_env()
    return _config_store.copy()

def reset_to_defaults() -> None:
    """Reset all configuration to default values"""
    global _config_store, _is_initialized
    _config_store = DEFAULT_CONFIG.copy()
    _is_initialized = True  # Important: mark as initialized to prevent reload from env

# Force initialization on import
_config_store = {}
_load_from_env()