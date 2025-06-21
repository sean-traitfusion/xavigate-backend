-- Drop old tables if they exist
DROP TABLE IF EXISTS interaction_logs CASCADE;
DROP TABLE IF EXISTS session_prompts CASCADE;

-- Recreate tables with uuid column (contains user_id value)
CREATE TABLE IF NOT EXISTS interaction_logs (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(255) NOT NULL,
    interaction_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT,
    assistant_response TEXT,
    rag_context TEXT,
    strategy VARCHAR(100),
    model VARCHAR(100),
    tools_called TEXT
);

CREATE INDEX IF NOT EXISTS idx_interaction_logs_uuid_created 
ON interaction_logs (uuid, created_at);

CREATE TABLE IF NOT EXISTS session_prompts (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(255) NOT NULL,
    system_prompt TEXT,
    persistent_summary TEXT,
    session_context TEXT,
    final_prompt TEXT,
    prompt_length INTEGER,
    estimated_tokens INTEGER,
    strategy VARCHAR(50),
    model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_session_prompts_uuid 
ON session_prompts (uuid);