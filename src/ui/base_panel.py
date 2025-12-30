"""
Base panel class for all UI panels.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from core.logger import get_logger

logger = get_logger(__name__)


class BasePanel(QWidget):
    """Base class for all panels."""
    
    def __init__(self, title: str = "Panel"):
        super().__init__()
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the panel UI. Override in subclasses."""
        layout = QVBoxLayout(self)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Add stretch to push content to top
        layout.addStretch()
    
    def refresh(self):
        """Refresh panel data. Override in subclasses."""
        logger.debug(f"Refreshing {self.title} panel")
    
    def show_error(self, message: str):
        """
        Show error message.
        
        Args:
            message: Error message
        """
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", message)
        logger.error(f"{self.title} panel error: {message}")
    
    def show_info(self, message: str):
        """
        Show info message.
        
        Args:
            message: Info message
        """
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Information", message)
    
    def show_success(self, message: str):
        """
        Show success message.
        
        Args:
            message: Success message
        """
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Success", message)

# Made with Bob
