"""
Flask web application for IBM Video Streaming Manager.
"""
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS

from api.channels import channel_manager
from api.videos import video_manager
from api.players import player_manager
from api.interactivity import interactivity_manager
from api.analytics import analytics_manager
from core.auth import auth_manager
from core.config import config
from core.logger import get_logger

logger = get_logger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10GB max file size


@app.route('/')
def index():
    """Main page."""
    if not auth_manager.has_credentials():
        return redirect(url_for('settings'))
    return render_template('index.html')


@app.route('/settings')
def settings():
    """Settings page."""
    return render_template('settings.html')


# API Routes - Channels
@app.route('/api/channels')
def api_channels():
    """Get list of channels."""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 50, type=int)
        
        response = channel_manager.list_channels(page=page, page_size=page_size)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error fetching channels: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/channels/<channel_id>')
def api_channel_details(channel_id):
    """Get channel details."""
    try:
        channel = channel_manager.get_channel(channel_id)
        return jsonify(channel)
    except Exception as e:
        logger.error(f"Error fetching channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


# API Routes - Videos
@app.route('/api/channels/<channel_id>/videos')
def api_videos(channel_id):
    """Get list of videos for a channel with smart pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 50, type=int)
        search = request.args.get('search', None)
        
        # IBM API has a hard limit of 50 videos per request
        # If user wants more, we need to make multiple requests
        IBM_API_MAX_PAGE_SIZE = 50
        
        if page_size <= IBM_API_MAX_PAGE_SIZE:
            # Single request is enough
            response = video_manager.list_videos(
                channel_id,
                page=page,
                page_size=page_size,
                search_query=search,
                include_private=True
            )
            # Normalize the response to use 'total' field for consistency
            if 'paging' in response:
                paging = response['paging']
                if 'item_count' in paging and 'total' not in paging:
                    paging['total'] = paging['item_count']
            return jsonify(response)
        else:
            # Need multiple requests to fetch all videos
            # Calculate how many API calls we need
            num_requests = (page_size + IBM_API_MAX_PAGE_SIZE - 1) // IBM_API_MAX_PAGE_SIZE
            
            # Calculate which IBM API pages we need to fetch
            # For example: if user wants page 1 with 200 videos per page,
            # we need IBM API pages 1, 2, 3, 4 (each with 50 videos)
            start_api_page = ((page - 1) * page_size) // IBM_API_MAX_PAGE_SIZE + 1
            
            all_videos = []
            total_count = 0
            paging_info = {}
            
            logger.info(f"Fetching {page_size} videos for page {page}: making {num_requests} API calls starting from API page {start_api_page}")
            
            for i in range(num_requests):
                api_page = start_api_page + i
                try:
                    response = video_manager.list_videos(
                        channel_id,
                        page=api_page,
                        page_size=IBM_API_MAX_PAGE_SIZE,
                        search_query=search,
                        include_private=True
                    )
                    
                    videos = response.get('videos', [])
                    all_videos.extend(videos)
                    
                    # Get total count from first response
                    # IBM API uses 'item_count' not 'total'
                    if i == 0:
                        paging_info = response.get('paging', {})
                        total_count = paging_info.get('item_count', paging_info.get('total', 0))
                    
                    # Stop if we got fewer videos than requested (last page)
                    if len(videos) < IBM_API_MAX_PAGE_SIZE:
                        break
                        
                except Exception as e:
                    logger.error(f"Error fetching API page {api_page}: {e}")
                    # Continue with what we have
                    break
            
            # Trim to exact page size if we got more
            all_videos = all_videos[:page_size]
            
            # Build response in same format as single request
            combined_response = {
                'videos': all_videos,
                'paging': {
                    'total': total_count,
                    'item_count': total_count,
                    'page': page,
                    'pagesize': page_size,
                    'actual_count': len(all_videos)
                }
            }
            
            logger.info(f"Combined response: {len(all_videos)} videos out of {total_count} total")
            return jsonify(combined_response)
            
    except Exception as e:
        logger.error(f"Error fetching videos for channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/videos/<video_id>')
def api_video_details(video_id):
    """Get video details."""
    try:
        video = video_manager.get_video(video_id)
        return jsonify(video)
    except Exception as e:
        logger.error(f"Error fetching video {video_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/videos/<video_id>/protection', methods=['PUT'])
def api_video_protection(video_id):
    """Update video protection status."""
    try:
        data = request.get_json()
        is_private = data.get('is_private', False)
        
        logger.info(f"Received request to set video {video_id} to {'private' if is_private else 'public'}")
        logger.info(f"Request data: {data}")
        
        # Call updated method that returns detailed response
        result = video_manager.set_video_protection(video_id, is_private)
        
        requested_status = result.get('requested_status', 'unknown')
        actual_status = result.get('actual_status', 'unknown')
        status_changed = (actual_status == requested_status)
        
        logger.info(f"Video {video_id} - Requested: {requested_status}, Actual: {actual_status}, Changed: {status_changed}")
        
        # Return detailed status for confirmation
        return jsonify({
            'success': result.get('success', False),
            'message': f'Video is now {actual_status}' if status_changed else f'Status change failed. Video remains {actual_status}',
            'video_id': video_id,
            'is_private': is_private,
            'requested_status': requested_status,
            'actual_status': actual_status,
            'status_changed': status_changed,
            'protect': actual_status
        })
    except Exception as e:
        logger.error(f"Error updating video {video_id} protection: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# API Routes - Authentication
@app.route('/api/auth/credentials', methods=['GET', 'POST'])
def api_credentials():
    """Get or set credentials."""
    if request.method == 'POST':
        try:
            data = request.get_json()
            client_id = data.get('client_id')
            client_secret = data.get('client_secret')
            
            if not client_id or not client_secret:
                return jsonify({'error': 'Missing credentials'}), 400
            
            # Use set_credentials method (not save_credentials)
            success = auth_manager.set_credentials(client_id, client_secret, save=True)
            if success:
                return jsonify({'success': True, 'message': 'Credentials saved successfully'})
            else:
                return jsonify({'error': 'Failed to save credentials'}), 500
        except Exception as e:
            logger.error(f"Error saving credentials: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        has_creds = auth_manager.has_credentials()
        return jsonify({'has_credentials': has_creds})


@app.route('/api/auth/test', methods=['POST'])
def api_test_auth():
    """Test API connection."""
    try:
        # Try to fetch channels to test connection
        response = channel_manager.list_channels(page=1, page_size=1)
        return jsonify({'success': True, 'message': 'Connection successful'})
    except Exception as e:
        logger.error(f"Error testing connection: {e}")
        return jsonify({'error': str(e)}), 500


# API Routes - Players
@app.route('/api/channels/<channel_id>/player')
def api_player_settings(channel_id):
    """Get player settings for a channel."""
    try:
        settings = player_manager.get_player_settings(channel_id)
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Error fetching player settings for channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


# API Routes - Interactive
@app.route('/api/channels/<channel_id>/chat')
def api_chat_settings(channel_id):
    """Get chat settings for a channel."""
    try:
        settings = interactivity_manager.get_chat_settings(channel_id)
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Error fetching chat settings for channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


# API Routes - Analytics
@app.route('/api/channels/<channel_id>/viewers')
def api_viewers(channel_id):
    """Get current viewers for a channel."""
    try:
        viewers = analytics_manager.get_current_viewers(channel_id)
        return jsonify(viewers)
    except Exception as e:
        logger.error(f"Error fetching viewers for channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/channels/<channel_id>/metrics')
def api_channel_analytics(channel_id):
    """Get analytics metrics for a channel."""
    try:
        from datetime import datetime, timedelta
        
        # Get date range from query parameters
        days = request.args.get('days', 7, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        metrics = analytics_manager.get_channel_metrics(
            channel_id=channel_id,
            start_date=start_date
        )
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error fetching analytics for channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/channels/<channel_id>/demographics')
def api_channel_demographics(channel_id):
    """Get viewer demographics for a channel."""
    try:
        from datetime import datetime, timedelta
        
        days = request.args.get('days', 7, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        demographics = analytics_manager.get_viewer_demographics(
            channel_id=channel_id,
            start_date=start_date
        )
        return jsonify(demographics)
    except Exception as e:
        logger.error(f"Error fetching demographics for channel {channel_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/videos/<video_id>/metrics')
def api_video_analytics(video_id):
    """Get analytics metrics for a video."""
    try:
        from datetime import datetime, timedelta
        
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        metrics = analytics_manager.get_video_metrics(
            video_id=video_id,
            start_date=start_date
        )
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error fetching analytics for video {video_id}: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting IBM Video Streaming Manager Web Application")
    app.run(debug=True, host='0.0.0.0', port=8080)

# Made with Bob
