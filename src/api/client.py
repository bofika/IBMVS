"""
Base API client for IBM Video Streaming API.
"""
import time
import requests
from typing import Any, Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.auth import auth_manager
from core.config import config
from core.logger import get_logger
from api.exceptions import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError,
    TimeoutError as APITimeoutError
)
from utils.constants import (
    API_TIMEOUT,
    API_RETRY_ATTEMPTS,
    API_RETRY_DELAY
)

logger = get_logger(__name__)


class IBMVideoClient:
    """Base client for IBM Video Streaming API."""
    
    def __init__(self):
        self.base_url = config.get_api_base_url()
        self.timeout = API_TIMEOUT
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry logic.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=API_RETRY_ATTEMPTS,
            backoff_factor=API_RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get request headers with authentication.
        
        Returns:
            Dictionary of headers
        """
        headers = auth_manager.get_auth_headers()
        
        if not headers:
            logger.warning("No authentication headers available")
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: Response object
            
        Returns:
            Response data as dictionary
            
        Raises:
            Various APIError subclasses based on status code
        """
        try:
            data = response.json() if response.content else {}
        except ValueError:
            data = {}
        
        # Handle error status codes
        if response.status_code == 401:
            logger.error("Authentication failed")
            raise AuthenticationError("Invalid or expired credentials")
        
        elif response.status_code == 403:
            logger.error("Authorization failed")
            raise AuthorizationError("Insufficient permissions")
        
        elif response.status_code == 404:
            logger.error(f"Resource not found: {response.url}")
            raise NotFoundError("Resource not found")
        
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            logger.warning(f"Rate limit exceeded. Retry after: {retry_after}")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None
            )
        
        elif response.status_code >= 500:
            logger.error(f"Server error: {response.status_code}")
            raise ServerError(f"Server error: {response.status_code}")
        
        elif not response.ok:
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            logger.error(f"API error: {error_msg}")
            raise APIError(error_msg, status_code=response.status_code, response=data)
        
        return data
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (relative to base URL)
            params: Query parameters
            json: JSON data
            data: Form data
            files: Files to upload
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data
            
        Raises:
            Various APIError subclasses
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        # Don't set Content-Type for file uploads
        if files and 'Content-Type' in headers:
            del headers['Content-Type']
        
        logger.debug(f"{method} {url}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                data=data,
                files=files,
                timeout=self.timeout,
                **kwargs
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {url}")
            raise APITimeoutError(f"Request timed out after {self.timeout} seconds")
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise NetworkError("Failed to connect to API server")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            raise APIError(f"Request failed: {str(e)}")
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a PUT request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a DELETE request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._request("DELETE", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a PATCH request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._request("PATCH", endpoint, **kwargs)
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.debug("API client session closed")


# Global client instance
client = IBMVideoClient()

# Made with Bob
