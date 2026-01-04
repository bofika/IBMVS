"""
Custom exceptions for the IBM Video Streaming Manager application.
"""


class IBMVideoStreamingError(Exception):
    """Base exception for IBM Video Streaming API errors."""
    pass


class AuthenticationError(IBMVideoStreamingError):
    """Raised when authentication fails."""
    pass


class NotFoundError(IBMVideoStreamingError):
    """Raised when a resource is not found (404)."""
    pass


class ValidationError(IBMVideoStreamingError):
    """Raised when input validation fails."""
    pass


class APIError(IBMVideoStreamingError):
    """Raised when the API returns an error."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

# Made with Bob
