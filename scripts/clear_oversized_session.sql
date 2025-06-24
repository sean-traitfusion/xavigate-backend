-- Clear oversized session memory for specific user/session
-- This will force a fresh start for the chat

-- Delete session memory entries for the problematic session
DELETE FROM session_memory 
WHERE session_id = '14784478-3091-7098-065d-6cd64d8b9988';

-- Optional: Clear interaction logs for this session if needed
-- DELETE FROM interaction_logs 
-- WHERE session_id = '14784478-3091-7098-065d-6cd64d8b9988'
-- AND created_at > NOW() - INTERVAL '1 hour';

-- Show remaining session memory
SELECT session_id, COUNT(*) as message_count, SUM(LENGTH(message)) as total_chars
FROM session_memory
WHERE session_id = '14784478-3091-7098-065d-6cd64d8b9988'
GROUP BY session_id;