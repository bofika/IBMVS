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
    
    # Analytics API uses a different base URL
    ANALYTICS_BASE_URL = "https://analytics-api.video.ibm.com"
    
    def __init__(self):
        self.base_url = config.get_api_base_url()
        self.analytics_base_url = self.ANALYTICS_BASE_URL
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
            # Log detailed error information
            logger.error(f"API Error - Status: {response.status_code}")
            logger.error(f"API Error - URL: {response.url}")
            logger.error(f"API Error - Response: {response.text[:500]}")  # First 500 chars
            logger.error(f"API Error - Headers: {dict(response.headers)}")
            
            # Try to extract error message from various formats
            error_msg = 'Unknown error'
            if isinstance(data, dict):
                # Try different error message locations
                if 'error' in data:
                    if isinstance(data['error'], dict):
                        error_msg = data['error'].get('message', str(data['error']))
                    else:
                        error_msg = str(data['error'])
                elif 'message' in data:
                    error_msg = data['message']
                elif 'error_description' in data:
                    error_msg = data['error_description']
            
            logger.error(f"API error message: {error_msg}")
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
    
    def _get_analytics_headers(self) -> Dict[str, str]:
        """
        Get request headers for Analytics API with JWT authentication.
        
        Returns:
            Dictionary of headers with JWT token
        """
        headers = auth_manager.get_analytics_auth_headers()
        
        if not headers:
            logger.warning("No Analytics API authentication headers available")
        
        return headers
    
    def _analytics_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an Analytics API request with JWT authentication.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (relative to analytics base URL)
            params: Query parameters
            json: JSON data
            data: Form data
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data
            
        Raises:
            Various APIError subclasses
        """
        url = f"{self.analytics_base_url}{endpoint}"
        headers = self._get_analytics_headers()
        
        logger.debug(f"Analytics API {method} {url}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                data=data,
                timeout=self.timeout,
                **kwargs
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            logger.error(f"Analytics API request timeout: {url}")
            raise APITimeoutError(f"Request timed out after {self.timeout} seconds")
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Analytics API connection error: {e}")
            raise NetworkError("Failed to connect to Analytics API server")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Analytics API request error: {e}")
            raise APIError(f"Request failed: {str(e)}")
    
    def analytics_get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a GET request to Analytics API.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._analytics_request("GET", endpoint, **kwargs)
    
    def analytics_post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a POST request to Analytics API.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        return self._analytics_request("POST", endpoint, **kwargs)
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.debug("API client session closed")


# Global client instance
client = IBMVideoClient()

# Made with Bob
