"""
Custom delegate for video table buttons.
"""
from PySide6.QtWidgets import QStyledItemDelegate, QPushButton, QStyleOptionButton, QStyle, QApplication
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter


class ButtonDelegate(QStyledItemDelegate):
    """Delegate for rendering buttons in table cells."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._clicked_row = -1
        self._clicked_column = -1
    
    def paint(self, painter, option, index):
        """Paint the button."""
        if index.column() in [5, 6]:  # Edit and Toggle columns
            # Create button style
            button_option = QStyleOptionButton()
            button_option.rect = option.rect.adjusted(2, 2, -2, -2)
            button_option.text = index.data(Qt.ItemDataRole.DisplayRole)
            button_option.state = QStyle.StateFlag.State_Enabled
            
            # Highlight on hover
            if option.state & QStyle.StateFlag.State_MouseOver:
                button_option.state |= QStyle.StateFlag.State_MouseOver
            
            # Draw the button
            QApplication.style().drawControl(
                QStyle.ControlElement.CE_PushButton,
                button_option,
                painter
            )
        else:
            super().paint(painter, option, index)
    
    def editorEvent(self, event, model, option, index):
        """Handle mouse events for button clicks."""
        if index.column() in [5, 6]:  # Edit and Toggle columns
            if event.type() == event.Type.MouseButtonRelease:
                if option.rect.contains(event.pos()):
                    self._clicked_row = index.row()
                    self._clicked_column = index.column()
                    return True
        return super().editorEvent(event, model, option, index)
    
    def getClickedCell(self):
        """Get the last clicked cell and reset."""
        row = self._clicked_row
        col = self._clicked_column
        self._clicked_row = -1
        self._clicked_column = -1
        return row, col

# Made with Bob
