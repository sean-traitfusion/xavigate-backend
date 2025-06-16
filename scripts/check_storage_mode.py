#!/usr/bin/env python3
"""Check which mode the storage service is running in"""
import requests

try:
    # Try to access the OpenAPI docs
    resp = requests.get("http://localhost:8011/openapi.json")
    if resp.status_code == 200:
        data = resp.json()
        # In prod mode, the root path includes /api/storage
        if data.get("servers", [{}])[0].get("url", "").endswith("/api/storage"):
            print("✅ Storage service is running in PROD mode")
            print("   - Database persistence enabled")
            print("   - Authentication required")
        else:
            print("✅ Storage service is running in DEV mode")
            print("   - In-memory storage")
            print("   - No authentication required")
    else:
        print("❌ Could not determine mode")
except Exception as e:
    print(f"❌ Storage service not responding: {e}")
    print("   Make sure it's running on port 8011")