"""
Input validation utilities.
"""
import os
import re
from typing import Optional, Tuple
from pathlib import Path
from utils.constants import (
    MAX_UPLOAD_SIZE,
    SUPPORTED_VIDEO_FORMATS,
    MAX_PAGE_SIZE
)


def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_channel_title(title: str) -> Tuple[bool, Optional[str]]:
    """
    Validate channel title.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Channel title cannot be empty"
    
    if len(title) < 3:
        return False, "Channel title must be at least 3 characters"
    
    if len(title) > 100:
        return False, "Channel title must be less than 100 characters"
    
    return True, None


def validate_video_title(title: str) -> Tuple[bool, Optional[str]]:
    """
    Validate video title.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Video title cannot be empty"
    
    if len(title) < 3:
        return False, "Video title must be at least 3 characters"
    
    if len(title) > 200:
        return False, "Video title must be less than 200 characters"
    
    return True, None


def validate_description(description: str, max_length: int = 5000) -> Tuple[bool, Optional[str]]:
    """
    Validate description text.
    
    Args:
        description: Description text
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(description) > max_length:
        return False, f"Description must be less than {max_length} characters"
    
    return True, None


def validate_video_file(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate video file for upload.
    
    Args:
        file_path: Path to video file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return False, "File does not exist"
    
    # Check if it's a file (not directory)
    if not path.is_file():
        return False, "Path is not a file"
    
    # Check file extension
    if path.suffix.lower() not in SUPPORTED_VIDEO_FORMATS:
        return False, f"Unsupported file format. Supported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}"
    
    # Check file size
    file_size = path.stat().st_size
    if file_size == 0:
        return False, "File is empty"
    
    if file_size > MAX_UPLOAD_SIZE:
        max_size_gb = MAX_UPLOAD_SIZE / (1024 ** 3)
        return False, f"File size exceeds maximum allowed size of {max_size_gb:.1f} GB"
    
    return True, None


def validate_page_number(page: int) -> Tuple[bool, Optional[str]]:
    """
    Validate page number for pagination.
    
    Args:
        page: Page number
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if page < 1:
        return False, "Page number must be at least 1"
    
    return True, None


def validate_page_size(page_size: int) -> Tuple[bool, Optional[str]]:
    """
    Validate page size for pagination.
    
    Args:
        page_size: Number of items per page
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if page_size < 1:
        return False, "Page size must be at least 1"
    
    if page_size > MAX_PAGE_SIZE:
        return False, f"Page size cannot exceed {MAX_PAGE_SIZE}"
    
    return True, None


def validate_color_hex(color: str) -> Tuple[bool, Optional[str]]:
    """
    Validate hex color code.
    
    Args:
        color: Hex color code (e.g., #FF0000)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    pattern = r'^#[0-9A-Fa-f]{6}$'
    if not re.match(pattern, color):
        return False, "Invalid hex color code. Format: #RRGGBB"
    
    return True, None


def validate_api_credentials(api_key: str, api_secret: str) -> Tuple[bool, Optional[str]]:
    """
    Validate API credentials.
    
    Args:
        api_key: API key
        api_secret: API secret
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not api_key or not api_key.strip():
        return False, "API key cannot be empty"
    
    if not api_secret or not api_secret.strip():
        return False, "API secret cannot be empty"
    
    if len(api_key) < 10:
        return False, "API key appears to be invalid"
    
    if len(api_secret) < 10:
        return False, "API secret appears to be invalid"
    
    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Ensure filename is not empty
    if not filename:
        filename = "untitled"
    
    return filename


def validate_poll_question(question: str) -> Tuple[bool, Optional[str]]:
    """
    Validate poll question.
    
    Args:
        question: Poll question text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Poll question cannot be empty"
    
    if len(question) < 5:
        return False, "Poll question must be at least 5 characters"
    
    if len(question) > 500:
        return False, "Poll question must be less than 500 characters"
    
    return True, None


def validate_poll_options(options: list) -> Tuple[bool, Optional[str]]:
    """
    Validate poll options.
    
    Args:
        options: List of poll option texts
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not options or len(options) < 2:
        return False, "Poll must have at least 2 options"
    
    if len(options) > 10:
        return False, "Poll cannot have more than 10 options"
    
    for i, option in enumerate(options):
        if not option or not option.strip():
            return False, f"Option {i + 1} cannot be empty"
        
        if len(option) > 200:
            return False, f"Option {i + 1} must be less than 200 characters"
    
    # Check for duplicate options
    if len(options) != len(set(opt.strip().lower() for opt in options)):
        return False, "Poll options must be unique"
    
    return True, None

# Made with Bob
