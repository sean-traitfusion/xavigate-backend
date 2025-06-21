#!/usr/bin/env python3
"""Decode JWT token to extract Cognito configuration"""
import json
import base64
import os

token = os.getenv("AUTH_TOKEN", "")
if not token:
    print("No AUTH_TOKEN found")
    exit(1)

# Split token
parts = token.split('.')
if len(parts) != 3:
    print("Invalid JWT format")
    exit(1)

# Decode header and payload (add padding if needed)
def decode_part(part):
    # Add padding if needed
    padding = 4 - len(part) % 4
    if padding != 4:
        part += '=' * padding
    return json.loads(base64.urlsafe_b64decode(part))

header = decode_part(parts[0])
payload = decode_part(parts[1])

print("JWT Token Analysis:")
print("=" * 60)
print("\nHeader:")
print(json.dumps(header, indent=2))
print("\nPayload:")
print(json.dumps(payload, indent=2))

# Extract Cognito configuration
iss = payload.get('iss', '')
if 'cognito-idp' in iss:
    # Parse issuer URL: https://cognito-idp.{region}.amazonaws.com/{user_pool_id}
    parts = iss.split('/')
    region_part = parts[2].split('.')[1]  # Extract region from cognito-idp.{region}.amazonaws.com
    user_pool_id = parts[-1]
    
    print("\n" + "=" * 60)
    print("Extracted Cognito Configuration:")
    print(f"COGNITO_REGION={region_part}")
    print(f"COGNITO_USER_POOL_ID={user_pool_id}")
    print(f"COGNITO_APP_CLIENT_ID={payload.get('client_id', '')}")
    
    print("\nAdd these to your .env file!")