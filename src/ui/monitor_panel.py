"""
Stream monitoring and analytics panel.
"""
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QGroupBox, QWidget, QSplitter,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime, timedelta

from ui.base_panel import BasePanel
from api.analytics import analytics_manager
from api.channels import channel_manager
from core.logger import get_logger
from core.exceptions import NotFoundError
from utils.helpers import format_number, time_ago

logger = get_logger(__name__)


class MonitorPanel(BasePanel):
    """Panel for monitoring streams and viewing analytics."""
    
    def __init__(self):
        super().__init__("Stream Monitor & Analytics")
        self.current_channel_id = None
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
    
    def setup_ui(self):
        """Setup the monitoring panel UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Stream Monitor & Analytics")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        toolbar.addWidget(QLabel("Channel:"))
        self.channel_combo = QComboBox()
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        self.load_channels()
        toolbar.addWidget(self.channel_combo)
        
        self.auto_refresh_check = QPushButton("Auto-Refresh: OFF")
        self.auto_refresh_check.setCheckable(True)
        self.auto_refresh_check.clicked.connect(self.toggle_auto_refresh)
        toolbar.addWidget(self.auto_refresh_check)
        
        refresh_btn = QPushButton("Refresh Now")
        refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Top section: Current stats
        stats_widget = self.create_stats_widget()
        splitter.addWidget(stats_widget)
        
        # Middle section: Stream preview placeholder
        preview_widget = self.create_preview_widget()
        splitter.addWidget(preview_widget)
        
        # Bottom section: Analytics
        analytics_widget = self.create_analytics_widget()
        splitter.addWidget(analytics_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 2)
        
        layout.addWidget(splitter)
    
    def create_stats_widget(self) -> QWidget:
        """Create current statistics widget."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Current viewers
        viewers_group = QGroupBox("Current Viewers")
        viewers_layout = QVBoxLayout()
        self.viewers_label = QLabel("--")
        self.viewers_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.viewers_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        viewers_layout.addWidget(self.viewers_label)
        viewers_group.setLayout(viewers_layout)
        layout.addWidget(viewers_group)
        
        # Stream status
        status_group = QGroupBox("Stream Status")
        status_layout = QVBoxLayout()
        self.status_label = QLabel("Offline")
        self.status_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Stream health
        health_group = QGroupBox("Stream Health")
        health_layout = QVBoxLayout()
        self.health_label = QLabel("--")
        self.health_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.health_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        health_layout.addWidget(self.health_label)
        health_group.setLayout(health_layout)
        layout.addWidget(health_group)
        
        # Peak viewers
        peak_group = QGroupBox("Peak Viewers Today")
        peak_layout = QVBoxLayout()
        self.peak_label = QLabel("--")
        self.peak_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.peak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        peak_layout.addWidget(self.peak_label)
        peak_group.setLayout(peak_layout)
        layout.addWidget(peak_group)
        
        return widget
    
    def create_preview_widget(self) -> QWidget:
        """Create stream preview widget."""
        widget = QGroupBox("Stream Preview")
        layout = QVBoxLayout(widget)
        
        # Placeholder for VLC player
        # In a full implementation, this would embed a VLC player widget
        preview_placeholder = QLabel("Stream Preview\n\n(VLC Player Integration)\n\nTo be implemented with python-vlc")
        preview_placeholder.setStyleSheet(
            "background-color: #000; color: #fff; font-size: 16px; padding: 40px;"
        )
        preview_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_placeholder.setMinimumHeight(300)
        layout.addWidget(preview_placeholder)
        
        # Preview controls
        controls_layout = QHBoxLayout()
        
        self.preview_url_label = QLabel("Stream URL: --")
        controls_layout.addWidget(self.preview_url_label)
        
        open_browser_btn = QPushButton("Open in Browser")
        open_browser_btn.clicked.connect(self.open_in_browser)
        controls_layout.addWidget(open_browser_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        return widget
    
    def create_analytics_widget(self) -> QWidget:
        """Create analytics widget."""
        widget = QGroupBox("Analytics & Metrics")
        layout = QVBoxLayout(widget)
        
        # Time range selector
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Time Range:"))
        
        self.time_range_combo = QComboBox()
        self.time_range_combo.addItems([
            "Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"
        ])
        self.time_range_combo.currentIndexChanged.connect(self.load_analytics)
        range_layout.addWidget(self.time_range_combo)
        
        range_layout.addStretch()
        layout.addLayout(range_layout)
        
        # Metrics table
        self.metrics_table = QTableWidget()
        self.metrics_table.setColumnCount(2)
        self.metrics_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.metrics_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.metrics_table)
        
        # Placeholder for charts
        # In a full implementation, this would use matplotlib or pyqtgraph
        chart_placeholder = QLabel("Analytics Charts\n\n(matplotlib/pyqtgraph Integration)\n\nCharts will show:\n- Viewer count over time\n- Engagement metrics\n- Geographic distribution")
        chart_placeholder.setStyleSheet(
            "background-color: #f0f0f0; padding: 20px; border: 1px solid #ccc;"
        )
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setMinimumHeight(200)
        layout.addWidget(chart_placeholder)
        
        return widget
    
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
                self.load_all_data()
        except Exception as e:
            self.show_error(f"Failed to load channels: {str(e)}")
    
    def on_channel_changed(self, index: int):
        """Handle channel selection change."""
        if index >= 0:
            self.current_channel_id = self.channel_combo.currentData()
            self.load_all_data()
    
    def load_all_data(self):
        """Load all monitoring data."""
        self.load_current_stats()
        self.load_stream_health()
        self.load_analytics()
    
    def load_current_stats(self):
        """Load current viewer statistics."""
        if not self.current_channel_id:
            return
        
        try:
            viewers_data = analytics_manager.get_current_viewers(self.current_channel_id)
            
            current = viewers_data.get('current', 0)
            if hasattr(self, 'viewers_label'):
                self.viewers_label.setText(format_number(current))
            
            peak = viewers_data.get('peak_today', 0)
            if hasattr(self, 'peak_label'):
                self.peak_label.setText(format_number(peak))
            
            # Update stream URL
            if hasattr(self, 'preview_url_label'):
                self.preview_url_label.setText(
                    f"Stream URL: https://video.ibm.com/channel/{self.current_channel_id}"
                )
            
            logger.debug(f"Current viewers: {current}, Peak: {peak}")
            
        except Exception as e:
            from api.exceptions import NotFoundError
            if isinstance(e, NotFoundError):
                logger.warning(f"Viewer stats not available for channel {self.current_channel_id}")
            else:
                logger.error(f"Failed to load current stats: {e}")
            
            # Safely update UI
            if hasattr(self, 'viewers_label'):
                self.viewers_label.setText("N/A")
            if hasattr(self, 'peak_label'):
                self.peak_label.setText("N/A")
    
    def load_stream_health(self):
        """Load stream health information."""
        if not self.current_channel_id:
            return
        
        try:
            health_data = analytics_manager.get_stream_health(self.current_channel_id)
            
            status = health_data.get('status', 'unknown')
            if hasattr(self, 'health_label'):
                self.health_label.setText(status.upper())
            
            # Color code based on status
            if status == 'healthy':
                if hasattr(self, 'health_label'):
                    self.health_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: green;"
                    )
                if hasattr(self, 'status_label'):
                    self.status_label.setText("Live")
                    self.status_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: green;"
                    )
            elif status == 'warning':
                if hasattr(self, 'health_label'):
                    self.health_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: orange;"
                    )
                if hasattr(self, 'status_label'):
                    self.status_label.setText("Live (Issues)")
                    self.status_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: orange;"
                    )
            else:
                if hasattr(self, 'health_label'):
                    self.health_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: gray;"
                    )
                if hasattr(self, 'status_label'):
                    self.status_label.setText("Offline")
                    self.status_label.setStyleSheet(
                        "font-size: 24px; font-weight: bold; color: gray;"
                    )
            
            logger.debug(f"Stream health: {status}")
            
        except Exception as e:
            from api.exceptions import NotFoundError
            if isinstance(e, NotFoundError):
                logger.warning(f"Stream health not available for channel {self.current_channel_id}")
            else:
                logger.error(f"Failed to load stream health: {e}")
            
            if hasattr(self, 'health_label'):
                self.health_label.setText("N/A")
            if hasattr(self, 'status_label'):
                self.status_label.setText("Unknown")
    
    def load_analytics(self):
        """Load analytics metrics."""
        if not self.current_channel_id:
            return
        
        if not hasattr(self, 'time_range_combo'):
            logger.warning("Analytics UI not initialized yet")
            return
        
        try:
            # Determine time range
            range_text = self.time_range_combo.currentText()
            if range_text == "Last Hour":
                start_date = datetime.utcnow() - timedelta(hours=1)
            elif range_text == "Last 24 Hours":
                start_date = datetime.utcnow() - timedelta(days=1)
            elif range_text == "Last 7 Days":
                start_date = datetime.utcnow() - timedelta(days=7)
            else:  # Last 30 Days
                start_date = datetime.utcnow() - timedelta(days=30)
            
            metrics = analytics_manager.get_channel_metrics(
                self.current_channel_id,
                start_date=start_date
            )
            
            # Populate metrics table
            metrics_data = [
                ("Total Views", format_number(metrics.get('total_views', 0))),
                ("Unique Viewers", format_number(metrics.get('unique_viewers', 0))),
                ("Avg Watch Time", f"{metrics.get('avg_watch_time', 0) // 60} minutes"),
                ("Peak Concurrent", format_number(metrics.get('peak_concurrent_viewers', 0))),
                ("Total Watch Time", f"{metrics.get('total_watch_time', 0) // 3600} hours"),
                ("Engagement Rate", f"{metrics.get('engagement_rate', 0) * 100:.1f}%"),
            ]
            
            self.metrics_table.setRowCount(len(metrics_data))
            for row, (metric, value) in enumerate(metrics_data):
                self.metrics_table.setItem(row, 0, QTableWidgetItem(metric))
                self.metrics_table.setItem(row, 1, QTableWidgetItem(str(value)))
            
            logger.info(f"Loaded analytics for {range_text}")
            
        except NotFoundError:
            logger.warning(f"Analytics not available for channel {self.current_channel_id}")
        except Exception as e:
            logger.error(f"Failed to load analytics: {e}")
    
    def toggle_auto_refresh(self, checked: bool):
        """Toggle auto-refresh."""
        if checked:
            self.refresh_timer.start(5000)  # Refresh every 5 seconds
            self.auto_refresh_check.setText("Auto-Refresh: ON")
            logger.info("Auto-refresh enabled")
        else:
            self.refresh_timer.stop()
            self.auto_refresh_check.setText("Auto-Refresh: OFF")
            logger.info("Auto-refresh disabled")
    
    def auto_refresh(self):
        """Auto-refresh data."""
        self.load_current_stats()
        self.load_stream_health()
    
    def open_in_browser(self):
        """Open stream in browser."""
        if not self.current_channel_id:
            self.show_error("No channel selected")
            return
        
        import webbrowser
        url = f"https://video.ibm.com/channel/{self.current_channel_id}"
        webbrowser.open(url)
        logger.info(f"Opened stream in browser: {url}")
    
    def refresh(self):
        """Refresh all data."""
        self.load_all_data()
    
    def closeEvent(self, event):
        """Handle panel close event."""
        self.refresh_timer.stop()
        super().closeEvent(event)

# Made with Bob
