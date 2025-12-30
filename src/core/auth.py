"""
Authentication and credential management.
"""
import os
import keyring
from typing import Optional, Tuple
from datetime import datetime, timedelta

from core.logger import get_logger
from utils.constants import APP_NAME

logger = get_logger(__name__)


class AuthManager:
    """Manages authentication and API credentials."""
    
    SERVICE_NAME = APP_NAME
    API_KEY_USERNAME = "ibm_api_key"
    API_SECRET_USERNAME = "ibm_api_secret"
    
    def __init__(self):
        self._api_key: Optional[str] = None
        self._api_secret: Optional[str] = None
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        
        # Try to load credentials from environment or keyring
        self._load_credentials()
    
    def _load_credentials(self):
        """Load credentials from environment variables or keyring."""
        # Try environment variables first
        self._api_key = os.getenv('IBM_API_KEY')
        self._api_secret = os.getenv('IBM_API_SECRET')
        
        # If not in environment, try keyring
        if not self._api_key:
            try:
                self._api_key = keyring.get_password(
                    self.SERVICE_NAME, 
                    self.API_KEY_USERNAME
                )
            except Exception as e:
                logger.debug(f"Could not load API key from keyring: {e}")
        
        if not self._api_secret:
            try:
                self._api_secret = keyring.get_password(
                    self.SERVICE_NAME,
                    self.API_SECRET_USERNAME
                )
            except Exception as e:
                logger.debug(f"Could not load API secret from keyring: {e}")
        
        if self._api_key and self._api_secret:
            logger.info("Credentials loaded successfully")
        else:
            logger.info("No credentials found")
    
    def set_credentials(self, api_key: str, api_secret: str, save: bool = True) -> bool:
        """
        Set API credentials.
        
        Args:
            api_key: IBM Video Streaming API key
            api_secret: IBM Video Streaming API secret
            save: Whether to save credentials to keyring
            
        Returns:
            True if credentials were set successfully
        """
        try:
            self._api_key = api_key
            self._api_secret = api_secret
            
            if save:
                # Save to keyring
                keyring.set_password(
                    self.SERVICE_NAME,
                    self.API_KEY_USERNAME,
                    api_key
                )
                keyring.set_password(
                    self.SERVICE_NAME,
                    self.API_SECRET_USERNAME,
                    api_secret
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
        Get API credentials.
        
        Returns:
            Tuple of (api_key, api_secret)
        """
        return (self._api_key, self._api_secret)
    
    def has_credentials(self) -> bool:
        """
        Check if credentials are available.
        
        Returns:
            True if both API key and secret are set
        """
        return bool(self._api_key and self._api_secret)
    
    def clear_credentials(self):
        """Clear stored credentials."""
        try:
            # Clear from keyring
            keyring.delete_password(self.SERVICE_NAME, self.API_KEY_USERNAME)
            keyring.delete_password(self.SERVICE_NAME, self.API_SECRET_USERNAME)
        except Exception as e:
            logger.debug(f"Could not clear credentials from keyring: {e}")
        
        # Clear from memory
        self._api_key = None
        self._api_secret = None
        self._access_token = None
        self._token_expiry = None
        
        logger.info("Credentials cleared")
    
    def get_access_token(self) -> Optional[str]:
        """
        Get access token for API requests.
        
        For IBM Video Streaming API, we use the API key directly as the token.
        In a real OAuth implementation, this would handle token refresh.
        
        Returns:
            Access token or None
        """
        if not self.has_credentials():
            logger.warning("No credentials available")
            return None
        
        # For IBM Video Streaming API, we use the API key as the bearer token
        # In a real implementation, you would exchange credentials for an OAuth token
        return self._api_key
    
    def is_token_valid(self) -> bool:
        """
        Check if access token is valid.
        
        Returns:
            True if token is valid and not expired
        """
        if not self._access_token:
            return False
        
        if self._token_expiry and datetime.now() >= self._token_expiry:
            logger.debug("Access token expired")
            return False
        
        return True
    
    def refresh_token(self) -> bool:
        """
        Refresh access token.
        
        Returns:
            True if token was refreshed successfully
        """
        # For IBM Video Streaming API, we don't need to refresh
        # The API key is used directly
        return self.has_credentials()
    
    def get_auth_headers(self) -> dict:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary of headers
        """
        token = self.get_access_token()
        if not token:
            return {}
        
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }


# Global auth manager instance
auth_manager = AuthManager()

# Made with Bob
