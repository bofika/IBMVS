#!/usr/bin/env python3
"""
Test script to see actual API response format.
"""
import requests
import sys
import getpass

print("=" * 70)
print("IBM Video Streaming API - Response Format Test")
print("=" * 70)
print()

# Get credentials
if len(sys.argv) >= 3:
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
else:
    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client Secret: ").strip()

print()
print("Step 1: Getting access token...")
print("-" * 70)

# Get access token
TOKEN_URL = "https://video.ibm.com/oauth2/token"
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'device_name': 'Test Device'
}

token_response = requests.post(TOKEN_URL, data=token_data, timeout=30)
print(f"Token Status: {token_response.status_code}")

if token_response.status_code != 200:
    print(f"❌ Failed to get token: {token_response.text}")
    exit(1)

token_json = token_response.json()
access_token = token_json['access_token']
print(f"✅ Access Token: {access_token[:20]}...")
print()

# Test channels endpoint
print("Step 2: Fetching channels...")
print("-" * 70)

API_BASE_URL = "https://api.video.ibm.com/v1"
CHANNELS_URL = f"{API_BASE_URL}/users/self/channels.json"

headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

params = {
    'p': 1,
    'pagesize': 10
}

print(f"URL: {CHANNELS_URL}")
print(f"Headers: {headers}")
print(f"Params: {params}")
print()

channels_response = requests.get(CHANNELS_URL, headers=headers, params=params, timeout=30)

print(f"Status Code: {channels_response.status_code}")
print(f"Content-Type: {channels_response.headers.get('Content-Type')}")
print()
print("Response Headers:")
for key, value in channels_response.headers.items():
    print(f"  {key}: {value}")
print()
print("Response Body:")
print("-" * 70)
print(channels_response.text)
print("-" * 70)
print()

# Try to parse as JSON
try:
    json_data = channels_response.json()
    print("✅ Response is valid JSON")
    print(f"Type: {type(json_data)}")
    print(f"Keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'Not a dict'}")
    print()
    print("Formatted JSON:")
    import json
    print(json.dumps(json_data, indent=2))
except Exception as e:
    print(f"❌ Failed to parse as JSON: {e}")

print()
print("=" * 70)

# Made with Bob
