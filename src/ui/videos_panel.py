"""
Videos management panel with QTableView and Model/View architecture.
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
    QHeaderView, QLineEdit, QLabel, QComboBox, QFileDialog, 
    QProgressDialog, QDialog, QFormLayout, QTextEdit, 
    QDialogButtonBox, QMessageBox, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer

from ui.base_panel import BasePanel
from ui.video_table_model import VideoTableModel
from ui.video_table_delegate import ButtonDelegate
from api.videos import video_manager
from api.channels import channel_manager
from core.logger import get_logger

logger = get_logger(__name__)


class VideoUploadThread(QThread):
    """Thread for uploading videos."""
    
    progress = Signal(int, int)  # current, total
    finished = Signal(dict)  # video data
    error = Signal(str)  # error message
    
    def __init__(self, channel_id: str, file_path: str, title: str, 
                 description: str, tags: list):
        super().__init__()
        self.channel_id = channel_id
        self.file_path = file_path
        self.title = title
        self.description = description
        self.tags = tags
    
    def run(self):
        """Run the upload."""
        try:
            result = video_manager.upload_video(
                self.channel_id,
                self.file_path,
                self.title,
                self.description,
                self.tags
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ChannelSelectorDialog(QDialog):
    """Dialog for selecting a channel with search functionality."""
    
    def __init__(self, channels: list, current_channel_id: str = None, parent=None):
        super().__init__(parent)
        self.channels = channels
        self.selected_channel = None
        self.current_channel_id = current_channel_id
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI."""
        self.setWindowTitle("Select Channel")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout(self)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to filter channels...")
        self.search_input.textChanged.connect(self.filter_channels)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Channel list
        self.channel_list = QListWidget()
        self.channel_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.channel_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self.accept)
        select_btn.setDefault(True)
        button_layout.addWidget(select_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Populate list
        self.populate_channels()
    
    def populate_channels(self):
        """Populate the channel list."""
        self.channel_list.clear()
        for channel in self.channels:
            item = QListWidgetItem(channel.get('title', 'Untitled'))
            item.setData(Qt.ItemDataRole.UserRole, channel)
            self.channel_list.addItem(item)
            
            # Select current channel
            if self.current_channel_id and channel.get('id') == self.current_channel_id:
                item.setSelected(True)
                self.channel_list.scrollToItem(item)
    
    def filter_channels(self, text: str):
        """Filter channels based on search text."""
        for i in range(self.channel_list.count()):
            item = self.channel_list.item(i)
            channel = item.data(Qt.ItemDataRole.UserRole)
            title = channel.get('title', '').lower()
            item.setHidden(text.lower() not in title)
    
    def on_item_double_clicked(self, item):
        """Handle double click on item."""
        self.accept()
    
    def get_selected_channel(self):
        """Get the selected channel."""
        items = self.channel_list.selectedItems()
        if items:
            return items[0].data(Qt.ItemDataRole.UserRole)
        return None


class VideosPanel(BasePanel):
    """Panel for managing videos using Model/View architecture."""
    
    def __init__(self):
        super().__init__("Videos")
        self.current_channel_id = None
        self.current_page = 1
        self.total_pages = 1
        self.page_size = 50
    
    def setup_ui(self):
        """Setup the videos panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Video Management")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        # Channel selector button
        toolbar.addWidget(QLabel("Channel:"))
        self.channel_button = QPushButton("Select Channel...")
        self.channel_button.setMinimumWidth(300)
        self.channel_button.setMinimumHeight(30)
        self.channel_button.clicked.connect(self.show_channel_selector)
        self.channel_button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px 10px;
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        toolbar.addWidget(self.channel_button)
        
        # Store channels list
        self.channels_list = []
        self.load_channels()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search videos...")
        self.search_input.textChanged.connect(self.search_videos)
        toolbar.addWidget(self.search_input)
        
        self.upload_btn = QPushButton("Upload Video")
        self.upload_btn.clicked.connect(self.upload_video)
        toolbar.addWidget(self.upload_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(self.refresh_btn)
        
        layout.addLayout(toolbar)
        
        # Pagination controls
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(QLabel("Videos per page:"))
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["50", "100", "200"])
        self.page_size_combo.setCurrentText("50")
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        # Fix dropdown visibility on macOS
        self.page_size_combo.setStyleSheet("""
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #3a3a3a;
                border: 1px solid #555;
            }
        """)
        pagination_layout.addWidget(self.page_size_combo)
        
        pagination_layout.addStretch()
        
        self.prev_page_btn = QPushButton("◀ Previous")
        self.prev_page_btn.clicked.connect(self.load_previous_page)
        self.prev_page_btn.setEnabled(False)
        pagination_layout.addWidget(self.prev_page_btn)
        
        self.page_label = QLabel("Page 1")
        pagination_layout.addWidget(self.page_label)
        
        self.next_page_btn = QPushButton("Next ▶")
        self.next_page_btn.clicked.connect(self.load_next_page)
        self.next_page_btn.setEnabled(False)
        pagination_layout.addWidget(self.next_page_btn)
        
        layout.addLayout(pagination_layout)
        
        # Videos table with Model/View
        self.video_model = VideoTableModel(self)
        self.videos_table = QTableView()
        self.videos_table.setModel(self.video_model)
        
        # Set up delegate for buttons
        self.button_delegate = ButtonDelegate(self)
        self.videos_table.setItemDelegateForColumn(5, self.button_delegate)  # Edit column
        self.videos_table.setItemDelegateForColumn(6, self.button_delegate)  # Toggle column
        
        # Configure table
        self.videos_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.videos_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.videos_table.setAlternatingRowColors(True)
        self.videos_table.setSortingEnabled(False)
        self.videos_table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.videos_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Title column stretches
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Duration
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Views
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Edit button
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Toggle button
        self.videos_table.setColumnWidth(5, 80)
        self.videos_table.setColumnWidth(6, 120)
        
        # Connect click events
        self.videos_table.clicked.connect(self.on_table_clicked)
        
        layout.addWidget(self.videos_table)
    
    def on_table_clicked(self, index):
        """Handle table cell clicks."""
        row, col = self.button_delegate.getClickedCell()
        if row >= 0:
            video = self.video_model.getVideo(row)
            if video:
                video_id = video.get('id', '')
                if col == 5:  # Edit column
                    self.edit_video(video_id)
                elif col == 6:  # Toggle column
                    protect = video.get('protect', 'unknown')
                    is_public = (protect == 'public')
                    self.toggle_video_status(video_id, is_public)
    
    def load_channels(self):
        """Load channels list."""
        try:
            response = channel_manager.list_channels()
            self.channels_list = response.get('channels', [])
            
            logger.info(f"Loaded {len(self.channels_list)} channels")
            
            # Set button text if we have a current channel
            if hasattr(self, 'current_channel_id') and self.current_channel_id:
                for channel in self.channels_list:
                    if channel.get('id') == self.current_channel_id:
                        self.channel_button.setText(channel.get('title', 'Unknown Channel'))
                        break
        except Exception as e:
            logger.error(f"Failed to load channels: {e}")
            self.show_error(f"Failed to load channels: {str(e)}")
    
    def show_channel_selector(self):
        """Show channel selector dialog."""
        if not self.channels_list:
            self.show_error("No channels available")
            return
        
        dialog = ChannelSelectorDialog(self.channels_list, self.current_channel_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_channel = dialog.get_selected_channel()
            if selected_channel:
                self.current_channel_id = selected_channel.get('id')
                self.channel_button.setText(selected_channel.get('title', 'Unknown Channel'))
                logger.info(f"Channel changed to: {selected_channel.get('title')} (ID: {self.current_channel_id})")
                self.load_videos(1)
    
    def load_videos(self, page: int = 1):
        """Load videos for the current channel."""
        if not self.current_channel_id:
            self.show_info("Please select a channel first")
            return
        
        try:
            logger.info(f"Fetching videos for channel {self.current_channel_id} (page {page}, include_private=True)")
            
            response = video_manager.list_videos(
                self.current_channel_id,
                page=page,
                page_size=self.page_size,
                include_private=True
            )
            
            # Debug: Log the response structure
            logger.debug(f"API Response keys: {response.keys()}")
            
            videos = response.get('videos', [])
            paging = response.get('paging', {})
            
            # Debug: Log paging info
            logger.debug(f"Paging info: {paging}")
            logger.debug(f"Number of videos: {len(videos)}")
            
            # Update pagination
            self.current_page = page
            total_videos = paging.get('total', len(videos))
            self.total_pages = max(1, (total_videos + self.page_size - 1) // self.page_size)
            
            self.page_label.setText(f"Page {self.current_page} of {self.total_pages} ({total_videos} videos)")
            self.prev_page_btn.setEnabled(self.current_page > 1)
            self.next_page_btn.setEnabled(self.current_page < self.total_pages)
            
            # Update model - this will automatically refresh the view
            self.video_model.setVideos(videos)
            
            # Force view update
            self.videos_table.viewport().update()
            self.videos_table.update()
            
            logger.info(f"Loaded {len(videos)} videos for channel {self.current_channel_id} (page {page}/{self.total_pages})")
            
        except Exception as e:
            logger.error(f"Failed to load videos: {str(e)}")
            self.show_error(f"Failed to load videos: {str(e)}")
    
    def load_previous_page(self):
        """Load previous page of videos."""
        if self.current_page > 1:
            self.load_videos(self.current_page - 1)
    
    def load_next_page(self):
        """Load next page of videos."""
        if self.current_page < self.total_pages:
            self.load_videos(self.current_page + 1)
    
    def on_page_size_changed(self, size_text: str):
        """Handle page size change."""
        self.page_size = int(size_text)
        self.load_videos(1)  # Reset to first page
    
    def search_videos(self, text: str):
        """Search videos (filter rows)."""
        # TODO: Implement proxy model for filtering
        pass
    
    def edit_video(self, video_id: str):
        """Edit a video."""
        self.show_info(f"Edit video dialog for video {video_id} - To be implemented")
        logger.info(f"Edit video requested: {video_id}")
    
    def toggle_video_status(self, video_id: str, is_currently_public: bool):
        """Toggle video between public and private."""
        try:
            # Set to private if currently public, and vice versa
            make_private = is_currently_public
            status_text = "private" if make_private else "public"
            
            logger.info(f"Toggling video {video_id} to {status_text}")
            video_manager.set_video_protection(video_id, make_private)
            
            self.show_success(f"Video status changed to {status_text}")
            
            # Reload current page after a short delay
            QTimer.singleShot(1000, lambda: self.load_videos(self.current_page))
            
        except Exception as e:
            logger.error(f"Failed to toggle video status: {str(e)}")
            self.show_error(f"Failed to toggle video status: {str(e)}")
    
    def upload_video(self):
        """Upload a video."""
        self.show_info("Upload video dialog - To be implemented")
        logger.info("Upload video requested")
    
    def refresh(self):
        """Refresh the current view."""
        if self.current_channel_id:
            self.load_videos(self.current_page)
        else:
            self.load_channels()

# Made with Bob
