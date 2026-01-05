"""
Video table model for QTableView.
"""
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor
from utils.helpers import format_duration


class VideoTableModel(QAbstractTableModel):
    """Table model for displaying videos."""
    
    # Column indices
    COL_ID = 0
    COL_TITLE = 1
    COL_DURATION = 2
    COL_VIEWS = 3
    COL_STATUS = 4
    COL_EDIT = 5
    COL_TOGGLE = 6
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._videos = []
        self._headers = ["ID", "Title", "Duration", "Views", "Status", "Edit", "Toggle Status"]
    
    def rowCount(self, parent=QModelIndex()):
        """Return number of rows."""
        if parent.isValid():
            return 0
        return len(self._videos)
    
    def columnCount(self, parent=QModelIndex()):
        """Return number of columns."""
        if parent.isValid():
            return 0
        return len(self._headers)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Return data for the given index and role."""
        if not index.isValid():
            return None
        
        if index.row() >= len(self._videos) or index.row() < 0:
            return None
        
        video = self._videos[index.row()]
        column = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.COL_ID:
                return str(video.get('id', ''))
            elif column == self.COL_TITLE:
                return video.get('title', 'Untitled')
            elif column == self.COL_DURATION:
                length_str = video.get('length', '0')
                try:
                    duration = float(length_str) if length_str else 0
                    return format_duration(int(duration)) if duration > 0 else "0:00"
                except (ValueError, TypeError):
                    return "N/A"
            elif column == self.COL_VIEWS:
                return str(video.get('views', 0))
            elif column == self.COL_STATUS:
                protect = video.get('protect', 'unknown')
                is_public = (protect == 'public')
                return "Public" if is_public else "Private" if protect == 'private' else protect
            elif column == self.COL_EDIT:
                return "Edit"
            elif column == self.COL_TOGGLE:
                protect = video.get('protect', 'unknown')
                is_public = (protect == 'public')
                return "Make Private" if is_public else "Make Public"
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if column in [self.COL_VIEWS, self.COL_DURATION]:
                return Qt.AlignmentFlag.AlignCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        
        elif role == Qt.ItemDataRole.BackgroundRole:
            # Alternate row colors for better readability
            if index.row() % 2 == 0:
                return QColor(45, 45, 45)
            return QColor(35, 35, 35)
        
        elif role == Qt.ItemDataRole.ForegroundRole:
            if column == self.COL_STATUS:
                protect = video.get('protect', 'unknown')
                if protect == 'public':
                    return QColor(100, 200, 100)  # Green for public
                elif protect == 'private':
                    return QColor(200, 100, 100)  # Red for private
            return QColor(255, 255, 255)
        
        elif role == Qt.ItemDataRole.UserRole:
            # Store the full video data
            return video
        
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """Return header data."""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if 0 <= section < len(self._headers):
                    return self._headers[section]
        return None
    
    def setVideos(self, videos):
        """Set the videos data and refresh the view."""
        self.beginResetModel()
        self._videos = videos
        self.endResetModel()
    
    def getVideo(self, row):
        """Get video data for a specific row."""
        if 0 <= row < len(self._videos):
            return self._videos[row]
        return None
    
    def updateVideo(self, row, video_data):
        """Update a specific video's data."""
        if 0 <= row < len(self._videos):
            self._videos[row] = video_data
            # Emit dataChanged for the entire row
            left_index = self.index(row, 0)
            right_index = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(left_index, right_index)
    
    def clear(self):
        """Clear all videos."""
        self.beginResetModel()
        self._videos = []
        self.endResetModel()

# Made with Bob
