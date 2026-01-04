"""
Videos management panel.
"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel,
    QComboBox, QFileDialog, QProgressDialog, QDialog,
    QFormLayout, QTextEdit, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from ui.base_panel import BasePanel
from api.videos import video_manager
from api.channels import channel_manager
from core.logger import get_logger
from utils.helpers import format_file_size, format_duration

logger = get_logger(__name__)


class VideoUploadThread(QThread):
    """Thread for uploading videos."""
    
    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(dict)  # video data
    error = pyqtSignal(str)  # error message
    
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


class VideoUploadDialog(QDialog):
    """Dialog for uploading videos."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Upload Video")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.file_path = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        
        # Channel selection
        self.channel_combo = QComboBox()
        self.load_channels()
        form.addRow("Channel:", self.channel_combo)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        file_layout.addWidget(self.file_label)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        form.addRow("Video File:", file_layout)
        
        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter video title")
        form.addRow("Title:", self.title_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter video description (optional)")
        self.description_input.setMaximumHeight(100)
        form.addRow("Description:", self.description_input)
        
        # Tags
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter tags separated by commas")
        form.addRow("Tags:", self.tags_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.start_upload)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_channels(self):
        """Load channels into combo box."""
        try:
            response = channel_manager.list_channels()
            channels = response.get('channels', [])
            
            for channel in channels:
                self.channel_combo.addItem(
                    channel.get('title', 'Untitled'),
                    channel.get('id')
                )
        except Exception as e:
            logger.error(f"Failed to load channels: {e}")
    
    def browse_file(self):
        """Browse for video file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.mov *.avi *.mkv *.flv *.wmv *.webm);;All Files (*)"
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path.split('/')[-1])
            
            # Auto-fill title if empty
            if not self.title_input.text():
                filename = file_path.split('/')[-1]
                title = filename.rsplit('.', 1)[0]
                self.title_input.setText(title)
    
    def start_upload(self):
        """Start the upload process."""
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please select a video file.")
            return
        
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "No Title", "Please enter a video title.")
            return
        
        if self.channel_combo.currentIndex() < 0:
            QMessageBox.warning(self, "No Channel", "Please select a channel.")
            return
        
        self.accept()
    
    def get_upload_data(self):
        """Get upload data."""
        tags = [tag.strip() for tag in self.tags_input.text().split(',') if tag.strip()]
        
        return {
            'channel_id': self.channel_combo.currentData(),
            'file_path': self.file_path,
            'title': self.title_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'tags': tags
        }


class VideosPanel(BasePanel):
    """Panel for managing videos."""
    
    def __init__(self):
        super().__init__("Videos")
        self.current_channel_id = None
    
    def setup_ui(self):
        """Setup the videos panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Video Management")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        # Channel selector
        toolbar.addWidget(QLabel("Channel:"))
        self.channel_combo = QComboBox()
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        self.load_channels()
        toolbar.addWidget(self.channel_combo)
        
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
        
        # Videos table
        self.videos_table = QTableWidget()
        self.videos_table.setColumnCount(6)
        self.videos_table.setHorizontalHeaderLabels([
            "ID", "Title", "Duration", "Views", "Status", "Actions"
        ])
        self.videos_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.videos_table)
    
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
                self.load_videos()
        except Exception as e:
            self.show_error(f"Failed to load channels: {str(e)}")
    
    def on_channel_changed(self, index: int):
        """Handle channel selection change."""
        if index >= 0:
            self.current_channel_id = self.channel_combo.currentData()
            self.load_videos()
    
    def load_videos(self):
        """Load videos for selected channel."""
        if not self.current_channel_id:
            return
        
        if not hasattr(self, 'videos_table'):
            logger.warning("Videos table not initialized yet")
            return
        
        try:
            response = video_manager.list_videos(self.current_channel_id)
            videos = response.get('videos', [])
            
            self.videos_table.setRowCount(len(videos))
            
            for row, video in enumerate(videos):
                video_id = video.get('id', '')
                self.videos_table.setItem(row, 0, QTableWidgetItem(video_id))
                self.videos_table.setItem(row, 1, QTableWidgetItem(video.get('title', 'Untitled')))
                
                # Handle duration - API returns 'length' as STRING
                length_str = video.get('length', '0')
                try:
                    duration = float(length_str) if length_str else 0
                    if duration > 0:
                        self.videos_table.setItem(row, 2, QTableWidgetItem(format_duration(int(duration))))
                    else:
                        self.videos_table.setItem(row, 2, QTableWidgetItem("0:00"))
                except (ValueError, TypeError):
                    self.videos_table.setItem(row, 2, QTableWidgetItem("N/A"))
                
                # Handle views
                views = video.get('views', 0)
                self.videos_table.setItem(row, 3, QTableWidgetItem(str(views)))
                
                # Handle status - API returns 'protect' field (public/private)
                protect = video.get('protect', 'unknown')
                self.videos_table.setItem(row, 4, QTableWidgetItem(protect))
                
                # Actions buttons
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, vid=video_id: self.edit_video(vid))
                self.videos_table.setCellWidget(row, 5, edit_btn)
            
            logger.info(f"Loaded {len(videos)} videos for channel {self.current_channel_id}")
            
        except Exception as e:
            logger.error(f"Failed to load videos: {str(e)}")
            self.show_error(f"Failed to load videos: {str(e)}")
    
    def search_videos(self, text: str):
        """Search videos."""
        if not hasattr(self, 'videos_table'):
            return
        
        for row in range(self.videos_table.rowCount()):
            title_item = self.videos_table.item(row, 1)
            if title_item:
                should_show = text.lower() in title_item.text().lower()
                self.videos_table.setRowHidden(row, not should_show)
    
    def edit_video(self, video_id: str):
        """Edit a video."""
        # TODO: Show edit video dialog
        self.show_info(f"Edit video dialog for video {video_id} - To be implemented")
        logger.info(f"Edit video requested: {video_id}")
    
    def upload_video(self):
        """Upload a new video."""
        dialog = VideoUploadDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            upload_data = dialog.get_upload_data()
            self.perform_upload(upload_data)
    
    def perform_upload(self, upload_data: dict):
        """Perform the actual upload."""
        progress = QProgressDialog("Uploading video...", "Cancel", 0, 100, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        
        # Create upload thread
        self.upload_thread = VideoUploadThread(
            upload_data['channel_id'],
            upload_data['file_path'],
            upload_data['title'],
            upload_data['description'],
            upload_data['tags']
        )
        
        self.upload_thread.finished.connect(lambda result: self.on_upload_finished(result, progress))
        self.upload_thread.error.connect(lambda error: self.on_upload_error(error, progress))
        
        self.upload_thread.start()
        progress.exec()
    
    def on_upload_finished(self, result: dict, progress: QProgressDialog):
        """Handle upload completion."""
        progress.close()
        self.show_success(f"Video uploaded successfully: {result.get('title', 'Untitled')}")
        self.refresh()
    
    def on_upload_error(self, error: str, progress: QProgressDialog):
        """Handle upload error."""
        progress.close()
        self.show_error(f"Upload failed: {error}")
    
    def refresh(self):
        """Refresh videos list."""
        self.load_videos()

# Made with Bob
