-- Fix for summarization_events table schema
-- This adds the missing user_id and session_id columns

-- First, check if columns already exist to avoid errors
DO $$ 
BEGIN
    -- Add user_id column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'summarization_events' 
        AND column_name = 'user_id'
    ) THEN
        ALTER TABLE summarization_events 
        ADD COLUMN user_id VARCHAR(255);
    END IF;

    -- Add session_id column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'summarization_events' 
        AND column_name = 'session_id'
    ) THEN
        ALTER TABLE summarization_events 
        ADD COLUMN session_id VARCHAR(255);
    END IF;
END $$;

-- Update existing rows to use uuid as both user_id and session_id for now
UPDATE summarization_events 
SET user_id = uuid, 
    session_id = uuid 
WHERE user_id IS NULL OR session_id IS NULL;

-- For future entries, we should not allow nulls
-- But we'll handle this in the application code to avoid breaking existing data