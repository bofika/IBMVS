"""
Configuration management for the application.
"""
import json
import os
from typing import Any, Optional, Dict
from pathlib import Path
from dotenv import load_dotenv

from utils.helpers import get_config_file, get_app_data_dir
from utils.constants import (
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_THEME,
    API_BASE_URL,
    CACHE_TTL
)
from core.logger import get_logger

logger = get_logger(__name__)


class Config:
    """Application configuration manager."""
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment."""
        # Load environment variables
        load_dotenv()
        
        # Load from config file
        config_file = get_config_file()
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    self._config = json.load(f)
                logger.info(f"Configuration loaded from {config_file}")
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
                self._config = {}
        else:
            logger.info("No configuration file found, using defaults")
            self._config = {}
        
        # Set defaults if not present
        self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values."""
        defaults = {
            'api': {
                'base_url': os.getenv('IBM_API_BASE_URL', API_BASE_URL),
                'timeout': 30,
                'retry_attempts': 3
            },
            'ui': {
                'theme': os.getenv('THEME', DEFAULT_THEME),
                'window_width': int(os.getenv('WINDOW_WIDTH', DEFAULT_WINDOW_WIDTH)),
                'window_height': int(os.getenv('WINDOW_HEIGHT', DEFAULT_WINDOW_HEIGHT)),
                'remember_window_state': True
            },
            'cache': {
                'enabled': True,
                'ttl': int(os.getenv('CACHE_TTL', CACHE_TTL))
            },
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO')
            },
            'upload': {
                'max_size': int(os.getenv('MAX_UPLOAD_SIZE', 5368709120)),
                'chunk_size': 1048576
            }
        }
        
        # Merge defaults with existing config
        for key, value in defaults.items():
            if key not in self._config:
                self._config[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in self._config[key]:
                        self._config[key][sub_key] = sub_value
    
    def save(self):
        """Save configuration to file."""
        config_file = get_config_file()
        try:
            with open(config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.info(f"Configuration saved to {config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'api.base_url')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        logger.debug(f"Configuration updated: {key} = {value}")
    
    def get_api_base_url(self) -> str:
        """Get API base URL."""
        return self.get('api.base_url', API_BASE_URL)
    
    def get_theme(self) -> str:
        """Get UI theme."""
        return self.get('ui.theme', DEFAULT_THEME)
    
    def set_theme(self, theme: str):
        """Set UI theme."""
        self.set('ui.theme', theme)
        self.save()
    
    def get_window_size(self) -> tuple:
        """Get window size."""
        width = self.get('ui.window_width', DEFAULT_WINDOW_WIDTH)
        height = self.get('ui.window_height', DEFAULT_WINDOW_HEIGHT)
        return (width, height)
    
    def set_window_size(self, width: int, height: int):
        """Set window size."""
        self.set('ui.window_width', width)
        self.set('ui.window_height', height)
        self.save()
    
    def get_window_position(self) -> Optional[tuple]:
        """Get window position."""
        x = self.get('ui.window_x')
        y = self.get('ui.window_y')
        if x is not None and y is not None:
            return (x, y)
        return None
    
    def set_window_position(self, x: int, y: int):
        """Set window position."""
        self.set('ui.window_x', x)
        self.set('ui.window_y', y)
        self.save()
    
    def is_cache_enabled(self) -> bool:
        """Check if cache is enabled."""
        return self.get('cache.enabled', True)
    
    def get_cache_ttl(self) -> int:
        """Get cache TTL in seconds."""
        return self.get('cache.ttl', CACHE_TTL)
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get('logging.level', 'INFO')
    
    def set_log_level(self, level: str):
        """Set logging level."""
        self.set('logging.level', level)
        self.save()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self._config = {}
        self._set_defaults()
        self.save()
        logger.info("Configuration reset to defaults")


# Global config instance
config = Config()

# Made with Bob
