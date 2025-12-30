"""
Main application window.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QListWidget, QMenuBar, QStatusBar,
    QMessageBox, QLabel, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

from core.logger import get_logger
from core.config import config
from core.auth import auth_manager
from utils.constants import APP_NAME, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Load window geometry from config
        self._load_window_state()
        
        # Check authentication
        if not auth_manager.has_credentials():
            self._show_credentials_dialog()
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        
        logger.info("Main window initialized")
    
    def setup_ui(self):
        """Setup the main UI layout."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(200)
        self.sidebar.setMinimumWidth(150)
        self.sidebar.currentRowChanged.connect(self.change_panel)
        
        # Add sidebar items
        sidebar_items = [
            ("Channels", "📺"),
            ("Videos", "🎬"),
            ("Players", "▶️"),
            ("Interactive", "💬"),
            ("Monitor", "📊"),
            ("Settings", "⚙️")
        ]
        
        for text, icon in sidebar_items:
            item = QListWidgetItem(f"{icon}  {text}")
            item.setSizeHint(QSize(0, 40))
            self.sidebar.addItem(item)
        
        # Content area
        self.content_stack = QStackedWidget()
        
        # Add placeholder panels (will be replaced with actual panels)
        from ui.channels_panel import ChannelsPanel
        from ui.videos_panel import VideosPanel
        from ui.players_panel import PlayersPanel
        from ui.interactive_panel import InteractivePanel
        from ui.monitor_panel import MonitorPanel
        from ui.settings_panel import SettingsPanel
        
        try:
            self.content_stack.addWidget(ChannelsPanel())
            self.content_stack.addWidget(VideosPanel())
            self.content_stack.addWidget(PlayersPanel())
            self.content_stack.addWidget(InteractivePanel())
            self.content_stack.addWidget(MonitorPanel())
            self.content_stack.addWidget(SettingsPanel())
        except Exception as e:
            logger.error(f"Failed to load panels: {e}")
            # Add placeholder panels
            for _ in range(6):
                placeholder = QLabel("Panel loading...")
                placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.content_stack.addWidget(placeholder)
        
        # Add to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack, 1)
        
        # Set initial panel
        self.sidebar.setCurrentRow(0)
    
    def setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("Ctrl+R")
        refresh_action.triggered.connect(self.refresh_current_panel)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        preferences_action = QAction("&Preferences", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(self.show_preferences)
        edit_menu.addAction(preferences_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        channels_action = QAction("&Channels", self)
        channels_action.setShortcut("Ctrl+1")
        channels_action.triggered.connect(lambda: self.sidebar.setCurrentRow(0))
        view_menu.addAction(channels_action)
        
        videos_action = QAction("&Videos", self)
        videos_action.setShortcut("Ctrl+2")
        videos_action.triggered.connect(lambda: self.sidebar.setCurrentRow(1))
        view_menu.addAction(videos_action)
        
        monitor_action = QAction("&Monitor", self)
        monitor_action.setShortcut("Ctrl+3")
        monitor_action.triggered.connect(lambda: self.sidebar.setCurrentRow(4))
        view_menu.addAction(monitor_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        documentation_action = QAction("&Documentation", self)
        documentation_action.triggered.connect(self.show_documentation)
        help_menu.addAction(documentation_action)
    
    def setup_statusbar(self):
        """Setup status bar."""
        self.statusBar().showMessage("Ready")
    
    def change_panel(self, index: int):
        """
        Change the current panel.
        
        Args:
            index: Panel index
        """
        self.content_stack.setCurrentIndex(index)
        panel_names = ["Channels", "Videos", "Players", "Interactive", "Monitor", "Settings"]
        if 0 <= index < len(panel_names):
            self.statusBar().showMessage(f"{panel_names[index]} panel")
            logger.debug(f"Switched to {panel_names[index]} panel")
    
    def refresh_current_panel(self):
        """Refresh the current panel."""
        current_widget = self.content_stack.currentWidget()
        if hasattr(current_widget, 'refresh'):
            current_widget.refresh()
            self.statusBar().showMessage("Refreshed", 2000)
        else:
            logger.warning("Current panel does not support refresh")
    
    def show_preferences(self):
        """Show preferences dialog."""
        self.sidebar.setCurrentRow(5)  # Switch to Settings panel
    
    def show_about(self):
        """Show about dialog."""
        from utils.constants import APP_VERSION
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"""<h3>{APP_NAME}</h3>
            <p>Version {APP_VERSION}</p>
            <p>A comprehensive desktop application for managing IBM Video Streaming services.</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Channel management</li>
                <li>Video upload and management</li>
                <li>Player configuration</li>
                <li>Interactive features (chat, polls, Q&A)</li>
                <li>Real-time monitoring and analytics</li>
            </ul>
            <p>Built with Python and PyQt6</p>"""
        )
    
    def show_documentation(self):
        """Show documentation."""
        QMessageBox.information(
            self,
            "Documentation",
            "Documentation is available in the docs/ directory.\n\n"
            "For online help, visit:\n"
            "https://developers.video.ibm.com/"
        )
    
    def _show_credentials_dialog(self):
        """Show credentials input dialog."""
        from ui.settings_panel import CredentialsDialog
        
        dialog = CredentialsDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            QMessageBox.warning(
                self,
                "No Credentials",
                "API credentials are required to use this application.\n"
                "You can set them later in Settings."
            )
    
    def _load_window_state(self):
        """Load window state from config."""
        # Load size
        width, height = config.get_window_size()
        self.resize(width, height)
        
        # Load position
        position = config.get_window_position()
        if position:
            x, y = position
            self.move(x, y)
    
    def _save_window_state(self):
        """Save window state to config."""
        # Save size
        config.set_window_size(self.width(), self.height())
        
        # Save position
        config.set_window_position(self.x(), self.y())
    
    def closeEvent(self, event):
        """Handle window close event."""
        self._save_window_state()
        logger.info("Application closing")
        event.accept()

# Made with Bob
