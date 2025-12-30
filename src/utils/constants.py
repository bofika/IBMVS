"""
Application constants and configuration values.
"""

# Application Info
APP_NAME = "IBM Video Streaming Manager"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"
APP_ORGANIZATION = "Your Organization"

# API Configuration
API_BASE_URL = "https://api.video.ibm.com"
API_TIMEOUT = 30  # seconds
API_RATE_LIMIT = 100  # requests per minute
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 1  # seconds

# File Upload
MAX_UPLOAD_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB
CHUNK_SIZE = 1024 * 1024  # 1 MB chunks
SUPPORTED_VIDEO_FORMATS = [
    '.mp4', '.mov', '.avi', '.mkv', '.flv', 
    '.wmv', '.webm', '.m4v', '.mpg', '.mpeg'
]

# Cache Configuration
CACHE_TTL = 300  # 5 minutes
CACHE_MAX_SIZE = 100  # Maximum cached items

# UI Configuration
DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 1024
MIN_WINDOW_HEIGHT = 600

# Themes
THEME_DARK = "dark"
THEME_LIGHT = "light"
DEFAULT_THEME = THEME_DARK

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_FILE_BACKUP_COUNT = 5

# Status Values
STATUS_LIVE = "live"
STATUS_OFFLINE = "offline"
STATUS_RECORDED = "recorded"
STATUS_PROCESSING = "processing"
STATUS_READY = "ready"
STATUS_ERROR = "error"

# Player Configuration
PLAYER_AUTOPLAY_DEFAULT = False
PLAYER_CONTROLS_DEFAULT = True
PLAYER_RESPONSIVE_DEFAULT = True
PLAYER_COLOR_SCHEME_DEFAULT = "dark"

# Interactivity
CHAT_MODERATION_AUTO = "auto"
CHAT_MODERATION_MANUAL = "manual"
CHAT_MODERATION_OFF = "off"

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

# Monitoring
MONITOR_REFRESH_INTERVAL = 5000  # milliseconds
METRICS_HISTORY_POINTS = 60  # Keep last 60 data points

# Error Messages
ERROR_NETWORK = "Network error occurred. Please check your connection."
ERROR_AUTH = "Authentication failed. Please check your credentials."
ERROR_NOT_FOUND = "Resource not found."
ERROR_RATE_LIMIT = "Rate limit exceeded. Please try again later."
ERROR_SERVER = "Server error occurred. Please try again later."
ERROR_UPLOAD = "File upload failed. Please try again."
ERROR_INVALID_FILE = "Invalid file format or size."

# Made with Bob
