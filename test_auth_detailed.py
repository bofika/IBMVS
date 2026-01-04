#!/usr/bin/env python3
"""
Detailed authentication test with multiple methods.
Usage: python3 test_auth_detailed.py [client_id] [client_secret]
"""
import requests
import base64
import sys
import getpass

print("=" * 70)
print("IBM Video Streaming - Detailed Authentication Test")
print("=" * 70)
print()

# Get credentials from command line or prompt
if len(sys.argv) >= 3:
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    print("Using credentials from command line arguments")
else:
    print("Enter your IBM Video Streaming OAuth credentials:")
    print("(You can also pass them as: python3 test_auth_detailed.py CLIENT_ID CLIENT_SECRET)")
    print()
    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client Secret: ").strip()

if not client_id or not client_secret:
    print("❌ Both Client ID and Client Secret are required")
    exit(1)

print()
print(f"Client ID: {client_id[:10]}...{client_id[-10:]}")
print(f"Client ID length: {len(client_id)} characters")
print(f"Client Secret: {client_secret[:10]}...{client_secret[-10:]}")
print(f"Client Secret length: {len(client_secret)} characters")
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
        token_data = response1.json()
        print(f"Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
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
        token_data = response2.json()
        print(f"Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
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
        token_data = response3.json()
        print(f"Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
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
        token_data = response4.json()
        print(f"Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
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
        token_data = response5.json()
        print(f"Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
    else:
        print("❌ FAILED")
except Exception as e:
    print(f"❌ Exception: {e}")

print()
print("=" * 70)
print("Test Complete")
print("=" * 70)
print()
print("If all tests failed, please verify:")
print("1. Credentials are from video.ibm.com dashboard (not IBM Cloud)")
print("2. API access is enabled for your account")
print("3. Credentials haven't been revoked")
print("4. You're using the correct credentials (not viewer auth)")

# Made with Bob
