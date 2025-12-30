"""
Helper utility functions.
"""
import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 GB")
    """
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "1:23:45")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_number(number: int) -> str:
    """
    Format number with thousand separators.
    
    Args:
        number: Number to format
        
    Returns:
        Formatted number string (e.g., "1,234,567")
    """
    return f"{number:,}"


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%dT%H:%M:%SZ") -> Optional[datetime]:
    """
    Parse datetime string to datetime object.
    
    Args:
        dt_str: Datetime string
        format_str: Format string
        
    Returns:
        Datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(dt_str, format_str)
    except (ValueError, TypeError):
        return None


def time_ago(dt: datetime) -> str:
    """
    Get human-readable time difference from now.
    
    Args:
        dt: Datetime object
        
    Returns:
        Time ago string (e.g., "2 hours ago")
    """
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"


def get_app_data_dir() -> Path:
    """
    Get application data directory path.
    
    Returns:
        Path to application data directory
    """
    if os.name == 'nt':  # Windows
        base_dir = Path(os.environ.get('APPDATA', ''))
    elif os.name == 'posix':  # macOS/Linux
        if 'darwin' in sys.platform:  # macOS
            base_dir = Path.home() / 'Library' / 'Application Support'
        else:  # Linux
            base_dir = Path.home() / '.local' / 'share'
    else:
        base_dir = Path.home()
    
    app_dir = base_dir / 'IBM Video Manager'
    app_dir.mkdir(parents=True, exist_ok=True)
    
    return app_dir


def get_log_dir() -> Path:
    """
    Get logs directory path.
    
    Returns:
        Path to logs directory
    """
    log_dir = get_app_data_dir() / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_cache_dir() -> Path:
    """
    Get cache directory path.
    
    Returns:
        Path to cache directory
    """
    cache_dir = get_app_data_dir() / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_config_file() -> Path:
    """
    Get configuration file path.
    
    Returns:
        Path to configuration file
    """
    return get_app_data_dir() / 'config.json'


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def safe_get(dictionary: Dict[str, Any], *keys, default=None) -> Any:
    """
    Safely get nested dictionary value.
    
    Args:
        dictionary: Dictionary to search
        *keys: Keys to traverse
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default
    return result


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage.
    
    Args:
        part: Part value
        total: Total value
        
    Returns:
        Percentage (0-100)
    """
    if total == 0:
        return 0.0
    return (part / total) * 100


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def generate_embed_code(channel_id: str, width: int = 640, height: int = 360, 
                       responsive: bool = True) -> str:
    """
    Generate HTML embed code for a channel.
    
    Args:
        channel_id: Channel ID
        width: Player width
        height: Player height
        responsive: Whether to make player responsive
        
    Returns:
        HTML embed code
    """
    if responsive:
        return f'''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="https://video.ibm.com/embed/{channel_id}" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" allowfullscreen>
    </iframe>
</div>'''
    else:
        return f'''<iframe src="https://video.ibm.com/embed/{channel_id}" 
        width="{width}" height="{height}" 
        frameborder="0" allowfullscreen>
</iframe>'''


def extract_channel_id_from_url(url: str) -> Optional[str]:
    """
    Extract channel ID from IBM Video Streaming URL.
    
    Args:
        url: Channel URL
        
    Returns:
        Channel ID or None
    """
    import re
    pattern = r'video\.ibm\.com/channel/(\d+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Made with Bob
