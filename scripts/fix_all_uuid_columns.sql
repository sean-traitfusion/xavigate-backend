-- Fix all tables that have uuid columns by renaming to user_id
-- This matches the authentication system that uses user_id

-- Check and rename columns in existing tables
DO $$ 
BEGIN
    -- session_memory table
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='session_memory' AND column_name='uuid') THEN
        ALTER TABLE session_memory RENAME COLUMN uuid TO user_id;
    END IF;
    
    -- persistent_memory table
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='persistent_memory' AND column_name='uuid') THEN
        ALTER TABLE persistent_memory RENAME COLUMN uuid TO user_id;
    END IF;
    
    -- summarization_events table
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='summarization_events' AND column_name='uuid') THEN
        ALTER TABLE summarization_events RENAME COLUMN uuid TO user_id;
    END IF;
    
    -- compression_events table
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='compression_events' AND column_name='uuid') THEN
        ALTER TABLE compression_events RENAME COLUMN uuid TO user_id;
    END IF;
    
    -- user_identity table
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name='user_identity' AND column_name='uuid') THEN
        ALTER TABLE user_identity RENAME COLUMN uuid TO user_id;
    END IF;
END $$;