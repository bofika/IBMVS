"""
Video management API operations.
"""
import os
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

from api.client import client
from core.logger import get_logger
from utils.validators import validate_video_title, validate_description, validate_video_file
from utils.helpers import format_file_size
from utils.constants import CHUNK_SIZE

logger = get_logger(__name__)


class VideoManager:
    """Manages video-related API operations."""
    
    def __init__(self):
        self.client = client
    
    def list_videos(
        self,
        channel_id: str,
        page: int = 1,
        page_size: int = 50,
        search_query: Optional[str] = None,
        include_private: bool = True
    ) -> Dict[str, Any]:
        """
        Get list of videos for a specific channel.
        
        Args:
            channel_id: Channel ID
            page: Page number (1-based)
            page_size: Number of items per page
            search_query: Optional search query
            include_private: Include private/unpublished videos (default: True)
            
        Returns:
            Dictionary containing videos list and pagination info
        """
        params: Dict[str, Any] = {
            'p': page,
            'pagesize': page_size
        }
        
        if search_query:
            params['q'] = search_query
        
        # Include both public and private videos by default (show all videos for management)
        # According to IBM API docs: filter[protect] can be "public", "private", or both comma-separated
        if include_private:
            params['filter[protect]'] = 'public,private'
        else:
            params['filter[protect]'] = 'public'
        
        logger.info(f"Fetching videos for channel {channel_id} (page {page}, include_private={include_private})")
        response = self.client.get(f'/channels/{channel_id}/videos.json', params=params)
        
        return response
    
    def get_video(self, video_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific video.
        
        Args:
            video_id: Video ID
            
        Returns:
            Video details
        """
        logger.info(f"Fetching video details: {video_id}")
        response = self.client.get(f'/videos/{video_id}.json')
        
        return response.get('video', {})
    
    def upload_video(
        self,
        channel_id: str,
        file_path: str,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Upload a video to a channel.
        
        Args:
            channel_id: Channel ID
            file_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            progress_callback: Optional callback for upload progress
            
        Returns:
            Upload response with video details
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate file
        is_valid, error = validate_video_file(file_path)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid video file")
        
        # Validate title
        is_valid, error = validate_video_title(title)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid video title")
        
        # Validate description
        is_valid, error = validate_description(description)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid description")
        
        file_path_obj = Path(file_path)
        file_size = file_path_obj.stat().st_size
        
        logger.info(f"Uploading video: {title} ({format_file_size(file_size)})")
        
        # Prepare form data
        data = {
            'title': title,
            'description': description
        }
        
        if tags:
            data['tags'] = ','.join(tags)
        
        # Open file and upload
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_path_obj.name, f, 'video/*')
            }
            
            response = self.client.post(
                f'/channels/{channel_id}/videos.json',
                data=data,
                files=files
            )
        
        logger.info(f"Video uploaded successfully: {response.get('video', {}).get('id')}")
        return response.get('video', {})
    
    def update_video(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update video metadata.
        
        Args:
            video_id: Video ID
            title: New title (optional)
            description: New description (optional)
            tags: New tags (optional)
            
        Returns:
            Updated video details
            
        Raises:
            ValidationError: If validation fails
        """
        data: Dict[str, Any] = {}
        
        if title is not None:
            is_valid, error = validate_video_title(title)
            if not is_valid:
                from api.exceptions import ValidationError
                raise ValidationError(error or "Invalid video title")
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
            return self.get_video(video_id)
        
        logger.info(f"Updating video: {video_id}")
        response = self.client.put(f'/videos/{video_id}.json', json=data)
        
        return response.get('video', {})
    
    def delete_video(self, video_id: str) -> bool:
        """
        Delete a video.
        
        Args:
            video_id: Video ID
            
        Returns:
            True if deletion was successful
        """
        logger.info(f"Deleting video: {video_id}")
        self.client.delete(f'/videos/{video_id}.json')
        
        return True
    
    def set_video_protection(self, video_id: str, is_private: bool) -> bool:
        """
        Set video protection status (public/private).
        
        Args:
            video_id: Video ID
            is_private: True for private, False for public
            
        Returns:
            True if successful
        """
        # API expects 'private' or 'public' as string values
        protection_value = 'private' if is_private else 'public'
        logger.info(f"Setting video {video_id} protection to: {protection_value}")
        
        response = self.client.put(
            f'/videos/{video_id}.json',
            json={'protect': protection_value}
        )
        
        # API might return different structures, just check if call succeeded
        logger.info(f"Video {video_id} protection updated successfully")
        return True
    
    def get_video_thumbnail(self, video_id: str) -> str:
        """
        Get video thumbnail URL.
        
        Args:
            video_id: Video ID
            
        Returns:
            Thumbnail URL
        """
        video = self.get_video(video_id)
        return video.get('thumbnail', '')
    
    def get_video_status(self, video_id: str) -> str:
        """
        Get video processing status.
        
        Args:
            video_id: Video ID
            
        Returns:
            Status string (processing, ready, error)
        """
        video = self.get_video(video_id)
        return video.get('status', 'unknown')
    
    def list_playlists(self, channel_id: str) -> List[Dict[str, Any]]:
        """
        Get list of playlists for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            List of playlists
        """
        logger.info(f"Fetching playlists for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/playlists.json')
        
        return response.get('playlists', [])
    
    def create_playlist(
        self,
        channel_id: str,
        title: str,
        description: str = "",
        video_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new playlist.
        
        Args:
            channel_id: Channel ID
            title: Playlist title
            description: Playlist description
            video_ids: List of video IDs to add
            
        Returns:
            Created playlist details
        """
        data: Dict[str, Any] = {
            'title': title,
            'description': description
        }
        
        if video_ids:
            data['videos'] = video_ids
        
        logger.info(f"Creating playlist: {title}")
        response = self.client.post(
            f'/channels/{channel_id}/playlists.json',
            json=data
        )
        
        return response.get('playlist', {})
    
    def add_video_to_playlist(
        self,
        playlist_id: str,
        video_id: str
    ) -> bool:
        """
        Add a video to a playlist.
        
        Args:
            playlist_id: Playlist ID
            video_id: Video ID
            
        Returns:
            True if successful
        """
        logger.info(f"Adding video {video_id} to playlist {playlist_id}")
        self.client.post(
            f'/playlists/{playlist_id}/videos.json',
            json={'video_id': video_id}
        )
        
        return True
    
    def remove_video_from_playlist(
        self,
        playlist_id: str,
        video_id: str
    ) -> bool:
        """
        Remove a video from a playlist.
        
        Args:
            playlist_id: Playlist ID
            video_id: Video ID
            
        Returns:
            True if successful
        """
        logger.info(f"Removing video {video_id} from playlist {playlist_id}")
        self.client.delete(f'/playlists/{playlist_id}/videos/{video_id}.json')
        
        return True


# Global video manager instance
video_manager = VideoManager()

# Made with Bob
