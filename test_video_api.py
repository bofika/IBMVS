#!/usr/bin/env python3
"""
Test script to check video API response structure.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.videos import video_manager
from api.channels import channel_manager
from core.logger import get_logger
import json

logger = get_logger(__name__)

def test_video_api():
    """Test video API response."""
    try:
        # Get first channel
        print("Fetching channels...")
        channels_response = channel_manager.list_channels()
        channels = channels_response.get('channels', [])
        
        if not channels:
            print("No channels found")
            return
        
        channel_id = channels[0].get('id')
        print(f"\nTesting with channel: {channel_id}")
        print(f"Channel title: {channels[0].get('title')}")
        
        # Get videos for this channel
        print(f"\nFetching videos for channel {channel_id}...")
        videos_response = video_manager.list_videos(channel_id)
        
        print("\n=== FULL API RESPONSE ===")
        print(json.dumps(videos_response, indent=2))
        
        videos = videos_response.get('videos', [])
        print(f"\n=== FOUND {len(videos)} VIDEOS ===")
        
        if videos:
            print("\n=== FIRST VIDEO DETAILS ===")
            first_video = videos[0]
            print(json.dumps(first_video, indent=2))
            
            print("\n=== VIDEO FIELDS ===")
            for key in sorted(first_video.keys()):
                value = first_video[key]
                print(f"{key}: {value} (type: {type(value).__name__})")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\nError: {e}")

if __name__ == '__main__':
    test_video_api()

# Made with Bob
