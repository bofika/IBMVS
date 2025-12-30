"""
Player configuration API operations.
"""
from typing import Dict, Any, Optional

from api.client import client
from core.logger import get_logger
from utils.validators import validate_color_hex
from utils.helpers import generate_embed_code

logger = get_logger(__name__)


class PlayerManager:
    """Manages player configuration API operations."""
    
    def __init__(self):
        self.client = client
    
    def get_player_settings(self, channel_id: str) -> Dict[str, Any]:
        """
        Get player configuration for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Player settings
        """
        logger.info(f"Fetching player settings for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/settings/player.json')
        
        return response.get('player', {})
    
    def update_player_settings(
        self,
        channel_id: str,
        autoplay: Optional[bool] = None,
        controls: Optional[bool] = None,
        responsive: Optional[bool] = None,
        color_scheme: Optional[str] = None,
        primary_color: Optional[str] = None,
        logo_url: Optional[str] = None,
        logo_position: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update player configuration.
        
        Args:
            channel_id: Channel ID
            autoplay: Enable autoplay
            controls: Show player controls
            responsive: Make player responsive
            color_scheme: Color scheme ('light' or 'dark')
            primary_color: Primary color (hex code)
            logo_url: Logo image URL
            logo_position: Logo position ('top-left', 'top-right', etc.)
            
        Returns:
            Updated player settings
            
        Raises:
            ValidationError: If validation fails
        """
        data: Dict[str, Any] = {}
        
        if autoplay is not None:
            data['autoplay'] = autoplay
        
        if controls is not None:
            data['controls'] = controls
        
        if responsive is not None:
            data['responsive'] = responsive
        
        if color_scheme is not None:
            if color_scheme not in ['light', 'dark']:
                from api.exceptions import ValidationError
                raise ValidationError("Color scheme must be 'light' or 'dark'")
            data['color_scheme'] = color_scheme
        
        if primary_color is not None:
            is_valid, error = validate_color_hex(primary_color)
            if not is_valid:
                from api.exceptions import ValidationError
                raise ValidationError(error or "Invalid color code")
            data['primary_color'] = primary_color
        
        if logo_url is not None:
            data['logo_url'] = logo_url
        
        if logo_position is not None:
            valid_positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right']
            if logo_position not in valid_positions:
                from api.exceptions import ValidationError
                raise ValidationError(f"Logo position must be one of: {', '.join(valid_positions)}")
            data['logo_position'] = logo_position
        
        if not data:
            logger.warning("No data to update")
            return self.get_player_settings(channel_id)
        
        logger.info(f"Updating player settings for channel: {channel_id}")
        response = self.client.put(
            f'/channels/{channel_id}/settings/player.json',
            json=data
        )
        
        return response.get('player', {})
    
    def get_embed_code(
        self,
        channel_id: str,
        width: int = 640,
        height: int = 360,
        responsive: bool = True
    ) -> str:
        """
        Get HTML embed code for a channel.
        
        Args:
            channel_id: Channel ID
            width: Player width in pixels
            height: Player height in pixels
            responsive: Make player responsive
            
        Returns:
            HTML embed code
        """
        logger.info(f"Generating embed code for channel: {channel_id}")
        
        # Try to get from API first
        try:
            params: Dict[str, Any] = {
                'width': width,
                'height': height,
                'responsive': responsive
            }
            response = self.client.get(
                f'/channels/{channel_id}/embed.json',
                params=params
            )
            return response.get('embed_code', '')
        except Exception as e:
            logger.warning(f"Failed to get embed code from API: {e}")
            # Fallback to generating locally
            return generate_embed_code(channel_id, width, height, responsive)
    
    def reset_player_settings(self, channel_id: str) -> Dict[str, Any]:
        """
        Reset player settings to defaults.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Default player settings
        """
        logger.info(f"Resetting player settings for channel: {channel_id}")
        
        default_settings = {
            'autoplay': False,
            'controls': True,
            'responsive': True,
            'color_scheme': 'dark'
        }
        
        return self.update_player_settings(
            channel_id,
            **default_settings
        )
    
    def preview_player(self, channel_id: str) -> str:
        """
        Get player preview URL.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Preview URL
        """
        return f"https://video.ibm.com/embed/{channel_id}"


# Global player manager instance
player_manager = PlayerManager()

# Made with Bob
