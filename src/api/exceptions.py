"""
Custom exceptions for API operations.
"""
from typing import Optional, Dict, Any


class APIError(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None,
                 response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Exception raised for authentication failures."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(APIError):
    """Exception raised for authorization failures."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class NotFoundError(APIError):
    """Exception raised when resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class RateLimitError(APIError):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class ValidationError(APIError):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str = "Validation failed", errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400)
        self.errors = errors or {}


class NetworkError(APIError):
    """Exception raised for network-related errors."""
    
    def __init__(self, message: str = "Network error occurred"):
        super().__init__(message)


class ServerError(APIError):
    """Exception raised for server errors."""
    
    def __init__(self, message: str = "Server error occurred"):
        super().__init__(message, status_code=500)


class UploadError(APIError):
    """Exception raised for upload failures."""
    
    def __init__(self, message: str = "Upload failed"):
        super().__init__(message)


class TimeoutError(APIError):
    """Exception raised when request times out."""
    
    def __init__(self, message: str = "Request timed out"):
        super().__init__(message)

# Made with Bob
