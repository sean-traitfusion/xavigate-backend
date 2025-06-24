-- Fix all missing columns in memory-related tables

-- 1. Note: summarization_events uses 'uuid' column to store user_id
-- No need to add user_id/session_id columns as the code expects uuid column

-- 2. Check and fix session_memory table
ALTER TABLE session_memory
ADD COLUMN IF NOT EXISTS user_id VARCHAR(255);

ALTER TABLE session_memory
ADD COLUMN IF NOT EXISTS session_id VARCHAR(255);

-- 3. Check and fix persistent_memory table  
ALTER TABLE persistent_memory
ADD COLUMN IF NOT EXISTS user_id VARCHAR(255);

-- 4. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_summarization_events_user_id 
ON summarization_events (user_id);

CREATE INDEX IF NOT EXISTS idx_summarization_events_session_id
ON summarization_events (session_id);

-- 5. Clear the problematic oversized session
DELETE FROM session_memory 
WHERE session_id = '14784478-3091-7098-065d-6cd64d8b9988' 
   OR uuid = '14784478-3091-7098-065d-6cd64d8b9988';

-- Show updated schemas
\echo 'summarization_events table:'
\d summarization_events

\echo 'session_memory table:'
\d session_memory