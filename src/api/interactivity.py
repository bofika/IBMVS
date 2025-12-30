"""
Interactivity API operations (chat, polls, Q&A).
"""
from typing import List, Dict, Any, Optional

from api.client import client
from core.logger import get_logger
from utils.validators import validate_poll_question, validate_poll_options

logger = get_logger(__name__)


class InteractivityManager:
    """Manages interactivity features (chat, polls, Q&A)."""
    
    def __init__(self):
        self.client = client
    
    # Chat Management
    
    def get_chat_settings(self, channel_id: str) -> Dict[str, Any]:
        """
        Get chat settings for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Chat settings
        """
        logger.info(f"Fetching chat settings for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/settings/chat.json')
        
        return response.get('chat', {})
    
    def update_chat_settings(
        self,
        channel_id: str,
        enabled: Optional[bool] = None,
        moderation: Optional[str] = None,
        require_login: Optional[bool] = None,
        slow_mode: Optional[bool] = None,
        slow_mode_interval: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update chat settings.
        
        Args:
            channel_id: Channel ID
            enabled: Enable/disable chat
            moderation: Moderation mode ('auto', 'manual', 'off')
            require_login: Require login to chat
            slow_mode: Enable slow mode
            slow_mode_interval: Slow mode interval in seconds
            
        Returns:
            Updated chat settings
            
        Raises:
            ValidationError: If validation fails
        """
        data: Dict[str, Any] = {}
        
        if enabled is not None:
            data['enabled'] = enabled
        
        if moderation is not None:
            valid_modes = ['auto', 'manual', 'off']
            if moderation not in valid_modes:
                from api.exceptions import ValidationError
                raise ValidationError(f"Moderation must be one of: {', '.join(valid_modes)}")
            data['moderation'] = moderation
        
        if require_login is not None:
            data['require_login'] = require_login
        
        if slow_mode is not None:
            data['slow_mode'] = slow_mode
        
        if slow_mode_interval is not None:
            if slow_mode_interval < 0:
                from api.exceptions import ValidationError
                raise ValidationError("Slow mode interval must be non-negative")
            data['slow_mode_interval'] = slow_mode_interval
        
        if not data:
            logger.warning("No data to update")
            return self.get_chat_settings(channel_id)
        
        logger.info(f"Updating chat settings for channel: {channel_id}")
        response = self.client.put(
            f'/channels/{channel_id}/settings/chat.json',
            json=data
        )
        
        return response.get('chat', {})
    
    # Poll Management
    
    def list_polls(self, channel_id: str) -> List[Dict[str, Any]]:
        """
        Get list of polls for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            List of polls
        """
        logger.info(f"Fetching polls for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/polls.json')
        
        return response.get('polls', [])
    
    def get_poll(self, channel_id: str, poll_id: str) -> Dict[str, Any]:
        """
        Get details of a specific poll.
        
        Args:
            channel_id: Channel ID
            poll_id: Poll ID
            
        Returns:
            Poll details
        """
        logger.info(f"Fetching poll {poll_id} for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/polls/{poll_id}.json')
        
        return response.get('poll', {})
    
    def create_poll(
        self,
        channel_id: str,
        question: str,
        options: List[str],
        duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a new poll.
        
        Args:
            channel_id: Channel ID
            question: Poll question
            options: List of poll options (2-10)
            duration: Poll duration in seconds (optional)
            
        Returns:
            Created poll details
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate question
        is_valid, error = validate_poll_question(question)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid poll question")
        
        # Validate options
        is_valid, error = validate_poll_options(options)
        if not is_valid:
            from api.exceptions import ValidationError
            raise ValidationError(error or "Invalid poll options")
        
        data: Dict[str, Any] = {
            'question': question,
            'options': [{'text': opt} for opt in options]
        }
        
        if duration is not None:
            if duration <= 0:
                from api.exceptions import ValidationError
                raise ValidationError("Duration must be positive")
            data['duration'] = duration
        
        logger.info(f"Creating poll for channel: {channel_id}")
        response = self.client.post(
            f'/channels/{channel_id}/polls.json',
            json=data
        )
        
        return response.get('poll', {})
    
    def update_poll(
        self,
        channel_id: str,
        poll_id: str,
        question: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a poll.
        
        Args:
            channel_id: Channel ID
            poll_id: Poll ID
            question: New question (optional)
            status: New status ('active' or 'closed')
            
        Returns:
            Updated poll details
        """
        data: Dict[str, Any] = {}
        
        if question is not None:
            is_valid, error = validate_poll_question(question)
            if not is_valid:
                from api.exceptions import ValidationError
                raise ValidationError(error or "Invalid poll question")
            data['question'] = question
        
        if status is not None:
            if status not in ['active', 'closed']:
                from api.exceptions import ValidationError
                raise ValidationError("Status must be 'active' or 'closed'")
            data['status'] = status
        
        if not data:
            logger.warning("No data to update")
            return self.get_poll(channel_id, poll_id)
        
        logger.info(f"Updating poll {poll_id} for channel: {channel_id}")
        response = self.client.put(
            f'/channels/{channel_id}/polls/{poll_id}.json',
            json=data
        )
        
        return response.get('poll', {})
    
    def delete_poll(self, channel_id: str, poll_id: str) -> bool:
        """
        Delete a poll.
        
        Args:
            channel_id: Channel ID
            poll_id: Poll ID
            
        Returns:
            True if deletion was successful
        """
        logger.info(f"Deleting poll {poll_id} from channel: {channel_id}")
        self.client.delete(f'/channels/{channel_id}/polls/{poll_id}.json')
        
        return True
    
    def close_poll(self, channel_id: str, poll_id: str) -> Dict[str, Any]:
        """
        Close an active poll.
        
        Args:
            channel_id: Channel ID
            poll_id: Poll ID
            
        Returns:
            Updated poll details
        """
        return self.update_poll(channel_id, poll_id, status='closed')
    
    # Q&A Management
    
    def get_qa_settings(self, channel_id: str) -> Dict[str, Any]:
        """
        Get Q&A settings for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Q&A settings
        """
        logger.info(f"Fetching Q&A settings for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/settings/qa.json')
        
        return response.get('qa', {})
    
    def update_qa_settings(
        self,
        channel_id: str,
        enabled: Optional[bool] = None,
        moderation: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update Q&A settings.
        
        Args:
            channel_id: Channel ID
            enabled: Enable/disable Q&A
            moderation: Enable moderation
            
        Returns:
            Updated Q&A settings
        """
        data: Dict[str, Any] = {}
        
        if enabled is not None:
            data['enabled'] = enabled
        
        if moderation is not None:
            data['moderation'] = moderation
        
        if not data:
            logger.warning("No data to update")
            return self.get_qa_settings(channel_id)
        
        logger.info(f"Updating Q&A settings for channel: {channel_id}")
        response = self.client.put(
            f'/channels/{channel_id}/settings/qa.json',
            json=data
        )
        
        return response.get('qa', {})
    
    def list_questions(self, channel_id: str) -> List[Dict[str, Any]]:
        """
        Get list of Q&A questions for a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            List of questions
        """
        logger.info(f"Fetching Q&A questions for channel: {channel_id}")
        response = self.client.get(f'/channels/{channel_id}/qa/questions.json')
        
        return response.get('questions', [])


# Global interactivity manager instance
interactivity_manager = InteractivityManager()

# Made with Bob
