"""
Channels management panel.
"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt

from ui.base_panel import BasePanel
from api.channels import channel_manager
from core.logger import get_logger

logger = get_logger(__name__)


class ChannelsPanel(BasePanel):
    """Panel for managing channels."""
    
    def __init__(self):
        super().__init__("Channels")
    
    def setup_ui(self):
        """Setup the channels panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Channel Management")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search channels...")
        self.search_input.textChanged.connect(self.search_channels)
        toolbar.addWidget(self.search_input)
        
        self.create_btn = QPushButton("Create Channel")
        self.create_btn.clicked.connect(self.create_channel)
        toolbar.addWidget(self.create_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(self.refresh_btn)
        
        layout.addLayout(toolbar)
        
        # Channels table
        self.channels_table = QTableWidget()
        self.channels_table.setColumnCount(5)
        self.channels_table.setHorizontalHeaderLabels([
            "ID", "Title", "Status", "Viewers", "Actions"
        ])
        self.channels_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.channels_table)
        
        # Load channels
        self.load_channels()
    
    def load_channels(self):
        """Load channels from API."""
        try:
            response = channel_manager.list_channels()
            channels = response.get('channels', [])
            
            self.channels_table.setRowCount(len(channels))
            
            for row, channel in enumerate(channels):
                channel_id = channel.get('id', '')
                self.channels_table.setItem(row, 0, QTableWidgetItem(channel_id))
                self.channels_table.setItem(row, 1, QTableWidgetItem(channel.get('title', '')))
                self.channels_table.setItem(row, 2, QTableWidgetItem(channel.get('status', '')))
                self.channels_table.setItem(row, 3, QTableWidgetItem(str(channel.get('viewer_count', 0))))
                
                # Actions buttons
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, cid=channel_id: self.edit_channel(cid))
                self.channels_table.setCellWidget(row, 4, edit_btn)
            
            logger.info(f"Loaded {len(channels)} channels")
            
        except Exception as e:
            self.show_error(f"Failed to load channels: {str(e)}")
    
    def edit_channel(self, channel_id: str):
        """Edit a channel."""
        # TODO: Show edit channel dialog
        self.show_info(f"Edit channel dialog for channel {channel_id} - To be implemented")
        logger.info(f"Edit channel requested: {channel_id}")
    
    def search_channels(self, text: str):
        """Search channels."""
        # Filter table rows based on search text
        for row in range(self.channels_table.rowCount()):
            title_item = self.channels_table.item(row, 1)
            if title_item:
                should_show = text.lower() in title_item.text().lower()
                self.channels_table.setRowHidden(row, not should_show)
    
    def create_channel(self):
        """Create a new channel."""
        # TODO: Show create channel dialog
        self.show_info("Create channel dialog - To be implemented")
    
    def refresh(self):
        """Refresh channels list."""
        self.load_channels()

# Made with Bob
