"""
Test script for Analytics API with JWT authentication.

This script tests the JWT token authentication flow for the Analytics API.
"""
import sys
from datetime import datetime, timedelta

from core.auth import auth_manager
from core.logger import get_logger
from api.analytics import analytics_manager
from api.channels import channel_manager

logger = get_logger(__name__)


def test_jwt_authentication():
    """Test JWT token authentication."""
    print("=" * 70)
    print("Testing JWT Authentication for Analytics API")
    print("=" * 70)
    
    # Check if credentials are available
    if not auth_manager.has_credentials():
        print("❌ No credentials found!")
        print("Please set IBM_CLIENT_ID and IBM_CLIENT_SECRET environment variables")
        print("or configure them in the application settings.")
        return False
    
    print("✓ Credentials found")
    
    # Test standard OAuth token
    print("\n1. Testing standard OAuth token...")
    token = auth_manager.get_access_token()
    if token:
        print(f"✓ OAuth token obtained: {token[:20]}...")
    else:
        print("❌ Failed to obtain OAuth token")
        return False
    
    # Test JWT token
    print("\n2. Testing JWT token for Analytics API...")
    jwt_token = auth_manager.get_jwt_token()
    if jwt_token:
        print(f"✓ JWT token obtained: {jwt_token[:20]}...")
    else:
        print("❌ Failed to obtain JWT token")
        return False
    
    # Verify tokens are different
    if token != jwt_token:
        print("✓ JWT token is different from OAuth token (as expected)")
    else:
        print("⚠️  Warning: JWT token is same as OAuth token")
    
    print("\n" + "=" * 70)
    print("JWT Authentication Test: PASSED")
    print("=" * 70)
    return True


def test_analytics_api():
    """Test Analytics API endpoints."""
    print("\n" + "=" * 70)
    print("Testing Analytics API Endpoints")
    print("=" * 70)
    
    try:
        # Get channels first
        print("\n1. Fetching channels...")
        response = channel_manager.list_channels()
        channels = response.get('channels', [])
        
        if not channels:
            print("❌ No channels found")
            return False
        
        print(f"✓ Found {len(channels)} channel(s)")
        
        # Test with first channel
        channel = channels[0]
        channel_id = channel.get('id')
        channel_title = channel.get('title', 'Untitled')
        
        print(f"\nTesting with channel: {channel_title} (ID: {channel_id})")
        
        # Test channel metrics
        print("\n2. Testing get_channel_metrics()...")
        try:
            start_date = datetime.utcnow() - timedelta(days=7)
            metrics = analytics_manager.get_channel_metrics(
                channel_id,
                start_date=start_date
            )
            print(f"✓ Channel metrics retrieved")
            print(f"   Sample data: {list(metrics.keys())[:5]}")
        except Exception as e:
            print(f"⚠️  Channel metrics: {str(e)}")
        
        # Test current viewers
        print("\n3. Testing get_current_viewers()...")
        try:
            viewers = analytics_manager.get_current_viewers(channel_id)
            print(f"✓ Current viewers retrieved")
            print(f"   Current viewers: {viewers.get('current', 'N/A')}")
        except Exception as e:
            print(f"⚠️  Current viewers: {str(e)}")
        
        # Test stream health
        print("\n4. Testing get_stream_health()...")
        try:
            health = analytics_manager.get_stream_health(channel_id)
            print(f"✓ Stream health retrieved")
            print(f"   Status: {health.get('status', 'N/A')}")
        except Exception as e:
            print(f"⚠️  Stream health: {str(e)}")
        
        # Test demographics
        print("\n5. Testing get_viewer_demographics()...")
        try:
            demographics = analytics_manager.get_viewer_demographics(
                channel_id,
                start_date=start_date
            )
            print(f"✓ Demographics retrieved")
            print(f"   Sample data: {list(demographics.keys())[:3]}")
        except Exception as e:
            print(f"⚠️  Demographics: {str(e)}")
        
        # Test engagement
        print("\n6. Testing get_engagement_metrics()...")
        try:
            engagement = analytics_manager.get_engagement_metrics(
                channel_id,
                start_date=start_date
            )
            print(f"✓ Engagement metrics retrieved")
            print(f"   Sample data: {list(engagement.keys())[:3]}")
        except Exception as e:
            print(f"⚠️  Engagement metrics: {str(e)}")
        
        print("\n" + "=" * 70)
        print("Analytics API Test: COMPLETED")
        print("=" * 70)
        print("\nNote: Some endpoints may return errors if:")
        print("  - The channel has no analytics data yet")
        print("  - The Analytics API uses different endpoint URLs")
        print("  - Additional API permissions are required")
        print("\nCheck the IBM Video Streaming Analytics API documentation for")
        print("the exact endpoint URLs and required permissions.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Analytics API test failed: {e}")
        logger.error(f"Analytics API test failed: {e}", exc_info=True)
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("IBM Video Streaming Analytics API - JWT Authentication Test")
    print("=" * 70)
    
    # Test JWT authentication
    if not test_jwt_authentication():
        print("\n❌ JWT authentication test failed!")
        sys.exit(1)
    
    # Test Analytics API
    test_analytics_api()
    
    print("\n" + "=" * 70)
    print("All Tests Completed!")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Verify JWT token is working correctly")
    print("2. Check Analytics API endpoint URLs in IBM documentation")
    print("3. Update endpoint URLs if they differ from Channel API")
    print("4. Test with actual analytics data")
    print("\nFor more information, see:")
    print("https://github.com/IBM/video-streaming-developer-docs")


if __name__ == "__main__":
    main()

# Made with Bob
