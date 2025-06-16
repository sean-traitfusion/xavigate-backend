#!/bin/bash
# Helper script to test with Cognito token

echo "🔐 Xavigate Memory Test with Authentication"
echo "=========================================="
echo ""
echo "Please paste your Cognito token (from browser DevTools):"
echo "(The token will not be displayed for security)"
echo ""
read -s COGNITO_TOKEN

if [ -z "$COGNITO_TOKEN" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

echo "✅ Token received. Running tests..."
echo ""

# Export the token and run the test
export COGNITO_TOKEN
source .venv/bin/activate
python scripts/test_memory_simple.py