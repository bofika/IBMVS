"""
Player configuration panel.
"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QFormLayout, QGroupBox, QCheckBox,
    QLineEdit, QTextEdit, QSpinBox, QColorDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ui.base_panel import BasePanel
from api.players import player_manager
from api.channels import channel_manager
from core.logger import get_logger

logger = get_logger(__name__)


class PlayersPanel(BasePanel):
    """Panel for configuring players."""
    
    def __init__(self):
        super().__init__("Player Configuration")
        self.current_channel_id = None
        self.current_settings = {}
    
    def setup_ui(self):
        """Setup the player configuration panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Player Configuration")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Channel selector
        channel_layout = QHBoxLayout()
        channel_layout.addWidget(QLabel("Channel:"))
        
        self.channel_combo = QComboBox()
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        self.load_channels()
        channel_layout.addWidget(self.channel_combo)
        channel_layout.addStretch()
        
        layout.addLayout(channel_layout)
        
        # Player settings form
        settings_group = QGroupBox("Player Settings")
        settings_layout = QFormLayout()
        
        # Autoplay
        self.autoplay_check = QCheckBox()
        settings_layout.addRow("Autoplay:", self.autoplay_check)
        
        # Controls
        self.controls_check = QCheckBox()
        self.controls_check.setChecked(True)
        settings_layout.addRow("Show Controls:", self.controls_check)
        
        # Responsive
        self.responsive_check = QCheckBox()
        self.responsive_check.setChecked(True)
        settings_layout.addRow("Responsive:", self.responsive_check)
        
        # Color scheme
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["dark", "light"])
        settings_layout.addRow("Color Scheme:", self.color_scheme_combo)
        
        # Primary color
        color_layout = QHBoxLayout()
        self.primary_color_input = QLineEdit()
        self.primary_color_input.setPlaceholderText("#007bff")
        color_layout.addWidget(self.primary_color_input)
        
        self.color_picker_btn = QPushButton("Pick Color")
        self.color_picker_btn.clicked.connect(self.pick_color)
        color_layout.addWidget(self.color_picker_btn)
        settings_layout.addRow("Primary Color:", color_layout)
        
        # Logo URL
        self.logo_url_input = QLineEdit()
        self.logo_url_input.setPlaceholderText("https://example.com/logo.png")
        settings_layout.addRow("Logo URL:", self.logo_url_input)
        
        # Logo position
        self.logo_position_combo = QComboBox()
        self.logo_position_combo.addItems([
            "top-left", "top-right", "bottom-left", "bottom-right"
        ])
        settings_layout.addRow("Logo Position:", self.logo_position_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Embed code section
        embed_group = QGroupBox("Embed Code")
        embed_layout = QVBoxLayout()
        
        embed_options_layout = QHBoxLayout()
        
        embed_options_layout.addWidget(QLabel("Width:"))
        self.embed_width_spin = QSpinBox()
        self.embed_width_spin.setRange(320, 1920)
        self.embed_width_spin.setValue(640)
        embed_options_layout.addWidget(self.embed_width_spin)
        
        embed_options_layout.addWidget(QLabel("Height:"))
        self.embed_height_spin = QSpinBox()
        self.embed_height_spin.setRange(180, 1080)
        self.embed_height_spin.setValue(360)
        embed_options_layout.addWidget(self.embed_height_spin)
        
        generate_embed_btn = QPushButton("Generate Embed Code")
        generate_embed_btn.clicked.connect(self.generate_embed_code)
        embed_options_layout.addWidget(generate_embed_btn)
        
        embed_options_layout.addStretch()
        embed_layout.addLayout(embed_options_layout)
        
        self.embed_code_text = QTextEdit()
        self.embed_code_text.setReadOnly(True)
        self.embed_code_text.setMaximumHeight(100)
        embed_layout.addWidget(self.embed_code_text)
        
        copy_embed_btn = QPushButton("Copy to Clipboard")
        copy_embed_btn.clicked.connect(self.copy_embed_code)
        embed_layout.addWidget(copy_embed_btn)
        
        embed_group.setLayout(embed_layout)
        layout.addWidget(embed_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_btn)
        
        preview_btn = QPushButton("Preview Player")
        preview_btn.clicked.connect(self.preview_player)
        button_layout.addWidget(preview_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Add stretch
        layout.addStretch()
    
    def load_channels(self):
        """Load channels into combo box."""
        try:
            response = channel_manager.list_channels()
            channels = response.get('channels', [])
            
            self.channel_combo.clear()
            for channel in channels:
                self.channel_combo.addItem(
                    channel.get('title', 'Untitled'),
                    channel.get('id')
                )
            
            if channels:
                self.current_channel_id = channels[0].get('id')
                self.load_player_settings()
        except Exception as e:
            self.show_error(f"Failed to load channels: {str(e)}")
    
    def on_channel_changed(self, index: int):
        """Handle channel selection change."""
        if index >= 0:
            self.current_channel_id = self.channel_combo.currentData()
            self.load_player_settings()
    
    def load_player_settings(self):
        """Load player settings for selected channel."""
        if not self.current_channel_id:
            return
        
        try:
            settings = player_manager.get_player_settings(self.current_channel_id)
            self.current_settings = settings
            
            # Update UI with settings
            self.autoplay_check.setChecked(settings.get('autoplay', False))
            self.controls_check.setChecked(settings.get('controls', True))
            self.responsive_check.setChecked(settings.get('responsive', True))
            
            color_scheme = settings.get('color_scheme', 'dark')
            index = self.color_scheme_combo.findText(color_scheme)
            if index >= 0:
                self.color_scheme_combo.setCurrentIndex(index)
            
            primary_color = settings.get('primary_color', '')
            if primary_color:
                self.primary_color_input.setText(primary_color)
            
            logo_url = settings.get('logo_url', '')
            if logo_url:
                self.logo_url_input.setText(logo_url)
            
            logo_position = settings.get('logo_position', 'top-right')
            index = self.logo_position_combo.findText(logo_position)
            if index >= 0:
                self.logo_position_combo.setCurrentIndex(index)
            
            logger.info(f"Loaded player settings for channel {self.current_channel_id}")
            
        except Exception as e:
            self.show_error(f"Failed to load player settings: {str(e)}")
    
    def pick_color(self):
        """Open color picker dialog."""
        current_color = self.primary_color_input.text() or "#007bff"
        color = QColorDialog.getColor(QColor(current_color), self, "Select Primary Color")
        
        if color.isValid():
            self.primary_color_input.setText(color.name())
    
    def save_settings(self):
        """Save player settings."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        try:
            settings = {
                'autoplay': self.autoplay_check.isChecked(),
                'controls': self.controls_check.isChecked(),
                'responsive': self.responsive_check.isChecked(),
                'color_scheme': self.color_scheme_combo.currentText(),
            }
            
            primary_color = self.primary_color_input.text().strip()
            if primary_color:
                settings['primary_color'] = primary_color
            
            logo_url = self.logo_url_input.text().strip()
            if logo_url:
                settings['logo_url'] = logo_url
                settings['logo_position'] = self.logo_position_combo.currentText()
            
            player_manager.update_player_settings(
                self.current_channel_id,
                **settings
            )
            
            self.show_success("Player settings saved successfully")
            logger.info(f"Saved player settings for channel {self.current_channel_id}")
            
        except Exception as e:
            self.show_error(f"Failed to save settings: {str(e)}")
    
    def reset_settings(self):
        """Reset player settings to defaults."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        try:
            player_manager.reset_player_settings(self.current_channel_id)
            self.show_success("Player settings reset to defaults")
            self.load_player_settings()
        except Exception as e:
            self.show_error(f"Failed to reset settings: {str(e)}")
    
    def generate_embed_code(self):
        """Generate embed code."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        try:
            width = self.embed_width_spin.value()
            height = self.embed_height_spin.value()
            responsive = self.responsive_check.isChecked()
            
            embed_code = player_manager.get_embed_code(
                self.current_channel_id,
                width,
                height,
                responsive
            )
            
            self.embed_code_text.setPlainText(embed_code)
            logger.info(f"Generated embed code for channel {self.current_channel_id}")
            
        except Exception as e:
            self.show_error(f"Failed to generate embed code: {str(e)}")
    
    def copy_embed_code(self):
        """Copy embed code to clipboard."""
        from PyQt6.QtWidgets import QApplication
        
        embed_code = self.embed_code_text.toPlainText()
        if embed_code:
            QApplication.clipboard().setText(embed_code)
            self.show_success("Embed code copied to clipboard")
        else:
            self.show_info("No embed code to copy. Generate one first.")
    
    def preview_player(self):
        """Preview player in browser."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        preview_url = player_manager.preview_player(self.current_channel_id)
        
        import webbrowser
        webbrowser.open(preview_url)
        logger.info(f"Opened player preview: {preview_url}")
    
    def refresh(self):
        """Refresh player settings."""
        self.load_player_settings()

# Made with Bob
