"""
Analytics Dashboard panel for viewing channel, video, and live stream analytics.
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QGroupBox, QWidget, QTabWidget,
    QTableWidget, QTableWidgetItem, QDateEdit, QSplitter
)
from PySide6.QtCore import Qt, QTimer, QDate
from datetime import datetime, timedelta

from ui.base_panel import BasePanel
from api.analytics import analytics_manager
from api.channels import channel_manager
from api.videos import video_manager
from core.logger import get_logger
from core.exceptions import NotFoundError
from utils.helpers import format_number, time_ago

logger = get_logger(__name__)


class AnalyticsDashboardPanel(BasePanel):
    """
    Comprehensive Analytics Dashboard for IBM Video Streaming.
    
    Features:
    - Channel analytics with date range selection
    - Video-specific analytics
    - Live stream monitoring
    - Export capabilities
    """
    
    def __init__(self):
        super().__init__("Analytics Dashboard")
        self.current_channel_id = None
        self.current_video_id = None
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
    
    def setup_ui(self):
        """Setup the analytics dashboard UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("📊 Analytics Dashboard")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)
        
        # Toolbar
        toolbar = self.create_toolbar()
        layout.addLayout(toolbar)
        
        # Main content with tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_channel_analytics_tab(), "📺 Channel Analytics")
        self.tabs.addTab(self.create_video_analytics_tab(), "🎬 Video Analytics")
        self.tabs.addTab(self.create_live_stream_tab(), "🔴 Live Stream Monitor")
        
        layout.addWidget(self.tabs)
        
        # Load initial data
        self.load_channels()
    
    def create_toolbar(self) -> QHBoxLayout:
        """Create toolbar with common controls."""
        toolbar = QHBoxLayout()
        
        # Channel selector
        toolbar.addWidget(QLabel("Channel:"))
        self.channel_combo = QComboBox()
        self.channel_combo.setMinimumWidth(200)
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        toolbar.addWidget(self.channel_combo)
        
        # Date range
        toolbar.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.dateChanged.connect(self.on_date_changed)
        toolbar.addWidget(self.start_date)
        
        toolbar.addWidget(QLabel("To:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.dateChanged.connect(self.on_date_changed)
        toolbar.addWidget(self.end_date)
        
        # Quick range buttons
        quick_ranges = QHBoxLayout()
        for label, days in [("Today", 0), ("7 Days", 7), ("30 Days", 30), ("90 Days", 90)]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, d=days: self.set_quick_range(d))
            quick_ranges.addWidget(btn)
        toolbar.addLayout(quick_ranges)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_all)
        toolbar.addWidget(refresh_btn)
        
        # Export button
        export_btn = QPushButton("📥 Export")
        export_btn.clicked.connect(self.export_data)
        toolbar.addWidget(export_btn)
        
        toolbar.addStretch()
        
        return toolbar
    
    def create_channel_analytics_tab(self) -> QWidget:
        """Create channel analytics tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary cards
        summary_layout = QHBoxLayout()
        
        # Total views card
        views_group = QGroupBox("Total Views")
        views_layout = QVBoxLayout()
        self.total_views_label = QLabel("--")
        self.total_views_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2196F3;")
        self.total_views_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        views_layout.addWidget(self.total_views_label)
        views_group.setLayout(views_layout)
        summary_layout.addWidget(views_group)
        
        # Unique viewers card
        unique_group = QGroupBox("Unique Viewers")
        unique_layout = QVBoxLayout()
        self.unique_viewers_label = QLabel("--")
        self.unique_viewers_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #4CAF50;")
        self.unique_viewers_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        unique_layout.addWidget(self.unique_viewers_label)
        unique_group.setLayout(unique_layout)
        summary_layout.addWidget(unique_group)
        
        # Watch time card
        watch_time_group = QGroupBox("Total Watch Time")
        watch_time_layout = QVBoxLayout()
        self.watch_time_label = QLabel("--")
        self.watch_time_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #FF9800;")
        self.watch_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        watch_time_layout.addWidget(self.watch_time_label)
        watch_time_group.setLayout(watch_time_layout)
        summary_layout.addWidget(watch_time_group)
        
        # Peak viewers card
        peak_group = QGroupBox("Peak Concurrent")
        peak_layout = QVBoxLayout()
        self.peak_viewers_label = QLabel("--")
        self.peak_viewers_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #9C27B0;")
        self.peak_viewers_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        peak_layout.addWidget(self.peak_viewers_label)
        peak_group.setLayout(peak_layout)
        summary_layout.addWidget(peak_group)
        
        layout.addLayout(summary_layout)
        
        # Detailed metrics table
        metrics_group = QGroupBox("Detailed Metrics")
        metrics_layout = QVBoxLayout()
        
        self.channel_metrics_table = QTableWidget()
        self.channel_metrics_table.setColumnCount(2)
        self.channel_metrics_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.channel_metrics_table.horizontalHeader().setStretchLastSection(True)
        metrics_layout.addWidget(self.channel_metrics_table)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        # Demographics section
        demo_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Geographic distribution
        geo_group = QGroupBox("Geographic Distribution")
        geo_layout = QVBoxLayout()
        self.geo_table = QTableWidget()
        self.geo_table.setColumnCount(2)
        self.geo_table.setHorizontalHeaderLabels(["Country", "Viewers"])
        geo_layout.addWidget(self.geo_table)
        geo_group.setLayout(geo_layout)
        demo_splitter.addWidget(geo_group)
        
        # Device breakdown
        device_group = QGroupBox("Device Breakdown")
        device_layout = QVBoxLayout()
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(2)
        self.device_table.setHorizontalHeaderLabels(["Device", "Percentage"])
        device_layout.addWidget(self.device_table)
        device_group.setLayout(device_layout)
        demo_splitter.addWidget(device_group)
        
        layout.addWidget(demo_splitter)
        
        return widget
    
    def create_video_analytics_tab(self) -> QWidget:
        """Create video analytics tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Video selector
        video_selector_layout = QHBoxLayout()
        video_selector_layout.addWidget(QLabel("Select Video:"))
        
        self.video_combo = QComboBox()
        self.video_combo.setMinimumWidth(300)
        self.video_combo.currentIndexChanged.connect(self.on_video_changed)
        video_selector_layout.addWidget(self.video_combo)
        
        load_videos_btn = QPushButton("Load Videos")
        load_videos_btn.clicked.connect(self.load_videos)
        video_selector_layout.addWidget(load_videos_btn)
        
        video_selector_layout.addStretch()
        layout.addLayout(video_selector_layout)
        
        # Video metrics summary
        video_summary_layout = QHBoxLayout()
        
        # Views
        video_views_group = QGroupBox("Video Views")
        video_views_layout = QVBoxLayout()
        self.video_views_label = QLabel("--")
        self.video_views_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2196F3;")
        self.video_views_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_views_layout.addWidget(self.video_views_label)
        video_views_group.setLayout(video_views_layout)
        video_summary_layout.addWidget(video_views_group)
        
        # Completion rate
        completion_group = QGroupBox("Completion Rate")
        completion_layout = QVBoxLayout()
        self.completion_rate_label = QLabel("--")
        self.completion_rate_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #4CAF50;")
        self.completion_rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        completion_layout.addWidget(self.completion_rate_label)
        completion_group.setLayout(completion_layout)
        video_summary_layout.addWidget(completion_group)
        
        # Avg duration
        duration_group = QGroupBox("Avg View Duration")
        duration_layout = QVBoxLayout()
        self.avg_duration_label = QLabel("--")
        self.avg_duration_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FF9800;")
        self.avg_duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        duration_layout.addWidget(self.avg_duration_label)
        duration_group.setLayout(duration_layout)
        video_summary_layout.addWidget(duration_group)
        
        layout.addLayout(video_summary_layout)
        
        # Video metrics table
        video_metrics_group = QGroupBox("Video Performance Metrics")
        video_metrics_layout = QVBoxLayout()
        
        self.video_metrics_table = QTableWidget()
        self.video_metrics_table.setColumnCount(2)
        self.video_metrics_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.video_metrics_table.horizontalHeader().setStretchLastSection(True)
        video_metrics_layout.addWidget(self.video_metrics_table)
        
        video_metrics_group.setLayout(video_metrics_layout)
        layout.addWidget(video_metrics_group)
        
        # Retention chart placeholder
        retention_group = QGroupBox("Viewer Retention")
        retention_layout = QVBoxLayout()
        retention_placeholder = QLabel(
            "📊 Retention Curve\n\n"
            "Shows percentage of viewers at each point in the video\n"
            "(Chart visualization to be implemented with matplotlib)"
        )
        retention_placeholder.setStyleSheet(
            "background-color: #f5f5f5; padding: 30px; border: 1px solid #ddd;"
        )
        retention_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        retention_placeholder.setMinimumHeight(200)
        retention_layout.addWidget(retention_placeholder)
        retention_group.setLayout(retention_layout)
        layout.addWidget(retention_group)
        
        return widget
    
    def create_live_stream_tab(self) -> QWidget:
        """Create live stream monitoring tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Real-time stats
        realtime_layout = QHBoxLayout()
        
        # Current viewers
        current_viewers_group = QGroupBox("🔴 Current Viewers")
        current_viewers_layout = QVBoxLayout()
        self.current_viewers_label = QLabel("--")
        self.current_viewers_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #F44336;")
        self.current_viewers_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_viewers_layout.addWidget(self.current_viewers_label)
        current_viewers_group.setLayout(current_viewers_layout)
        realtime_layout.addWidget(current_viewers_group)
        
        # Stream status
        status_group = QGroupBox("Stream Status")
        status_layout = QVBoxLayout()
        self.stream_status_label = QLabel("Offline")
        self.stream_status_label.setStyleSheet("font-size: 28px; font-weight: bold; color: gray;")
        self.stream_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.stream_status_label)
        status_group.setLayout(status_layout)
        realtime_layout.addWidget(status_group)
        
        # Stream health
        health_group = QGroupBox("Stream Health")
        health_layout = QVBoxLayout()
        self.stream_health_label = QLabel("--")
        self.stream_health_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.stream_health_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        health_layout.addWidget(self.stream_health_label)
        health_group.setLayout(health_layout)
        realtime_layout.addWidget(health_group)
        
        layout.addLayout(realtime_layout)
        
        # Auto-refresh control
        refresh_control_layout = QHBoxLayout()
        self.auto_refresh_check = QPushButton("Auto-Refresh: OFF")
        self.auto_refresh_check.setCheckable(True)
        self.auto_refresh_check.clicked.connect(self.toggle_auto_refresh)
        refresh_control_layout.addWidget(self.auto_refresh_check)
        
        refresh_control_layout.addWidget(QLabel("Refresh Interval:"))
        self.refresh_interval_combo = QComboBox()
        self.refresh_interval_combo.addItems(["5 seconds", "10 seconds", "30 seconds", "1 minute"])
        refresh_control_layout.addWidget(self.refresh_interval_combo)
        
        refresh_control_layout.addStretch()
        layout.addLayout(refresh_control_layout)
        
        # Engagement metrics
        engagement_group = QGroupBox("Live Engagement")
        engagement_layout = QVBoxLayout()
        
        self.engagement_table = QTableWidget()
        self.engagement_table.setColumnCount(2)
        self.engagement_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.engagement_table.horizontalHeader().setStretchLastSection(True)
        engagement_layout.addWidget(self.engagement_table)
        
        engagement_group.setLayout(engagement_layout)
        layout.addWidget(engagement_group)
        
        # Stream timeline placeholder
        timeline_group = QGroupBox("Viewer Timeline")
        timeline_layout = QVBoxLayout()
        timeline_placeholder = QLabel(
            "📈 Live Viewer Count Over Time\n\n"
            "Real-time graph showing viewer count changes\n"
            "(Chart visualization to be implemented)"
        )
        timeline_placeholder.setStyleSheet(
            "background-color: #f5f5f5; padding: 30px; border: 1px solid #ddd;"
        )
        timeline_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline_placeholder.setMinimumHeight(200)
        timeline_layout.addWidget(timeline_placeholder)
        timeline_group.setLayout(timeline_layout)
        layout.addWidget(timeline_group)
        
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
                self.refresh_all()
        except Exception as e:
            self.show_error(f"Failed to load channels: {str(e)}")
            logger.error(f"Failed to load channels: {e}")
    
    def load_videos(self):
        """Load videos for selected channel."""
        if not self.current_channel_id:
            self.show_error("Please select a channel first")
            return
        
        try:
            response = video_manager.list_videos(self.current_channel_id)
            videos = response.get('videos', [])
            
            self.video_combo.clear()
            for video in videos:
                self.video_combo.addItem(
                    video.get('title', 'Untitled'),
                    video.get('id')
                )
            
            if videos:
                self.current_video_id = videos[0].get('id')
                self.load_video_analytics()
            
            logger.info(f"Loaded {len(videos)} videos for channel {self.current_channel_id}")
        except Exception as e:
            self.show_error(f"Failed to load videos: {str(e)}")
            logger.error(f"Failed to load videos: {e}")
    
    def on_channel_changed(self, index: int):
        """Handle channel selection change."""
        if index >= 0:
            self.current_channel_id = self.channel_combo.currentData()
            self.refresh_all()
    
    def on_video_changed(self, index: int):
        """Handle video selection change."""
        if index >= 0:
            self.current_video_id = self.video_combo.currentData()
            self.load_video_analytics()
    
    def on_date_changed(self):
        """Handle date range change."""
        self.refresh_all()
    
    def set_quick_range(self, days: int):
        """Set quick date range."""
        if days == 0:
            self.start_date.setDate(QDate.currentDate())
        else:
            self.start_date.setDate(QDate.currentDate().addDays(-days))
        self.end_date.setDate(QDate.currentDate())
        self.refresh_all()
    
    def get_date_range(self):
        """Get selected date range as datetime objects."""
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        return (
            datetime.combine(start, datetime.min.time()),
            datetime.combine(end, datetime.max.time())
        )
    
    def refresh_all(self):
        """Refresh all analytics data."""
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:  # Channel Analytics
            self.load_channel_analytics()
        elif current_tab == 1:  # Video Analytics
            self.load_video_analytics()
        elif current_tab == 2:  # Live Stream
            self.load_live_stream_data()
    
    def load_channel_analytics(self):
        """Load channel analytics data."""
        if not self.current_channel_id:
            return
        
        try:
            start_date, end_date = self.get_date_range()
            
            # Get channel metrics
            metrics = analytics_manager.get_channel_metrics(
                self.current_channel_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Update summary cards
            self.total_views_label.setText(format_number(metrics.get('total_views', 0)))
            self.unique_viewers_label.setText(format_number(metrics.get('unique_viewers', 0)))
            
            watch_time_hours = metrics.get('total_watch_time', 0) // 3600
            self.watch_time_label.setText(f"{format_number(watch_time_hours)}h")
            
            self.peak_viewers_label.setText(format_number(metrics.get('peak_concurrent_viewers', 0)))
            
            # Update detailed metrics table
            detailed_metrics = [
                ("Total Views", format_number(metrics.get('total_views', 0))),
                ("Unique Viewers", format_number(metrics.get('unique_viewers', 0))),
                ("Average Watch Time", f"{metrics.get('avg_watch_time', 0) // 60} minutes"),
                ("Total Watch Time", f"{watch_time_hours} hours"),
                ("Peak Concurrent Viewers", format_number(metrics.get('peak_concurrent_viewers', 0))),
                ("Engagement Rate", f"{metrics.get('engagement_rate', 0) * 100:.1f}%"),
                ("Bounce Rate", f"{metrics.get('bounce_rate', 0) * 100:.1f}%"),
                ("Return Viewer Rate", f"{metrics.get('return_rate', 0) * 100:.1f}%"),
            ]
            
            self.channel_metrics_table.setRowCount(len(detailed_metrics))
            for row, (metric, value) in enumerate(detailed_metrics):
                self.channel_metrics_table.setItem(row, 0, QTableWidgetItem(metric))
                self.channel_metrics_table.setItem(row, 1, QTableWidgetItem(str(value)))
            
            # Load demographics
            self.load_demographics()
            
            logger.info(f"Loaded channel analytics for {self.current_channel_id}")
            
        except Exception as e:
            logger.error(f"Failed to load channel analytics: {e}")
            self.show_error(f"Failed to load analytics: {str(e)}")
    
    def load_demographics(self):
        """Load viewer demographics."""
        if not self.current_channel_id:
            return
        
        try:
            start_date, end_date = self.get_date_range()
            
            demographics = analytics_manager.get_viewer_demographics(
                self.current_channel_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Geographic distribution
            countries = demographics.get('countries', {})
            self.geo_table.setRowCount(len(countries))
            for row, (country, count) in enumerate(countries.items()):
                self.geo_table.setItem(row, 0, QTableWidgetItem(country))
                self.geo_table.setItem(row, 1, QTableWidgetItem(format_number(count)))
            
            # Device breakdown
            devices = demographics.get('devices', {})
            total_devices = sum(devices.values()) or 1
            self.device_table.setRowCount(len(devices))
            for row, (device, count) in enumerate(devices.items()):
                percentage = (count / total_devices) * 100
                self.device_table.setItem(row, 0, QTableWidgetItem(device))
                self.device_table.setItem(row, 1, QTableWidgetItem(f"{percentage:.1f}%"))
            
        except Exception as e:
            logger.error(f"Failed to load demographics: {e}")
    
    def load_video_analytics(self):
        """Load video analytics data."""
        if not self.current_video_id:
            return
        
        try:
            start_date, end_date = self.get_date_range()
            
            metrics = analytics_manager.get_video_metrics(
                self.current_video_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Update summary
            self.video_views_label.setText(format_number(metrics.get('views', 0)))
            self.completion_rate_label.setText(f"{metrics.get('completion_rate', 0) * 100:.1f}%")
            
            avg_duration_mins = metrics.get('avg_view_duration', 0) // 60
            self.avg_duration_label.setText(f"{avg_duration_mins}m")
            
            # Update detailed metrics
            video_metrics = [
                ("Total Views", format_number(metrics.get('views', 0))),
                ("Unique Viewers", format_number(metrics.get('unique_viewers', 0))),
                ("Completion Rate", f"{metrics.get('completion_rate', 0) * 100:.1f}%"),
                ("Average View Duration", f"{avg_duration_mins} minutes"),
                ("Total Watch Time", f"{metrics.get('total_watch_time', 0) // 3600} hours"),
                ("Likes", format_number(metrics.get('likes', 0))),
                ("Shares", format_number(metrics.get('shares', 0))),
                ("Comments", format_number(metrics.get('comments', 0))),
            ]
            
            self.video_metrics_table.setRowCount(len(video_metrics))
            for row, (metric, value) in enumerate(video_metrics):
                self.video_metrics_table.setItem(row, 0, QTableWidgetItem(metric))
                self.video_metrics_table.setItem(row, 1, QTableWidgetItem(str(value)))
            
            logger.info(f"Loaded video analytics for {self.current_video_id}")
            
        except Exception as e:
            logger.error(f"Failed to load video analytics: {e}")
            self.show_error(f"Failed to load video analytics: {str(e)}")
    
    def load_live_stream_data(self):
        """Load live stream monitoring data."""
        if not self.current_channel_id:
            return
        
        try:
            # Current viewers
            viewers_data = analytics_manager.get_current_viewers(self.current_channel_id)
            current = viewers_data.get('current', 0)
            self.current_viewers_label.setText(format_number(current))
            
            # Stream health
            health_data = analytics_manager.get_stream_health(self.current_channel_id)
            status = health_data.get('status', 'unknown')
            
            if status == 'healthy':
                self.stream_status_label.setText("🔴 Live")
                self.stream_status_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #F44336;")
                self.stream_health_label.setText("Healthy")
                self.stream_health_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #4CAF50;")
            elif status == 'warning':
                self.stream_status_label.setText("⚠️ Live (Issues)")
                self.stream_status_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FF9800;")
                self.stream_health_label.setText("Warning")
                self.stream_health_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FF9800;")
            else:
                self.stream_status_label.setText("Offline")
                self.stream_status_label.setStyleSheet("font-size: 28px; font-weight: bold; color: gray;")
                self.stream_health_label.setText("--")
                self.stream_health_label.setStyleSheet("font-size: 28px; font-weight: bold; color: gray;")
            
            # Engagement metrics
            start_date, end_date = self.get_date_range()
            engagement = analytics_manager.get_engagement_metrics(
                self.current_channel_id,
                start_date=start_date,
                end_date=end_date
            )
            
            engagement_metrics = [
                ("Chat Messages", format_number(engagement.get('chat_messages', 0))),
                ("Active Chatters", format_number(engagement.get('active_chatters', 0))),
                ("Poll Responses", format_number(engagement.get('poll_responses', 0))),
                ("Q&A Questions", format_number(engagement.get('qa_questions', 0))),
                ("Engagement Rate", f"{engagement.get('engagement_rate', 0) * 100:.1f}%"),
            ]
            
            self.engagement_table.setRowCount(len(engagement_metrics))
            for row, (metric, value) in enumerate(engagement_metrics):
                self.engagement_table.setItem(row, 0, QTableWidgetItem(metric))
                self.engagement_table.setItem(row, 1, QTableWidgetItem(str(value)))
            
            logger.info(f"Loaded live stream data for {self.current_channel_id}")
            
        except Exception as e:
            logger.error(f"Failed to load live stream data: {e}")
    
    def toggle_auto_refresh(self, checked: bool):
        """Toggle auto-refresh for live stream monitoring."""
        if checked:
            interval_text = self.refresh_interval_combo.currentText()
            if "5 seconds" in interval_text:
                interval = 5000
            elif "10 seconds" in interval_text:
                interval = 10000
            elif "30 seconds" in interval_text:
                interval = 30000
            else:  # 1 minute
                interval = 60000
            
            self.refresh_timer.start(interval)
            self.auto_refresh_check.setText("Auto-Refresh: ON")
            logger.info(f"Auto-refresh enabled ({interval}ms)")
        else:
            self.refresh_timer.stop()
            self.auto_refresh_check.setText("Auto-Refresh: OFF")
            logger.info("Auto-refresh disabled")
    
    def auto_refresh(self):
        """Auto-refresh live stream data."""
        if self.tabs.currentIndex() == 2:  # Live Stream tab
            self.load_live_stream_data()
    
    def export_data(self):
        """Export analytics data."""
        if not self.current_channel_id:
            self.show_error("Please select a channel first")
            return
        
        try:
            start_date, end_date = self.get_date_range()
            
            result = analytics_manager.export_metrics(
                self.current_channel_id,
                start_date=start_date,
                end_date=end_date,
                format='json'
            )
            
            self.show_success("Analytics data exported successfully!")
            logger.info(f"Exported analytics for channel {self.current_channel_id}")
            
        except Exception as e:
            self.show_error(f"Failed to export data: {str(e)}")
            logger.error(f"Failed to export data: {e}")


# Made with Bob