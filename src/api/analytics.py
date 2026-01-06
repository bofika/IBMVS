"""
Analytics and monitoring API operations.

The Analytics API uses JWT authentication instead of standard OAuth tokens.
All requests to the Analytics API must use JWT tokens obtained via the
auth manager's get_jwt_token() method.

Based on IBM Video Streaming Analytics API v1 documentation:
https://github.com/IBM/video-streaming-developer-docs
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from api.client import client
from core.logger import get_logger

logger = get_logger(__name__)


class AnalyticsManager:
    """
    Manages analytics and monitoring API operations.
    
    Note: Analytics API requires JWT authentication, which is handled
    automatically by the client's analytics_get() method.
    
    API Base URL: https://analytics-api.video.ibm.com/v1/
    """
    
    def __init__(self):
        self.client = client
    
    def _format_datetime(self, dt: datetime) -> str:
        """Format datetime to ISO8601 format required by Analytics API."""
        return dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    def get_total_views(
        self,
        content_type: str = 'live',
        content_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        dimension: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get total views for content.
        
        Args:
            content_type: 'live' or 'recorded'
            content_id: Optional content ID (channel or video)
            start_date: Start date for metrics
            end_date: End date for metrics
            dimension: Optional dimension (month, day, hour, device, view-source, country, region)
            
        Returns:
            Total views data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date),
            '_page': 1,
            '_limit': 1000
        }
        
        if content_id:
            params['content_id'] = content_id
        
        # Build endpoint based on parameters
        if dimension:
            endpoint = f'/v1/total-views/{content_type}/{dimension}'
        else:
            endpoint = f'/v1/total-views/{content_type}/summary'
        
        logger.info(f"Fetching total views: {endpoint}")
        response = self.client.analytics_get(endpoint, params=params)
        
        return response
    
    def get_channel_metrics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get analytics metrics for a channel (live content).
        
        Args:
            channel_id: Channel ID
            start_date: Start date for metrics (default: 30 days ago)
            end_date: End date for metrics (default: now)
            metrics: List of specific metrics to retrieve (not used in v1 API)
            
        Returns:
            Channel metrics
        """
        return self.get_total_views(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_video_metrics(
        self,
        video_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get metrics for a specific video (recorded content).
        
        Args:
            video_id: Video ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Video metrics
        """
        return self.get_total_views(
            content_type='recorded',
            content_id=video_id,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_unique_devices(
        self,
        content_type: str = 'live',
        content_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        dimension: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get unique devices metrics.
        
        Args:
            content_type: 'live' or 'recorded'
            content_id: Optional content ID
            start_date: Start date
            end_date: End date
            dimension: Optional dimension
            
        Returns:
            Unique devices data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date),
            '_page': 1,
            '_limit': 1000
        }
        
        if content_id:
            params['content_id'] = content_id
        
        if dimension:
            endpoint = f'/v1/unique-devices/{content_type}/{dimension}'
        else:
            endpoint = f'/v1/unique-devices/{content_type}/summary'
        
        logger.info(f"Fetching unique devices: {endpoint}")
        response = self.client.analytics_get(endpoint, params=params)
        
        return response
    
    def get_authenticated_viewers(
        self,
        content_type: str = 'live',
        content_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        dimension: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get authenticated viewers metrics.
        
        Args:
            content_type: 'live' or 'recorded'
            content_id: Optional content ID
            start_date: Start date
            end_date: End date
            dimension: Optional dimension
            
        Returns:
            Authenticated viewers data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date),
            '_page': 1,
            '_limit': 1000
        }
        
        if content_id:
            params['content_id'] = content_id
        
        if dimension:
            endpoint = f'/v1/authenticated-viewers/{content_type}/{dimension}'
        else:
            endpoint = f'/v1/authenticated-viewers/{content_type}/summary'
        
        logger.info(f"Fetching authenticated viewers: {endpoint}")
        response = self.client.analytics_get(endpoint, params=params)
        
        return response
    
    def get_peak_viewers(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        granularity: str = 'minute'
    ) -> Dict[str, Any]:
        """
        Get peak viewer information for a channel.
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            granularity: 'minute', 'hour', 'day', or 'month'
            
        Returns:
            Peak viewer data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date),
            'content_id': channel_id,
            'granularity': granularity,
            '_page': 1,
            '_limit': 1000
        }
        
        logger.info(f"Fetching peak viewers for channel: {channel_id}")
        response = self.client.analytics_get('/v1/peak-viewer-numbers/live', params=params)
        
        return response
    
    def get_peak_viewers_summary(
        self,
        content_type: str,
        content_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get peak viewer summary for content.
        
        Args:
            content_type: 'live' or 'recorded'
            content_id: Content ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Peak viewer summary
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'content_id': content_id,
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date)
        }
        
        logger.info(f"Fetching peak viewer summary for {content_type} {content_id}")
        response = self.client.analytics_get(f'/v1/peak-viewer-numbers/{content_type}/summary', params=params)
        
        return response
    
    def get_viewer_seconds(
        self,
        content_type: str = 'live',
        content_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        granularity: str = 'day'
    ) -> Dict[str, Any]:
        """
        Get viewer consumption in seconds (watch time).
        
        Args:
            content_type: 'live' or 'recorded'
            content_id: Optional content ID
            start_date: Start date
            end_date: End date
            granularity: 'minute', 'hour', 'day', or 'month'
            
        Returns:
            Viewer seconds data
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        params: Dict[str, Any] = {
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date),
            'granularity': granularity,
            '_page': 1,
            '_limit': 1000
        }
        
        if content_id:
            params['content_id'] = content_id
        
        logger.info(f"Fetching viewer seconds for {content_type}")
        response = self.client.analytics_get(f'/v1/viewer-seconds/{content_type}', params=params)
        
        return response
    
    def get_watch_time(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get total watch time metrics for a channel.
        
        Args:
            channel_id: Channel ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Watch time data
        """
        return self.get_viewer_seconds(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_viewers_list(
        self,
        content_type: Optional[str] = None,
        content_id: Optional[str] = None,
        viewer_identifier: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get list of unique viewers.
        
        Args:
            content_type: Optional 'live' or 'recorded'
            content_id: Optional content ID
            viewer_identifier: Optional filter for viewer identifiers
            start_date: Start date
            end_date: End date
            page: Page number
            limit: Page size
            
        Returns:
            List of viewers
        """
        params: Dict[str, Any] = {
            '_page': page,
            '_limit': limit
        }
        
        if start_date:
            params['date_time_from'] = self._format_datetime(start_date)
        if end_date:
            params['date_time_to'] = self._format_datetime(end_date)
        if viewer_identifier:
            params['viewer_identifier'] = viewer_identifier
        if content_id:
            params['content_id'] = content_id
        
        if content_type:
            endpoint = f'/v1/viewers/{content_type}'
        else:
            endpoint = '/v1/viewers'
        
        logger.info(f"Fetching viewers list: {endpoint}")
        response = self.client.analytics_get(endpoint, params=params)
        
        return response
    
    def get_raw_views(
        self,
        content_type: Optional[str] = None,
        content_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get raw view segments export.
        
        Args:
            content_type: Optional 'live' or 'recorded'
            content_id: Optional content ID
            start_date: Start date (required)
            end_date: End date (required)
            page: Page number
            limit: Page size
            
        Returns:
            Raw view segments
        """
        if not start_date or not end_date:
            raise ValueError("start_date and end_date are required for raw views export")
        
        params: Dict[str, Any] = {
            'date_time_from': self._format_datetime(start_date),
            'date_time_to': self._format_datetime(end_date),
            '_page': page,
            '_limit': limit
        }
        
        if content_id:
            params['content_id'] = content_id
        
        if content_type:
            endpoint = f'/v1/views/{content_type}'
        else:
            endpoint = '/v1/views'
        
        logger.info(f"Fetching raw views: {endpoint}")
        response = self.client.analytics_get(endpoint, params=params)
        
        return response
    
    # Legacy method names for backward compatibility
    def get_current_viewers(self, channel_id: str) -> Dict[str, Any]:
        """Get current viewer count (uses peak viewers endpoint)."""
        logger.info(f"Fetching current viewers for channel: {channel_id}")
        # Use peak viewers for last hour as approximation
        return self.get_peak_viewers(
            channel_id,
            start_date=datetime.utcnow() - timedelta(hours=1),
            granularity='minute'
        )
    
    def get_stream_health(self, channel_id: str) -> Dict[str, Any]:
        """Get stream health metrics (not available in Analytics API v1)."""
        logger.warning("Stream health endpoint not available in Analytics API v1")
        return {'status': 'unknown', 'message': 'Stream health not available in Analytics API v1'}
    
    def get_viewer_demographics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get viewer demographics (country, device)."""
        logger.info(f"Fetching viewer demographics for channel: {channel_id}")
        # Get country and device dimensions
        country_data = self.get_total_views(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            end_date=end_date,
            dimension='country'
        )
        device_data = self.get_total_views(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            end_date=end_date,
            dimension='device'
        )
        return {
            'countries': country_data.get('data', []),
            'devices': device_data.get('data', [])
        }
    
    def get_engagement_metrics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get engagement metrics (not directly available in Analytics API v1)."""
        logger.warning("Engagement metrics endpoint not available in Analytics API v1")
        return {'message': 'Engagement metrics not available in Analytics API v1'}
    
    def export_metrics(
        self,
        channel_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        format: str = 'json'
    ) -> Dict[str, Any]:
        """Export metrics data (uses raw views export)."""
        logger.info(f"Exporting metrics for channel {channel_id} as {format}")
        return self.get_raw_views(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )


# Global analytics manager instance
analytics_manager = AnalyticsManager()

# Made with Bob
