#!/usr/bin/env python3
"""
Test script to verify channel pagination.
Tests that all 189 channels can be retrieved through pagination.
"""
import sys

# Add src to path
sys.path.insert(0, 'src')

from api.channels import channel_manager
from core.auth import auth_manager
from core.logger import get_logger

logger = get_logger(__name__)


def test_channel_pagination():
    """Test channel pagination to load all channels."""
    print("=" * 80)
    print("CHANNEL PAGINATION TEST")
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
    
    # Test pagination
    print("\n" + "-" * 80)
    print("FETCHING ALL CHANNELS")
    print("-" * 80)
    
    all_channels = []
    page = 1
    page_size = 50
    total_count = 0
    
    while True:
        print(f"\nFetching page {page} (page_size={page_size})...")
        
        try:
            response = channel_manager.list_channels(page=page, page_size=page_size)
            
            # Get channels
            channels = response.get('channels', [])
            print(f"  Received {len(channels)} channels on this page")
            
            # Get paging info
            paging = response.get('paging', {})
            print(f"  Paging info: {paging}")
            
            # Get total count from first page
            if page == 1:
                total_count = paging.get('item_count', paging.get('total', 0))
                print(f"  Total channels in account: {total_count}")
            
            # Add to collection
            all_channels.extend(channels)
            print(f"  Total channels collected so far: {len(all_channels)}")
            
            # Check if we should continue
            if len(channels) < page_size:
                print(f"  Last page reached (got {len(channels)} < {page_size})")
                break
            
            if len(all_channels) >= total_count and total_count > 0:
                print(f"  All channels collected ({len(all_channels)} >= {total_count})")
                break
            
            # Continue to next page
            page += 1
            
            # Safety limit
            if page > 10:
                print(f"  Safety limit reached (page {page})")
                break
                
        except Exception as e:
            print(f"\n❌ Error fetching page {page}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total channels expected: {total_count}")
    print(f"Total channels collected: {len(all_channels)}")
    print(f"Pages fetched: {page}")
    
    if len(all_channels) == total_count:
        print(f"\n✓ SUCCESS: All {total_count} channels retrieved!")
    else:
        print(f"\n⚠ WARNING: Expected {total_count} but got {len(all_channels)} channels")
    
    # Show sample channels
    if all_channels:
        print(f"\nFirst 5 channels:")
        for i, channel in enumerate(all_channels[:5], 1):
            print(f"  {i}. {channel.get('title', 'Untitled')} (ID: {channel.get('id')})")
        
        if len(all_channels) > 5:
            print(f"\nLast 5 channels:")
            for i, channel in enumerate(all_channels[-5:], len(all_channels) - 4):
                print(f"  {i}. {channel.get('title', 'Untitled')} (ID: {channel.get('id')})")
    
    return len(all_channels) == total_count


if __name__ == '__main__':
    try:
        success = test_channel_pagination()
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
