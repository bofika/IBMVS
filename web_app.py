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
    """Get list of videos for a channel."""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 50, type=int)
        search = request.args.get('search', None)
        
        response = video_manager.list_videos(
            channel_id,
            page=page,
            page_size=page_size,
            search_query=search,
            include_private=True
        )
        return jsonify(response)
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
        
        video_manager.set_video_protection(video_id, is_private)
        return jsonify({'success': True, 'message': 'Video protection updated'})
    except Exception as e:
        logger.error(f"Error updating video {video_id} protection: {e}")
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
            
            auth_manager.save_credentials(client_id, client_secret)
            return jsonify({'success': True, 'message': 'Credentials saved'})
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


if __name__ == '__main__':
    logger.info("Starting IBM Video Streaming Manager Web Application")
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
