#!/usr/bin/env python3
"""
Test script to understand Analytics API response structure.
"""
import sys
sys.path.insert(0, 'src')

from datetime import datetime, timedelta
from api.analytics import analytics_manager
from api.channels import channel_manager
import json

print("=" * 70)
print("Analytics API Response Structure Test")
print("=" * 70)

# Get a channel to test with
print("\n1. Fetching channels...")
try:
    channels_response = channel_manager.list_channels(page=1, page_size=5)
    channels = channels_response.get('channels', [])
    
    if not channels:
        print("❌ No channels found")
        sys.exit(1)
    
    channel = channels[0]
    channel_id = channel.get('id')
    channel_title = channel.get('title', 'Untitled')
    
    print(f"✓ Testing with channel: {channel_title} (ID: {channel_id})")
except Exception as e:
    print(f"❌ Error fetching channels: {e}")
    sys.exit(1)

# Test different date ranges and content types
test_cases = [
    {"name": "Last 7 days - Live", "days": 7, "content_type": "live"},
    {"name": "Last 30 days - Live", "days": 30, "content_type": "live"},
    {"name": "Last 90 days - Live", "days": 90, "content_type": "live"},
    {"name": "Last 30 days - Recorded", "days": 30, "content_type": "recorded"},
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. Testing: {test['name']}")
    print("-" * 70)
    
    try:
        start_date = datetime.utcnow() - timedelta(days=test['days'])
        
        if test['content_type'] == 'live':
            response = analytics_manager.get_channel_metrics(
                channel_id=channel_id,
                start_date=start_date
            )
        else:
            response = analytics_manager.get_total_views(
                content_type='recorded',
                content_id=channel_id,
                start_date=start_date
            )
        
        print(f"✓ API call successful")
        print(f"Response type: {type(response)}")
        
        if isinstance(response, dict):
            print(f"Response keys: {list(response.keys())}")
            
            # Check for data array
            if 'data' in response:
                data = response['data']
                print(f"Data type: {type(data)}")
                print(f"Data length: {len(data) if isinstance(data, list) else 'N/A'}")
                
                if isinstance(data, list) and len(data) > 0:
                    print(f"First item keys: {list(data[0].keys())}")
                    print(f"First item sample:")
                    print(json.dumps(data[0], indent=2))
                elif isinstance(data, list):
                    print("⚠️  Data array is empty")
                else:
                    print(f"Data content: {data}")
            
            # Check for pagination
            if 'pagination' in response:
                print(f"Pagination: {response['pagination']}")
            
            # Print full response if small
            if len(str(response)) < 1000:
                print(f"\nFull response:")
                print(json.dumps(response, indent=2))
        else:
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Test demographics
print(f"\n5. Testing Demographics")
print("-" * 70)
try:
    start_date = datetime.utcnow() - timedelta(days=30)
    demographics = analytics_manager.get_viewer_demographics(
        channel_id=channel_id,
        start_date=start_date
    )
    
    print(f"✓ Demographics call successful")
    print(f"Response type: {type(demographics)}")
    
    if isinstance(demographics, dict):
        print(f"Response keys: {list(demographics.keys())}")
        
        if 'countries' in demographics:
            countries = demographics['countries']
            print(f"Countries count: {len(countries) if isinstance(countries, list) else 'N/A'}")
            if isinstance(countries, list) and len(countries) > 0:
                print(f"First country: {countries[0]}")
        
        if 'devices' in demographics:
            devices = demographics['devices']
            print(f"Devices count: {len(devices) if isinstance(devices, list) else 'N/A'}")
            if isinstance(devices, list) and len(devices) > 0:
                print(f"First device: {devices[0]}")
        
        # Print full response if small
        if len(str(demographics)) < 1000:
            print(f"\nFull demographics response:")
            print(json.dumps(demographics, indent=2))
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)

# Made with Bob
