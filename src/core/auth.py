"""
Authentication and credential management for IBM Video Streaming API.
Uses OAuth 2.0 Client Credentials flow.
"""
import os
import keyring
import requests
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta

from core.logger import get_logger
from utils.constants import APP_NAME

logger = get_logger(__name__)


class AuthManager:
    """Manages OAuth 2.0 authentication for IBM Video Streaming API."""
    
    SERVICE_NAME = APP_NAME
    CLIENT_ID_USERNAME = "ibm_client_id"
    CLIENT_SECRET_USERNAME = "ibm_client_secret"
    
    # IBM Video Streaming OAuth endpoints
    AUTH_URL = "https://authentication.video.ibm.com/authorize"
    TOKEN_URL = "https://authentication.video.ibm.com/oauth2/token"
    API_BASE_URL = "https://api.video.ibm.com"
    
    def __init__(self):
        self._client_id: Optional[str] = None
        self._client_secret: Optional[str] = None
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        self._token_type: str = "Bearer"
        
        # Try to load credentials from environment or keyring
        self._load_credentials()
    
    def _load_credentials(self):
        """Load credentials from environment variables or keyring."""
        # Try environment variables first
        self._client_id = os.getenv('IBM_CLIENT_ID')
        self._client_secret = os.getenv('IBM_CLIENT_SECRET')
        
        # If not in environment, try keyring
        if not self._client_id:
            try:
                self._client_id = keyring.get_password(
                    self.SERVICE_NAME,
                    self.CLIENT_ID_USERNAME
                )
            except Exception as e:
                logger.debug(f"Could not load client ID from keyring: {e}")
        
        if not self._client_secret:
            try:
                self._client_secret = keyring.get_password(
                    self.SERVICE_NAME,
                    self.CLIENT_SECRET_USERNAME
                )
            except Exception as e:
                logger.debug(f"Could not load client secret from keyring: {e}")
        
        if self._client_id and self._client_secret:
            logger.info("Credentials loaded successfully")
        else:
            logger.info("No credentials found")
    
    def set_credentials(self, client_id: str, client_secret: str, save: bool = True) -> bool:
        """
        Set OAuth 2.0 client credentials.
        
        Args:
            client_id: IBM Video Streaming client ID (40-character string)
            client_secret: IBM Video Streaming client secret
            save: Whether to save credentials to keyring
            
        Returns:
            True if credentials were set successfully
        """
        try:
            self._client_id = client_id.strip()
            self._client_secret = client_secret.strip()
            
            if save:
                # Save to keyring
                keyring.set_password(
                    self.SERVICE_NAME,
                    self.CLIENT_ID_USERNAME,
                    self._client_id
                )
                keyring.set_password(
                    self.SERVICE_NAME,
                    self.CLIENT_SECRET_USERNAME,
                    self._client_secret
                )
                logger.info("Credentials saved to keyring")
            
            # Clear any existing token
            self._access_token = None
            self._token_expiry = None
            
            return True
        except Exception as e:
            logger.error(f"Failed to set credentials: {e}")
            return False
    
    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get OAuth 2.0 client credentials.
        
        Returns:
            Tuple of (client_id, client_secret)
        """
        return (self._client_id, self._client_secret)
    
    def has_credentials(self) -> bool:
        """
        Check if credentials are available.
        
        Returns:
            True if both client ID and secret are set
        """
        return bool(self._client_id and self._client_secret)
    
    def clear_credentials(self):
        """Clear stored credentials and tokens."""
        try:
            # Clear from keyring
            keyring.delete_password(self.SERVICE_NAME, self.CLIENT_ID_USERNAME)
            keyring.delete_password(self.SERVICE_NAME, self.CLIENT_SECRET_USERNAME)
        except Exception as e:
            logger.debug(f"Could not clear credentials from keyring: {e}")
        
        # Clear from memory
        self._client_id = None
        self._client_secret = None
        self._access_token = None
        self._token_expiry = None
        
        logger.info("Credentials cleared")
    
    def _request_access_token(self) -> bool:
        """
        Request a new access token using OAuth 2.0 Client Credentials flow.
        
        Returns:
            True if token was obtained successfully
        """
        if not self.has_credentials():
            logger.error("No credentials available for token request")
            return False
        
        try:
            logger.info("Requesting new access token...")
            
            # Prepare token request
            data = {
                'grant_type': 'client_credentials',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'device_name': 'IBM Video Streaming Manager'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Request token
            response = requests.post(
                self.TOKEN_URL,
                data=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self._access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)  # Default 1 hour
                self._token_type = token_data.get('token_type', 'Bearer')
                
                # Set expiry time (subtract 5 minutes for safety)
                self._token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
                
                logger.info(f"Access token obtained successfully (expires in {expires_in}s)")
                return True
            else:
                logger.error(f"Token request failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during token request: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during token request: {e}")
            return False
    
    def get_access_token(self) -> Optional[str]:
        """
        Get valid access token for API requests.
        Automatically requests new token if needed.
        
        Returns:
            Access token or None if unable to obtain
        """
        if not self.has_credentials():
            logger.warning("No credentials available")
            return None
        
        # Check if we need a new token
        if not self.is_token_valid():
            logger.debug("Token invalid or expired, requesting new token")
            if not self._request_access_token():
                logger.error("Failed to obtain access token")
                return None
        
        return self._access_token
    
    def is_token_valid(self) -> bool:
        """
        Check if current access token is valid and not expired.
        
        Returns:
            True if token is valid and not expired
        """
        if not self._access_token:
            logger.debug("No access token available")
            return False
        
        if self._token_expiry and datetime.now() >= self._token_expiry:
            logger.debug("Access token expired")
            return False
        
        return True
    
    def refresh_token(self) -> bool:
        """
        Force refresh of access token.
        
        Returns:
            True if token was refreshed successfully
        """
        logger.info("Forcing token refresh")
        self._access_token = None
        self._token_expiry = None
        return self._request_access_token()
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        Automatically handles token refresh if needed.
        
        Returns:
            Dictionary of headers with Authorization bearer token
        """
        token = self.get_access_token()
        if not token:
            logger.warning("No valid access token available for auth headers")
            return {}
        
        return {
            'Authorization': f'{self._token_type} {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test API connection with current credentials.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            token = self.get_access_token()
            if not token:
                return False, "Failed to obtain access token. Check your credentials."
            
            # Test with a simple API call (list channels)
            headers = self.get_auth_headers()
            response = requests.get(
                f"{self.API_BASE_URL}/channels.json",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Connection successful!"
            elif response.status_code == 401:
                return False, "Authentication failed. Invalid credentials."
            elif response.status_code == 403:
                return False, "Access forbidden. Check your API permissions."
            else:
                return False, f"API returned status code: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Connection timeout. Check your internet connection."
        except requests.exceptions.ConnectionError:
            return False, "Connection error. Check your internet connection."
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False, f"Connection test failed: {str(e)}"


# Global auth manager instance
auth_manager = AuthManager()

# Made with Bob
