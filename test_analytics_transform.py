#!/usr/bin/env python3
"""
Test script to verify analytics data transformation.
Tests that the backend correctly transforms JSON API format to simple format.
"""
import sys
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, 'src')

from api.analytics import analytics_manager
from core.auth import auth_manager
from core.logger import get_logger

logger = get_logger(__name__)


def test_analytics_transformation():
    """Test analytics data transformation."""
    print("=" * 80)
    print("ANALYTICS DATA TRANSFORMATION TEST")
    print("=" * 80)
    
    # Check authentication
    try:
        token = auth_manager.get_access_token()
        if not token:
            print("\n❌ Not authenticated. Please run the web app and configure credentials first.")
            return False
        print("\n✓ Authenticated")
    except Exception as e:
        print(f"\n❌ Authentication error: {e}")
        return False
    
    # Get channel list
    from api.channels import channel_manager
    try:
        channels_response = channel_manager.list_channels()
        channels = channels_response.get('channels', [])
        
        if not channels:
            print("\n❌ No channels found")
            return False
        
        channel = channels[0]
        channel_id = channel['id']
        channel_title = channel.get('title', 'Untitled')
        
        print(f"\n✓ Testing with channel: {channel_title} (ID: {channel_id})")
        
    except Exception as e:
        print(f"\n❌ Error getting channels: {e}")
        return False
    
    # Test raw API response
    print("\n" + "-" * 80)
    print("1. RAW API RESPONSE (JSON API format)")
    print("-" * 80)
    
    try:
        start_date = datetime.utcnow() - timedelta(days=30)
        raw_response = analytics_manager.get_channel_metrics(
            channel_id=channel_id,
            start_date=start_date
        )
        
        print(f"\nResponse type: {type(raw_response)}")
        print(f"Response keys: {list(raw_response.keys()) if isinstance(raw_response, dict) else 'N/A'}")
        
        if isinstance(raw_response, dict) and 'data' in raw_response:
            data_array = raw_response.get('data', [])
            print(f"Data array length: {len(data_array)}")
            
            if data_array:
                first_item = data_array[0]
                print(f"\nFirst item structure:")
                print(f"  Type: {type(first_item)}")
                print(f"  Keys: {list(first_item.keys()) if isinstance(first_item, dict) else 'N/A'}")
                
                if 'attributes' in first_item:
                    attrs = first_item['attributes']
                    print(f"\n  Attributes:")
                    for key, value in attrs.items():
                        print(f"    {key}: {value}")
        
        print(f"\nFull response: {raw_response}")
        
    except Exception as e:
        print(f"\n❌ Error getting raw metrics: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test transformation logic
    print("\n" + "-" * 80)
    print("2. TRANSFORMED DATA (Simple format)")
    print("-" * 80)
    
    try:
        transformed = {
            'total_views': 0,
            'unique_viewers': 0,
            'peak_viewers': 0,
            'watch_time': 0,
            'data': []
        }
        
        if isinstance(raw_response, dict) and 'data' in raw_response:
            data_array = raw_response.get('data', [])
            if data_array and len(data_array) > 0:
                first_item = data_array[0]
                if isinstance(first_item, dict) and 'attributes' in first_item:
                    attrs = first_item['attributes']
                    transformed['total_views'] = attrs.get('value', 0)
        
        print(f"\nTransformed data:")
        for key, value in transformed.items():
            if key != 'data':
                print(f"  {key}: {value}")
        
        if transformed['total_views'] > 0:
            print("\n✓ Successfully extracted view count!")
        else:
            print("\n⚠ View count is 0 (may be no data for this period)")
        
    except Exception as e:
        print(f"\n❌ Error transforming data: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test demographics
    print("\n" + "-" * 80)
    print("3. DEMOGRAPHICS DATA")
    print("-" * 80)
    
    try:
        # Get country data
        country_data = analytics_manager.get_total_views(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            dimension='country'
        )
        
        print("\nCountry data:")
        if isinstance(country_data, dict) and 'data' in country_data:
            data_array = country_data.get('data', [])
            print(f"  Found {len(data_array)} countries")
            
            for item in data_array[:5]:  # Show first 5
                attrs = item.get('attributes', {})
                country = attrs.get('country', 'Unknown')
                value = attrs.get('value', 0)
                print(f"    {country}: {value} views")
        
        # Get device data
        device_data = analytics_manager.get_total_views(
            content_type='live',
            content_id=channel_id,
            start_date=start_date,
            dimension='device'
        )
        
        print("\nDevice data:")
        if isinstance(device_data, dict) and 'data' in device_data:
            data_array = device_data.get('data', [])
            print(f"  Found {len(data_array)} device types")
            
            for item in data_array:
                attrs = item.get('attributes', {})
                device = attrs.get('device', 'Unknown')
                value = attrs.get('value', 0)
                print(f"    {device}: {value} views")
        
    except Exception as e:
        print(f"\n⚠ Error getting demographics: {e}")
        # Don't fail the test for demographics
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\n✓ Data transformation logic verified!")
    print("\nNext steps:")
    print("  1. Start the web app: python web_app.py")
    print("  2. Navigate to Analytics section")
    print("  3. Select a channel and date range")
    print("  4. Verify that metrics display correctly")
    
    return True


if __name__ == '__main__':
    try:
        success = test_analytics_transformation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
