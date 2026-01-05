"""
IBM Video Streaming Manager - Main Application Entry Point
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from core.logger import get_logger
from core.config import config
from ui.main_window import MainWindow
from utils.constants import APP_NAME, APP_VERSION

logger = get_logger(__name__)


def main():
    """Main application entry point."""
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("IBM Video Manager")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    try:
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        
        # Run application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
