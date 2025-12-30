"""
Settings and preferences panel.
"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QGroupBox, QDialog, QDialogButtonBox, QLabel
)

from ui.base_panel import BasePanel
from core.auth import auth_manager
from core.config import config
from core.logger import get_logger

logger = get_logger(__name__)


class CredentialsDialog(QDialog):
    """Dialog for entering API credentials."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Credentials")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(
            "Enter your IBM Video Streaming API credentials.\n"
            "You can find these in your IBM Video Streaming account settings."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Form
        form = QFormLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter API Key")
        form.addRow("API Key:", self.api_key_input)
        
        self.api_secret_input = QLineEdit()
        self.api_secret_input.setPlaceholderText("Enter API Secret")
        self.api_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("API Secret:", self.api_secret_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_credentials)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def save_credentials(self):
        """Save credentials and close dialog."""
        api_key = self.api_key_input.text().strip()
        api_secret = self.api_secret_input.text().strip()
        
        if not api_key or not api_secret:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Both API Key and API Secret are required."
            )
            return
        
        if auth_manager.set_credentials(api_key, api_secret, save=True):
            self.accept()
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Error",
                "Failed to save credentials."
            )


class SettingsPanel(BasePanel):
    """Panel for application settings."""
    
    def __init__(self):
        super().__init__("Settings")
    
    def setup_ui(self):
        """Setup settings panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Application Settings")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # API Credentials Group
        credentials_group = QGroupBox("API Credentials")
        credentials_layout = QVBoxLayout()
        
        if auth_manager.has_credentials():
            status_label = QLabel("✓ Credentials configured")
            status_label.setStyleSheet("color: green;")
        else:
            status_label = QLabel("✗ No credentials configured")
            status_label.setStyleSheet("color: red;")
        
        credentials_layout.addWidget(status_label)
        
        change_credentials_btn = QPushButton("Change Credentials")
        change_credentials_btn.clicked.connect(self.change_credentials)
        credentials_layout.addWidget(change_credentials_btn)
        
        clear_credentials_btn = QPushButton("Clear Credentials")
        clear_credentials_btn.clicked.connect(self.clear_credentials)
        credentials_layout.addWidget(clear_credentials_btn)
        
        credentials_group.setLayout(credentials_layout)
        layout.addWidget(credentials_group)
        
        # Application Settings Group
        app_settings_group = QGroupBox("Application Settings")
        app_settings_layout = QFormLayout()
        
        # Theme selection would go here
        # Cache settings would go here
        # Log level settings would go here
        
        app_settings_group.setLayout(app_settings_layout)
        layout.addWidget(app_settings_group)
        
        # Add stretch
        layout.addStretch()
    
    def change_credentials(self):
        """Show dialog to change credentials."""
        dialog = CredentialsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.show_success("Credentials updated successfully")
            self.setup_ui()  # Refresh UI
    
    def clear_credentials(self):
        """Clear stored credentials."""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            "Clear Credentials",
            "Are you sure you want to clear stored credentials?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            auth_manager.clear_credentials()
            self.show_success("Credentials cleared")
            self.setup_ui()  # Refresh UI

# Made with Bob
