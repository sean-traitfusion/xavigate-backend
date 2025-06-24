-- Fix interaction_logs table by adding missing user_id and session_id columns
-- This fixes the "null value in column user_id" error

-- Add user_id column if it doesn't exist
ALTER TABLE interaction_logs 
ADD COLUMN IF NOT EXISTS user_id VARCHAR(255);

-- Add session_id column if it doesn't exist  
ALTER TABLE interaction_logs
ADD COLUMN IF NOT EXISTS session_id VARCHAR(255);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_interaction_logs_user_id 
ON interaction_logs (user_id);

CREATE INDEX IF NOT EXISTS idx_interaction_logs_session_id
ON interaction_logs (session_id);

-- For existing rows, copy uuid value to user_id if user_id is null
-- (since uuid column contains user_id values in this system)
UPDATE interaction_logs 
SET user_id = uuid 
WHERE user_id IS NULL AND uuid IS NOT NULL;

-- For existing rows where session_id is null, try to extract from interaction_id
-- interaction_id format is typically: user_id_session_id_timestamp_count
UPDATE interaction_logs
SET session_id = CASE 
    WHEN interaction_id LIKE '%_%_%_%' THEN 
        split_part(interaction_id, '_', 2)
    ELSE 
        uuid  -- fallback to uuid if pattern doesn't match
END
WHERE session_id IS NULL;

-- Show the updated schema
\d interaction_logs