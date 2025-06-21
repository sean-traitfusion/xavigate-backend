#!/bin/bash
# End-to-End Test Runner for Xavigate
# Usage: ./run_e2e_test.sh [JWT_TOKEN]

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Xavigate E2E Test Runner${NC}"
echo "================================"

# Check if JWT token is provided as argument
if [ -n "$1" ]; then
    export AUTH_TOKEN="$1"
    echo -e "${GREEN}✓ Using provided JWT token${NC}"
elif [ -n "$AUTH_TOKEN" ]; then
    echo -e "${GREEN}✓ Using AUTH_TOKEN from environment${NC}"
else
    if [ "$ENV" = "prod" ]; then
        echo -e "${RED}❌ Error: Production mode requires AUTH_TOKEN${NC}"
        echo "Usage: $0 <JWT_TOKEN>"
        echo "Or export AUTH_TOKEN='your-jwt-token'"
        exit 1
    else
        echo -e "${YELLOW}⚠️  Running in development mode (no auth required)${NC}"
    fi
fi

# Display current configuration
echo
echo "Configuration:"
echo "- ENV: ${ENV:-dev}"
echo "- API_BASE_URL: ${API_BASE_URL:-http://localhost:8080/api}"
echo "- AUTH_TOKEN: ${AUTH_TOKEN:0:20}..." 

# Check if services are running
echo
echo "Checking services..."

# Check individual services
services=("8015" "8011" "8017" "8012")
service_names=("Chat Service" "Storage Service" "Vector Service" "Stats Service")

all_running=true
for i in "${!services[@]}"; do
    port="${services[$i]}"
    name="${service_names[$i]}"
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/health" | grep -q "200\|404"; then
        echo -e "${GREEN}✓ $name (port $port) is running${NC}"
    else
        echo -e "${RED}✗ $name (port $port) is not responding${NC}"
        all_running=false
    fi
done

# Check NGINX separately (optional)
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/health" | grep -q "200\|404"; then
    echo -e "${GREEN}✓ NGINX/API Gateway (port 8080) is running${NC}"
    echo -e "${YELLOW}  Note: Using direct service URLs for testing${NC}"
else
    echo -e "${YELLOW}⚠️  NGINX/API Gateway (port 8080) is not running${NC}"
    echo -e "${YELLOW}  Using direct service URLs instead${NC}"
fi

if [ "$all_running" = false ]; then
    echo
    echo -e "${RED}❌ Some required services are not running. Please start them first:${NC}"
    echo "   docker compose up -d"
    exit 1
fi

# Run the test
echo
echo -e "${GREEN}Running E2E tests...${NC}"
echo

cd "$(dirname "$0")"
python3 test_e2e_production.py

echo
echo -e "${GREEN}✅ Test run complete!${NC}"