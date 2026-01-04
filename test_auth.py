#!/usr/bin/env python3
"""
Test script to verify IBM Video Streaming OAuth 2.0 authentication.
"""
import requests
import keyring
import base64

# Service name for keyring
SERVICE_NAME = "IBM_Video_Streaming_Manager"
CLIENT_ID_USERNAME = "client_id"
CLIENT_SECRET_USERNAME = "client_secret"

# Get credentials from keyring
client_id = keyring.get_password(SERVICE_NAME, CLIENT_ID_USERNAME)
client_secret = keyring.get_password(SERVICE_NAME, CLIENT_SECRET_USERNAME)

print("=" * 60)
print("IBM Video Streaming OAuth 2.0 Authentication Test")
print("=" * 60)
print()

if not client_id or not client_secret:
    print("❌ ERROR: Credentials not found in keyring!")
    print(f"   Client ID found: {client_id is not None}")
    print(f"   Client Secret found: {client_secret is not None}")
    exit(1)

print(f"✓ Client ID: {client_id[:8]}...{client_id[-8:]}")
print(f"  Length: {len(client_id)} characters")
print()
print(f"✓ Client Secret: {client_secret[:8]}...{client_secret[-8:]}")
print(f"  Length: {len(client_secret)} characters")
print()

# Test the token endpoint
TOKEN_URL = "https://video.ibm.com/oauth2/token"

print(f"Testing token endpoint: {TOKEN_URL}")
print()

# Prepare request data
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'device_name': 'IBM Video Streaming Manager Test'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Create Basic Auth header manually to verify
auth_string = f"{client_id}:{client_secret}"
auth_bytes = auth_string.encode('ascii')
auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
print(f"Basic Auth header (first 20 chars): Basic {auth_b64[:20]}...")
print()

try:
    # Method 1: Using requests auth parameter (recommended)
    print("Method 1: Using requests auth parameter")
    response = requests.post(
        TOKEN_URL,
        data=data,
        headers=headers,
        auth=(client_id, client_secret),
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    
    if response.status_code == 200:
        token_data = response.json()
        print("✅ SUCCESS! Token obtained:")
        print(f"   Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
        print(f"   Token Type: {token_data.get('token_type', 'N/A')}")
        print(f"   Expires In: {token_data.get('expires_in', 'N/A')} seconds")
    else:
        print(f"❌ FAILED with status {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data}")
        except:
            print(f"   Response: {response.text}")
    
    print()
    print("=" * 60)
    
    # Method 2: Manual Basic Auth header
    print("Method 2: Manual Basic Auth header")
    headers_with_auth = headers.copy()
    headers_with_auth['Authorization'] = f'Basic {auth_b64}'
    
    response2 = requests.post(
        TOKEN_URL,
        data=data,
        headers=headers_with_auth,
        timeout=30
    )
    
    print(f"Status Code: {response2.status_code}")
    print(f"Response: {response2.text}")
    
    if response2.status_code == 200:
        print("✅ SUCCESS with manual header!")
    else:
        print(f"❌ FAILED with status {response2.status_code}")
    
except Exception as e:
    print(f"❌ Exception occurred: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)

# Made with Bob
