"""
Channel management API operations.
"""
from typing import List, Dict, Any, Optional

from api.client import client
from core.logger import get_logger
from utils.validators import validate_channel_title, validate_description

logger = get_logger(__name__)


class ChannelManager:
    """Manages channel-related API operations."""
    
    def __init__(self):
        self.client = client
    
    def list_channels(
        self,
        page: int = 1,
        page_size: int = 50,
        search_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of channels for the authenticated user.
        
        Args:
            page: Page number (1-based)
            page_size: Number of items per page
            search_query: Optional search query
            
        Returns:
            Dictionary containing channels list and pagination info
        """
        params: Dict[str, Any] = {
            'p': page,
            'pagesize': page_size
        }
        
        if search_query:
            params['q'] = search_query
        
        logger.info(f"Fetching channels (page {page}, size {page_size})")
        response = self.client.get('/users/self/channels.json', params=params)
        
        return response
    
    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Channel details
        """
        logger.info(f"Fetching channel details: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}.json')
        
        return response.get('channel', {})
    
    def create_channel(
        self,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new channel.
        
        Args:
            title: Channel title
            description: Channel description
            tags: List of tags
            
        Returns:
            Created channel details
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate inputs
        is_valid, error = validate_channel_title(title)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid channel title")
        
        is_valid, error = validate_description(description)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid description")
        
        data: Dict[str, Any] = {
            'title': title,
            'description': description
        }
        
        if tags:
            data['tags'] = tags
        
        logger.info(f"Creating channel: {title}")
        response = self.client.post('/users/self/channels.json', json=data)
        
        return response.get('channel', {})
    
    def update_channel(
        self,
        channel_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing channel.
        
        Args:
            channel_id: Channel ID
            title: New title (optional)
            description: New description (optional)
            tags: New tags (optional)
            
        Returns:
            Updated channel details
            
        Raises:
            ValidationError: If validation fails
        """
        data: Dict[str, Any] = {}
        
        if title is not None:
            is_valid, error = validate_channel_title(title)
            if not is_valid:
                from api.exceptions import ValidationError
                raise ValidationError(error or "Invalid channel title")
            data['title'] = title
        
        if description is not None:
            is_valid, error = validate_description(description)
            if not is_valid:
                from api.exceptions import ValidationError
                raise ValidationError(error or "Invalid description")
            data['description'] = description
        
        if tags is not None:
            data['tags'] = tags
        
        if not data:
            logger.warning("No data to update")
            return self.get_channel(channel_id)
        
        logger.info(f"Updating channel: {channel_id}")
        response = self.client.put(f'/channels/{channel_id}.json', json=data)
        
        return response.get('channel', {})
    
    def delete_channel(self, channel_id: str) -> bool:
        """
        Delete a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            True if deletion was successful
        """
        logger.info(f"Deleting channel: {channel_id}")
        self.client.delete(f'/channels/{channel_id}.json')
        
        return True
    
    def get_channel_settings(self, channel_id: str) -> Dict[str, Any]:
        """
        Get channel settings.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Channel settings
        """
        logger.info(f"Fetching channel settings: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/settings.json')
        
        return response.get('settings', {})
    
    def update_channel_settings(
        self,
        channel_id: str,
        settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update channel settings.
        
        Args:
            channel_id: Channel ID
            settings: Settings to update
            
        Returns:
            Updated settings
        """
        logger.info(f"Updating channel settings: {channel_id}")
        response = self.client.put(
            f'/channels/{channel_id}/settings.json',
            json=settings
        )
        
        return response.get('settings', {})
    
    def get_broadcast_settings(self, channel_id: str) -> Dict[str, Any]:
        """
        Get broadcast settings for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Broadcast settings
        """
        logger.info(f"Fetching broadcast settings: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/settings/broadcast.json')
        
        return response.get('broadcast', {})
    
    def update_broadcast_settings(
        self,
        channel_id: str,
        settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update broadcast settings.
        
        Args:
            channel_id: Channel ID
            settings: Broadcast settings to update
            
        Returns:
            Updated broadcast settings
        """
        logger.info(f"Updating broadcast settings: {channel_id}")
        response = self.client.put(
            f'/channels/{channel_id}/settings/broadcast.json',
            json=settings
        )
        
        return response.get('broadcast', {})


# Global channel manager instance
channel_manager = ChannelManager()

# Made with Bob
