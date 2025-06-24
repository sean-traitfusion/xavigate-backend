#!/bin/bash
# Script to clear oversized session and restart services

echo "Clearing oversized session memory..."
docker exec -it xavigate_postgres psql -U xavigate_user -d xavigate -c "DELETE FROM session_memory WHERE session_id = '14784478-3091-7098-065d-6cd64d8b9988' OR uuid = '14784478-3091-7098-065d-6cd64d8b9988';"

echo "Checking session memory size..."
docker exec -it xavigate_postgres psql -U xavigate_user -d xavigate -c "SELECT session_id, COUNT(*) as messages, SUM(LENGTH(message)) as total_chars FROM session_memory GROUP BY session_id ORDER BY total_chars DESC LIMIT 5;"

echo "Restarting services..."
docker-compose restart chat_service storage_service

echo "Waiting for services to be ready..."
sleep 10

echo "Services restarted. Please check the application."