#!/usr/bin/env python3
"""
Script to clear old credentials from system keyring.
Run this before using the updated OAuth 2.0 authentication.
"""
import keyring
import sys

APP_NAME = "IBM Video Manager"

def clear_old_credentials():
    """Clear old API key/secret credentials."""
    print("🔧 Clearing old credentials from system keyring...")
    print(f"   Service: {APP_NAME}")
    
    # Old credential keys
    old_keys = [
        "ibm_api_key",
        "ibm_api_secret",
        "ibm_client_id",
        "ibm_client_secret"
    ]
    
    cleared = []
    for key in old_keys:
        try:
            # Try to get the credential
            value = keyring.get_password(APP_NAME, key)
            if value:
                # Delete it
                keyring.delete_password(APP_NAME, key)
                cleared.append(key)
                print(f"   ✓ Cleared: {key}")
        except keyring.errors.PasswordDeleteError:
            # Already deleted or doesn't exist
            pass
        except Exception as e:
            print(f"   ⚠ Could not clear {key}: {e}")
    
    if cleared:
        print(f"\n✅ Successfully cleared {len(cleared)} credential(s)")
        print("\nYou can now enter your new OAuth 2.0 credentials in the app:")
        print("1. Run: python3 src/main.py")
        print("2. Go to Settings")
        print("3. Click 'Configure Credentials'")
        print("4. Enter your Client ID (40 characters) and Client Secret")
    else:
        print("\n✓ No old credentials found in keyring")
    
    return len(cleared) > 0

if __name__ == "__main__":
    print("=" * 60)
    print("IBM Video Streaming Manager - Credential Cleanup")
    print("=" * 60)
    print()
    
    try:
        cleared = clear_old_credentials()
        sys.exit(0 if cleared else 0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

# Made with Bob
