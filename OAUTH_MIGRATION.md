# OAuth 2.0 Migration Guide

## ⚠️ Important: Clear Old Credentials First!

If you previously used this application with API Key/Secret authentication, you **MUST** clear the old credentials before using the new OAuth 2.0 authentication.

## Quick Fix

### Step 1: Clear Old Credentials

Run the cleanup script:

```bash
python3 clear_credentials.py
```

This will remove any old credentials stored in your system keyring.

### Step 2: Get New OAuth 2.0 Credentials

1. Log in to your IBM Video Streaming account
2. Go to **Dashboard** → **API/Channel Settings**
3. Create new **OAuth 2.0 client credentials**
4. You will receive:
   - **Client ID**: A 40-character string (e.g., `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`)
   - **Client Secret**: A secret key

### Step 3: Enter Credentials in App

```bash
python3 src/main.py
```

1. Go to **Settings** (⚙️ icon in sidebar)
2. Click **"Configure Credentials"**
3. Enter your **Client ID** (40 characters)
4. Enter your **Client Secret**
5. Click **"Test Connection"** to verify
6. Click **OK** to save

## What Changed?

### Before (Old Method)
- Used simple API Key + API Secret
- Direct authentication with each request
- Stored as: `IBM_API_KEY` and `IBM_API_SECRET`

### After (New Method - OAuth 2.0)
- Uses OAuth 2.0 Client Credentials flow
- Client ID + Client Secret → Access Token
- Access tokens expire after ~1 hour and are auto-refreshed
- Stored as: `IBM_CLIENT_ID` and `IBM_CLIENT_SECRET`

## Troubleshooting

### "Authentication failed" Error

**Cause**: Old credentials are still in keyring

**Solution**:
```bash
# Run the cleanup script
python3 clear_credentials.py

# Then restart the app and enter new credentials
python3 src/main.py
```

### "Invalid Client ID" Error

**Cause**: Client ID is not exactly 40 characters

**Solution**: 
- Double-check you copied the entire Client ID
- It should be exactly 40 characters long
- No spaces before or after

### "Token request failed: 401"

**Cause**: Invalid Client ID or Client Secret

**Solution**:
1. Go back to IBM Video Streaming Dashboard
2. Verify your credentials are correct
3. You may need to generate new credentials
4. Make sure you're using **OAuth 2.0** credentials, not API keys

### Manual Keyring Cleanup (macOS)

If the script doesn't work, you can manually clear credentials:

```bash
# Open Keychain Access app
open "/Applications/Utilities/Keychain Access.app"

# Search for: "IBM Video Manager"
# Delete all entries related to IBM Video Manager
```

### Check What's in Keyring

```python
import keyring

APP_NAME = "IBM Video Manager"

# Check for old credentials
print("Old API Key:", keyring.get_password(APP_NAME, "ibm_api_key"))
print("Old API Secret:", keyring.get_password(APP_NAME, "ibm_api_secret"))

# Check for new credentials
print("New Client ID:", keyring.get_password(APP_NAME, "ibm_client_id"))
print("New Client Secret:", keyring.get_password(APP_NAME, "ibm_client_secret"))
```

## Debug Mode

To see detailed OAuth token request logs:

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG

# Run the app
python3 src/main.py
```

Look for lines like:
```
Requesting new OAuth 2.0 access token...
Token URL: https://authentication.video.ibm.com/oauth2/token
Client ID: a1b2c3d4...s9t0
Response status code: 200
✓ Access token obtained successfully!
```

## Still Having Issues?

1. **Check the logs**: Look in `logs/app.log` for detailed error messages
2. **Verify credentials**: Make sure you're using OAuth 2.0 credentials, not API keys
3. **Test manually**: Try the credentials with curl:

```bash
curl -X POST https://authentication.video.ibm.com/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "device_name=Test"
```

If this returns a token, your credentials are valid.

## Environment Variables (Alternative)

Instead of using the UI, you can set credentials via environment variables:

```bash
export IBM_CLIENT_ID="your_40_character_client_id"
export IBM_CLIENT_SECRET="your_client_secret"

python3 src/main.py
```

---

**Last Updated**: 2026-01-04