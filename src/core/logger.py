"""
Logging configuration and setup.
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from utils.constants import (
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_FILE_MAX_BYTES,
    LOG_FILE_BACKUP_COUNT
)
from utils.helpers import get_log_dir


class Logger:
    """Application logger manager."""
    
    _instance: Optional['Logger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            Logger._initialized = True
    
    def _setup_logging(self):
        """Set up logging configuration."""
        # Create formatters
        formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
        
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # File handler
        log_dir = get_log_dir()
        log_file = log_dir / 'app.log'
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Error file handler
        error_log_file = log_dir / 'error.log'
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name: Logger name (usually __name__)
            
        Returns:
            Logger instance
        """
        return logging.getLogger(name)
    
    @staticmethod
    def set_level(level: str):
        """
        Set logging level.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        numeric_level = getattr(logging, level.upper(), None)
        if isinstance(numeric_level, int):
            logging.getLogger().setLevel(numeric_level)


# Initialize logger on module import
Logger()


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return Logger.get_logger(name)

# Made with Bob
