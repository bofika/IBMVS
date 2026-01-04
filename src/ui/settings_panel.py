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
    """Dialog for entering OAuth 2.0 client credentials."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("OAuth 2.0 Credentials")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(
            "Enter your IBM Video Streaming OAuth 2.0 credentials.\n\n"
            "To obtain credentials:\n"
            "1. Log in to your IBM Video Streaming account\n"
            "2. Go to Dashboard → API/Channel Settings\n"
            "3. Create new OAuth 2.0 client credentials\n"
            "4. Copy the Client ID (40-character string) and Client Secret"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Form
        form = QFormLayout()
        
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Enter Client ID (40 characters)")
        form.addRow("Client ID:", self.client_id_input)
        
        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Enter Client Secret")
        self.client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Client Secret:", self.client_secret_input)
        
        layout.addLayout(form)
        
        # Test connection button
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        layout.addWidget(self.test_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_credentials)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def test_connection(self):
        """Test the connection with provided credentials."""
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()
        
        if not client_id or not client_secret:
            self.status_label.setText("⚠️ Please enter both Client ID and Client Secret")
            self.status_label.setStyleSheet("color: orange;")
            return
        
        self.status_label.setText("Testing connection...")
        self.status_label.setStyleSheet("color: blue;")
        self.test_btn.setEnabled(False)
        
        # Temporarily set credentials
        auth_manager.set_credentials(client_id, client_secret, save=False)
        
        # Test connection
        success, message = auth_manager.test_connection()
        
        if success:
            self.status_label.setText(f"✓ {message}")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText(f"✗ {message}")
            self.status_label.setStyleSheet("color: red;")
        
        self.test_btn.setEnabled(True)
    
    def save_credentials(self):
        """Save credentials and close dialog."""
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()
        
        if not client_id or not client_secret:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Both Client ID and Client Secret are required."
            )
            return
        
        # Validate client ID length (should be 40 characters)
        if len(client_id) != 40:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Invalid Client ID",
                "Client ID should be exactly 40 characters long.\n"
                "Please check your credentials."
            )
            return
        
        if auth_manager.set_credentials(client_id, client_secret, save=True):
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
        
        # OAuth 2.0 Credentials Group
        credentials_group = QGroupBox("OAuth 2.0 Credentials")
        credentials_layout = QVBoxLayout()
        
        if auth_manager.has_credentials():
            status_label = QLabel("✓ Credentials configured")
            status_label.setStyleSheet("color: green; font-weight: bold;")
            
            # Show client ID (partially masked)
            client_id, _ = auth_manager.get_credentials()
            if client_id:
                masked_id = client_id[:8] + "..." + client_id[-8:]
                id_label = QLabel(f"Client ID: {masked_id}")
                id_label.setStyleSheet("color: gray; font-size: 10px;")
                credentials_layout.addWidget(id_label)
        else:
            status_label = QLabel("✗ No credentials configured")
            status_label.setStyleSheet("color: red; font-weight: bold;")
        
        credentials_layout.addWidget(status_label)
        
        change_credentials_btn = QPushButton("Configure Credentials")
        change_credentials_btn.clicked.connect(self.change_credentials)
        credentials_layout.addWidget(change_credentials_btn)
        
        test_connection_btn = QPushButton("Test Connection")
        test_connection_btn.clicked.connect(self.test_connection)
        test_connection_btn.setEnabled(auth_manager.has_credentials())
        credentials_layout.addWidget(test_connection_btn)
        
        clear_credentials_btn = QPushButton("Clear Credentials")
        clear_credentials_btn.clicked.connect(self.clear_credentials)
        clear_credentials_btn.setEnabled(auth_manager.has_credentials())
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
            self.show_success("Credentials saved successfully!")
            # Clear the layout and rebuild
            while self.layout().count():
                child = self.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.setup_ui()  # Refresh UI
    
    def test_connection(self):
        """Test API connection."""
        from PyQt6.QtWidgets import QMessageBox
        
        success, message = auth_manager.test_connection()
        
        if success:
            QMessageBox.information(
                self,
                "Connection Test",
                f"✓ {message}"
            )
        else:
            QMessageBox.warning(
                self,
                "Connection Test",
                f"✗ {message}"
            )
    
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
            # Clear the layout and rebuild
            while self.layout().count():
                child = self.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.setup_ui()  # Refresh UI

# Made with Bob
