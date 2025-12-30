"""
Analytics and monitoring API operations.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from api.client import client
from core.logger import get_logger
from utils.helpers import format_datetime

logger = get_logger(__name__)


class AnalyticsManager:
    """Manages analytics and monitoring API operations."""
    
    def __init__(self):
        self.client = client
    
    def get_channel_metrics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get analytics metrics for a channel.
        
        Args:
            channel_id: Channel ID
            start_date: Start date for metrics (default: 30 days ago)
            end_date: End date for metrics (default: now)
            metrics: List of specific metrics to retrieve
            
        Returns:
            Channel metrics
        """
        # Set default date range if not provided
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date)
        }
        
        if metrics:
            params['metrics'] = ','.join(metrics)
        
        logger.info(f"Fetching metrics for channel {channel_id} ({start_date} to {end_date})")
        response = self.client.get(
            f'/channels/{channel_id}/metrics.json',
            params=params
        )
        
        return response.get('metrics', {})
    
    def get_current_viewers(self, channel_id: str) -> Dict[str, Any]:
        """
        Get current viewer count and details.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Current viewer information
        """
        logger.info(f"Fetching current viewers for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/viewers.json')
        
        return response.get('viewers', {})
    
    def get_stream_health(self, channel_id: str) -> Dict[str, Any]:
        """
        Get stream health metrics.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Stream health information
        """
        logger.info(f"Fetching stream health for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/health.json')
        
        return response.get('health', {})
    
    def get_viewer_demographics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get viewer demographics (countries, devices, etc.).
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Viewer demographics
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date)
        }
        
        logger.info(f"Fetching viewer demographics for channel: {channel_id}")
        response = self.client.get(
            f'/channels/{channel_id}/demographics.json',
            params=params
        )
        
        return response.get('demographics', {})
    
    def get_engagement_metrics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get engagement metrics (chat activity, poll participation, etc.).
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Engagement metrics
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date)
        }
        
        logger.info(f"Fetching engagement metrics for channel: {channel_id}")
        response = self.client.get(
            f'/channels/{channel_id}/engagement.json',
            params=params
        )
        
        return response.get('engagement', {})
    
    def get_video_metrics(
        self,
        video_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get metrics for a specific video.
        
        Args:
            video_id: Video ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Video metrics
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date)
        }
        
        logger.info(f"Fetching metrics for video: {video_id}")
        response = self.client.get(
            f'/videos/{video_id}/metrics.json',
            params=params
        )
        
        return response.get('metrics', {})
    
    def get_peak_viewers(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get peak viewer information.
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Peak viewer data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date)
        }
        
        logger.info(f"Fetching peak viewers for channel: {channel_id}")
        response = self.client.get(
            f'/channels/{channel_id}/peak-viewers.json',
            params=params
        )
        
        return response.get('peak_viewers', {})
    
    def get_watch_time(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get total watch time metrics.
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Watch time data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date)
        }
        
        logger.info(f"Fetching watch time for channel: {channel_id}")
        response = self.client.get(
            f'/channels/{channel_id}/watch-time.json',
            params=params
        )
        
        return response.get('watch_time', {})
    
    def export_metrics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        format: str = 'json'
    ) -> Dict[str, Any]:
        """
        Export metrics data.
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            format: Export format ('json' or 'csv')
            
        Returns:
            Export data or download URL
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'start_date': format_datetime(start_date),
            'end_date': format_datetime(end_date),
            'format': format
        }
        
        logger.info(f"Exporting metrics for channel {channel_id} as {format}")
        response = self.client.get(
            f'/channels/{channel_id}/metrics/export.json',
            params=params
        )
        
        return response


# Global analytics manager instance
analytics_manager = AnalyticsManager()

# Made with Bob
