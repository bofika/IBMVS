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
    # Based on official documentation: https://developers.video.ibm.com/api-basics-authentication
    AUTH_URL = "https://authentication.video.ibm.com/authorize"
    TOKEN_URL = "https://video.ibm.com/oauth2/token"
    API_BASE_URL = "https://api.video.ibm.com"
    
    def __init__(self):
        self._client_id: Optional[str] = None
        self._client_secret: Optional[str] = None
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        self._token_type: str = "Bearer"
        
        # JWT token for Analytics API
        self._jwt_token: Optional[str] = None
        self._jwt_token_expiry: Optional[datetime] = None
        
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
            logger.info("=" * 60)
            logger.info("Requesting new OAuth 2.0 access token...")
            logger.info(f"Token URL: {self.TOKEN_URL}")
            
            # Verify credentials are not None first
            if not self._client_id or not self._client_secret:
                logger.error("=" * 60)
                logger.error("✗ Client credentials are missing!")
                logger.error(f"  Client ID is None: {self._client_id is None}")
                logger.error(f"  Client Secret is None: {self._client_secret is None}")
                logger.error("=" * 60)
                raise ValueError("Client credentials are not set")
            
            logger.info(f"Client ID: {self._client_id[:8]}...{self._client_id[-8:]}")
            logger.info(f"Client ID length: {len(self._client_id)}")
            logger.info(f"Client Secret length: {len(self._client_secret)}")
            
            # Prepare token request data
            # NOTE: Despite IBM's documentation suggesting HTTP Basic Auth,
            # the actual working method is to send client_secret in POST data
            data = {
                'grant_type': 'client_credentials',
                'client_id': self._client_id,
                'client_secret': self._client_secret,  # Send in POST data, not Basic Auth
                'device_name': 'IBM Video Streaming Manager'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            logger.debug(f"Request data keys: {list(data.keys())}")
            logger.info("Sending client_secret in POST data (not Basic Auth)")
            
            # Request token
            logger.info("Sending token request...")
            response = requests.post(
                self.TOKEN_URL,
                data=data,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                token_data = response.json()
                self._access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)  # Default 1 hour
                self._token_type = token_data.get('token_type', 'Bearer')
                
                # Set expiry time (subtract 5 minutes for safety)
                self._token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
                
                logger.info(f"✓ Access token obtained successfully!")
                logger.info(f"  Token type: {self._token_type}")
                logger.info(f"  Expires in: {expires_in} seconds")
                logger.info(f"  Token preview: {self._access_token[:20]}..." if self._access_token else "  No token received")
                logger.info("=" * 60)
                return True
            else:
                logger.error("=" * 60)
                logger.error(f"✗ Token request FAILED!")
                logger.error(f"  Status code: {response.status_code}")
                logger.error(f"  Response body: {response.text}")
                logger.error("=" * 60)
                
                # Try to parse error details
                try:
                    error_data = response.json()
                    logger.error(f"  Error details: {error_data}")
                except:
                    pass
                
                return False
                
        except requests.exceptions.Timeout:
            logger.error("Token request timed out after 30 seconds")
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error during token request: {e}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during token request: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during token request: {e}", exc_info=True)
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
    
    def _request_jwt_token(self) -> bool:
        """
        Request a JWT token for Analytics API.
        
        The Analytics API requires JWT tokens instead of standard OAuth tokens.
        This is obtained by setting token_type=jwt as a POST parameter.
        
        Returns:
            True if JWT token was obtained successfully
        """
        if not self.has_credentials():
            logger.error("No credentials available for JWT token request")
            return False
        
        try:
            logger.info("=" * 60)
            logger.info("Requesting JWT token for Analytics API...")
            logger.info(f"Token URL: {self.TOKEN_URL}")
            
            if not self._client_id or not self._client_secret:
                logger.error("Client credentials are missing!")
                return False
            
            logger.info(f"Client ID: {self._client_id[:8]}...{self._client_id[-8:]}")
            
            # Request JWT token with token_type=jwt parameter
            # This MUST be sent as POST form data, not JSON
            data = {
                'grant_type': 'client_credentials',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'token_type': 'jwt',  # This is the key difference for Analytics API
                'device_name': 'IBM Video Streaming Manager - Analytics'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            logger.info("Requesting JWT token (token_type=jwt)...")
            response = requests.post(
                self.TOKEN_URL,
                data=data,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                self._jwt_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)
                
                # Set expiry time (subtract 5 minutes for safety)
                self._jwt_token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
                
                logger.info(f"✓ JWT token obtained successfully!")
                logger.info(f"  Expires in: {expires_in} seconds")
                logger.info(f"  Token preview: {self._jwt_token[:20]}..." if self._jwt_token else "  No token received")
                logger.info("=" * 60)
                return True
            else:
                logger.error("=" * 60)
                logger.error(f"✗ JWT token request FAILED!")
                logger.error(f"  Status code: {response.status_code}")
                logger.error(f"  Response body: {response.text}")
                logger.error("=" * 60)
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error during JWT token request: {e}", exc_info=True)
            return False
    
    def get_jwt_token(self) -> Optional[str]:
        """
        Get valid JWT token for Analytics API requests.
        Automatically requests new token if needed.
        
        Returns:
            JWT token or None if unable to obtain
        """
        if not self.has_credentials():
            logger.warning("No credentials available for JWT token")
            return None
        
        # Check if we need a new JWT token
        if not self.is_jwt_token_valid():
            logger.debug("JWT token invalid or expired, requesting new token")
            if not self._request_jwt_token():
                logger.error("Failed to obtain JWT token")
                return None
        
        return self._jwt_token
    
    def is_jwt_token_valid(self) -> bool:
        """
        Check if current JWT token is valid and not expired.
        
        Returns:
            True if JWT token is valid and not expired
        """
        if not self._jwt_token:
            logger.debug("No JWT token available")
            return False
        
        if self._jwt_token_expiry and datetime.now() >= self._jwt_token_expiry:
            logger.debug("JWT token expired")
            return False
        
        return True
    
    def refresh_jwt_token(self) -> bool:
        """
        Force refresh of JWT token.
        
        Returns:
            True if JWT token was refreshed successfully
        """
        logger.info("Forcing JWT token refresh")
        self._jwt_token = None
        self._jwt_token_expiry = None
        return self._request_jwt_token()
    
    def get_analytics_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for Analytics API requests.
        Uses JWT token instead of standard OAuth token.
        
        Note: IBM Analytics API requires the JWT token WITHOUT the "Bearer" prefix.
        The Authorization header should contain just the token itself.
        
        Returns:
            Dictionary of headers with JWT Authorization token (no Bearer prefix)
        """
        jwt_token = self.get_jwt_token()
        if not jwt_token:
            logger.warning("No valid JWT token available for Analytics API")
            return {}
        
        # IBM Analytics API requires JWT token WITHOUT "Bearer" prefix
        # Format: Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...
        return {
            'Authorization': jwt_token,  # No "Bearer" prefix for Analytics API
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
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
