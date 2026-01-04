#!/usr/bin/env python3
"""
Detailed authentication test with multiple methods.
"""
import requests
import keyring
import base64
import json

SERVICE_NAME = "IBM_Video_Streaming_Manager"
CLIENT_ID_USERNAME = "client_id"
CLIENT_SECRET_USERNAME = "client_secret"

client_id = keyring.get_password(SERVICE_NAME, CLIENT_ID_USERNAME)
client_secret = keyring.get_password(SERVICE_NAME, CLIENT_SECRET_USERNAME)

print("=" * 70)
print("IBM Video Streaming - Detailed Authentication Test")
print("=" * 70)
print()

if not client_id or not client_secret:
    print("❌ No credentials found in keyring")
    exit(1)

print(f"Client ID: {client_id[:10]}...{client_id[-10:]}")
print(f"Client Secret: {client_secret[:10]}...{client_secret[-10:]}")
print()

TOKEN_URL = "https://video.ibm.com/oauth2/token"

# Test 1: Standard approach with requests auth parameter
print("=" * 70)
print("TEST 1: Using requests auth parameter (current implementation)")
print("=" * 70)

data1 = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'device_name': 'Test Device'
}

headers1 = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    response1 = requests.post(
        TOKEN_URL,
        data=data1,
        headers=headers1,
        auth=(client_id, client_secret),
        timeout=30
    )
    print(f"Status: {response1.status_code}")
    print(f"Response: {response1.text}")
    if response1.status_code == 200:
        print("✅ SUCCESS!")
    else:
        print("❌ FAILED")
except Exception as e:
    print(f"❌ Exception: {e}")

print()

# Test 2: Manual Basic Auth header
print("=" * 70)
print("TEST 2: Manual Basic Auth header")
print("=" * 70)

auth_string = f"{client_id}:{client_secret}"
auth_b64 = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

data2 = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'device_name': 'Test Device'
}

headers2 = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {auth_b64}'
}

try:
    response2 = requests.post(
        TOKEN_URL,
        data=data2,
        headers=headers2,
        timeout=30
    )
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.text}")
    if response2.status_code == 200:
        print("✅ SUCCESS!")
    else:
        print("❌ FAILED")
except Exception as e:
    print(f"❌ Exception: {e}")

print()

# Test 3: Without client_id in POST data (only in Basic Auth)
print("=" * 70)
print("TEST 3: Client ID only in Basic Auth (not in POST data)")
print("=" * 70)

data3 = {
    'grant_type': 'client_credentials',
    'device_name': 'Test Device'
}

headers3 = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    response3 = requests.post(
        TOKEN_URL,
        data=data3,
        headers=headers3,
        auth=(client_id, client_secret),
        timeout=30
    )
    print(f"Status: {response3.status_code}")
    print(f"Response: {response3.text}")
    if response3.status_code == 200:
        print("✅ SUCCESS!")
    else:
        print("❌ FAILED")
except Exception as e:
    print(f"❌ Exception: {e}")

print()

# Test 4: Client secret in POST data instead of Basic Auth
print("=" * 70)
print("TEST 4: Client secret in POST data (no Basic Auth)")
print("=" * 70)

data4 = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'device_name': 'Test Device'
}

headers4 = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    response4 = requests.post(
        TOKEN_URL,
        data=data4,
        headers=headers4,
        timeout=30
    )
    print(f"Status: {response4.status_code}")
    print(f"Response: {response4.text}")
    if response4.status_code == 200:
        print("✅ SUCCESS!")
    else:
        print("❌ FAILED")
except Exception as e:
    print(f"❌ Exception: {e}")

print()

# Test 5: With scope parameter
print("=" * 70)
print("TEST 5: With 'broadcaster' scope")
print("=" * 70)

data5 = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'device_name': 'Test Device',
    'scope': 'broadcaster'
}

headers5 = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    response5 = requests.post(
        TOKEN_URL,
        data=data5,
        headers=headers5,
        auth=(client_id, client_secret),
        timeout=30
    )
    print(f"Status: {response5.status_code}")
    print(f"Response: {response5.text}")
    if response5.status_code == 200:
        print("✅ SUCCESS!")
    else:
        print("❌ FAILED")
except Exception as e:
    print(f"❌ Exception: {e}")

print()
print("=" * 70)
print("Test Complete")
print("=" * 70)

# Made with Bob
