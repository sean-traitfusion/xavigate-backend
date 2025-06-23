#!/bin/bash
# Test script to verify all services are working

echo "Testing Xavigate Services..."
echo "============================"

# Base URL - adjust if needed
BASE_URL="http://localhost"

# Test each service health endpoint
echo -e "\n1. Testing Storage Service..."
curl -s -o /dev/null -w "Storage Service: %{http_code}\n" $BASE_URL/api/storage/health

echo -e "\n2. Testing Vector Service..."
curl -s -o /dev/null -w "Vector Service: %{http_code}\n" $BASE_URL/api/vector/health

echo -e "\n3. Testing Auth Service..."
curl -s -o /dev/null -w "Auth Service: %{http_code}\n" $BASE_URL/api/auth/health

echo -e "\n4. Testing Chat Service..."
curl -s -o /dev/null -w "Chat Service: %{http_code}\n" $BASE_URL/api/chat/health

echo -e "\n5. Testing Stats Service..."
curl -s -o /dev/null -w "Stats Service: %{http_code}\n" $BASE_URL/api/stats/health

echo -e "\n6. Checking Docker containers..."
docker ps --format "table {{.Names}}\t{{.Status}}" | grep xavigate

echo -e "\n7. Checking for recent errors in storage service..."
docker logs xavigate_storage_service --tail 20 | grep -i error || echo "No recent errors found"

echo -e "\nDone!"