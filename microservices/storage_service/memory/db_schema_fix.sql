-- Fix for session_memory table schema mismatch
ALTER TABLE session_memory 
ADD COLUMN IF NOT EXISTS user_id VARCHAR(255),
ADD COLUMN IF NOT EXISTS session_id VARCHAR(255);

-- Update existing data if needed (assuming uuid contains session_id)
UPDATE session_memory 
SET session_id = uuid,
    user_id = uuid
WHERE session_id IS NULL;

-- Create index for new columns
CREATE INDEX IF NOT EXISTS idx_session_memory_session_user 
ON session_memory (session_id, user_id, created_at);

-- Fix for persistent_memory table schema mismatch
ALTER TABLE persistent_memory 
ADD COLUMN IF NOT EXISTS user_id VARCHAR(255);

-- Update existing data if needed
UPDATE persistent_memory 
SET user_id = uuid
WHERE user_id IS NULL;

-- Create index for new column
CREATE INDEX IF NOT EXISTS idx_persistent_memory_user_id 
ON persistent_memory (user_id);