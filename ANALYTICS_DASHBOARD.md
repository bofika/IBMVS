# Analytics Dashboard Documentation

## Overview

The Analytics Dashboard provides comprehensive analytics and monitoring capabilities for IBM Video Streaming channels, videos, and live streams. It uses JWT (JSON Web Token) authentication to access the Analytics API, which is separate from the standard Channel API.

## Key Features

### 📺 Channel Analytics
- **Total Views**: Track total views across selected date range
- **Unique Viewers**: Count of unique viewers
- **Watch Time**: Total and average watch time metrics
- **Peak Concurrent Viewers**: Maximum simultaneous viewers
- **Engagement Metrics**: Chat activity, poll participation, Q&A engagement
- **Demographics**: Geographic distribution and device breakdown
- **Date Range Selection**: Flexible date range with quick presets

### 🎬 Video Analytics
- **Video Performance**: Views, completion rate, average duration
- **Engagement**: Likes, shares, comments
- **Retention Analysis**: Viewer retention throughout video
- **Traffic Sources**: Where viewers are coming from
- **Video Selection**: Analyze any video from your channels

### 🔴 Live Stream Monitor
- **Real-time Viewer Count**: Current viewers updated in real-time
- **Stream Status**: Live/Offline status with health indicators
- **Stream Health**: Quality and performance metrics
- **Auto-refresh**: Configurable auto-refresh intervals (5s, 10s, 30s, 1min)
- **Live Engagement**: Real-time chat and interaction metrics

## Authentication

### JWT Token Authentication

The Analytics API requires JWT tokens instead of standard OAuth Bearer tokens. This is handled automatically by the application.

#### How It Works

1. **Standard OAuth Token**: Used for Channel API operations (list channels, manage videos, etc.)
2. **JWT Token**: Used specifically for Analytics API operations

Both tokens use the same client credentials but are requested differently:

```python
# Standard OAuth token (for Channel API)
data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

# JWT token (for Analytics API)
data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'token_type': 'jwt'  # This is the key difference!
}
```

#### Implementation Details

The JWT authentication is implemented in:
- **`src/core/auth.py`**: `get_jwt_token()`, `_request_jwt_token()`, `get_analytics_auth_headers()`
- **`src/api/client.py`**: `analytics_get()`, `analytics_post()`, `_analytics_request()`
- **`src/api/analytics.py`**: All analytics methods use `client.analytics_get()`

## Usage

### Accessing the Dashboard

1. Launch the application
2. Navigate to the Analytics Dashboard panel
3. Select a channel from the dropdown
4. Choose your desired date range
5. View analytics across different tabs

### Channel Analytics Tab

1. **Select Channel**: Choose from your available channels
2. **Set Date Range**: Use date pickers or quick range buttons
3. **View Metrics**: See summary cards and detailed metrics table
4. **Demographics**: Review geographic and device distribution

### Video Analytics Tab

1. **Load Videos**: Click "Load Videos" to fetch videos from selected channel
2. **Select Video**: Choose a video from the dropdown
3. **View Performance**: See views, completion rate, and engagement
4. **Analyze Retention**: Review viewer retention curve (visualization coming soon)

### Live Stream Monitor Tab

1. **View Real-time Stats**: See current viewer count and stream status
2. **Enable Auto-refresh**: Toggle auto-refresh for live updates
3. **Set Refresh Interval**: Choose update frequency (5s to 1min)
4. **Monitor Engagement**: Track live chat and interaction metrics

## API Endpoints

The Analytics API uses different endpoints than the Channel API:

### Base URLs
- **Channel API**: `https://api.video.ibm.com`
- **Analytics API**: `https://analytics-api.video.ibm.com` (may vary - check IBM docs)

### Analytics Endpoints

#### Channel Metrics
```
GET /channels/{channelId}/metrics.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
  - metrics: comma-separated list (optional)
```

#### Current Viewers
```
GET /channels/{channelId}/viewers.json
```

#### Stream Health
```
GET /channels/{channelId}/health.json
```

#### Demographics
```
GET /channels/{channelId}/demographics.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
```

#### Engagement Metrics
```
GET /channels/{channelId}/engagement.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
```

#### Video Metrics
```
GET /videos/{videoId}/metrics.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
```

#### Peak Viewers
```
GET /channels/{channelId}/peak-viewers.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
```

#### Watch Time
```
GET /channels/{channelId}/watch-time.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
```

#### Export Metrics
```
GET /channels/{channelId}/metrics/export.json
Parameters:
  - start_date: ISO8601 datetime
  - end_date: ISO8601 datetime
  - format: 'json' or 'csv'
```

## Testing

### Test JWT Authentication

Run the test script to verify JWT authentication:

```bash
python test_analytics_jwt.py
```

This will:
1. Verify credentials are configured
2. Request standard OAuth token
3. Request JWT token
4. Confirm tokens are different
5. Test Analytics API endpoints

### Expected Output

```
======================================================================
Testing JWT Authentication for Analytics API
======================================================================
✓ Credentials found

1. Testing standard OAuth token...
✓ OAuth token obtained: eyJhbGciOiJSUzI1NiIs...

2. Testing JWT token for Analytics API...
✓ JWT token obtained: eyJhbGciOiJSUzI1NiIs...
✓ JWT token is different from OAuth token (as expected)

======================================================================
JWT Authentication Test: PASSED
======================================================================
```

## Troubleshooting

### Common Issues

#### 1. "Failed to obtain JWT token"

**Cause**: Credentials not configured or invalid

**Solution**:
- Verify `IBM_CLIENT_ID` and `IBM_CLIENT_SECRET` are set
- Check credentials are correct in IBM Video Streaming dashboard
- Ensure credentials have Analytics API access

#### 2. "Analytics API authentication headers not available"

**Cause**: JWT token request failed

**Solution**:
- Check network connectivity
- Verify IBM Video Streaming API is accessible
- Review logs for detailed error messages

#### 3. "Resource not found" errors

**Cause**: Analytics API endpoints may differ from documentation

**Solution**:
- Check IBM Video Streaming Analytics API documentation
- Verify endpoint URLs in `src/api/analytics.py`
- Update `ANALYTICS_BASE_URL` in `src/api/client.py` if needed

#### 4. No analytics data displayed

**Cause**: Channel may not have analytics data yet

**Solution**:
- Ensure channel has had viewers/activity
- Try a different date range
- Check if channel is properly configured for analytics

### Debug Mode

Enable debug logging to see detailed API requests:

```python
# In your code or config
import logging
logging.getLogger('core.auth').setLevel(logging.DEBUG)
logging.getLogger('api.client').setLevel(logging.DEBUG)
logging.getLogger('api.analytics').setLevel(logging.DEBUG)
```

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Analytics Dashboard UI                    │
│                  (src/ui/analytics_panel.py)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Analytics Manager                          │
│                  (src/api/analytics.py)                     │
│  - get_channel_metrics()                                    │
│  - get_video_metrics()                                      │
│  - get_current_viewers()                                    │
│  - get_stream_health()                                      │
│  - get_demographics()                                       │
│  - get_engagement_metrics()                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Client                                │
│                  (src/api/client.py)                        │
│  - analytics_get()  ← Uses JWT authentication              │
│  - analytics_post()                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Auth Manager                               │
│                  (src/core/auth.py)                         │
│  - get_jwt_token()  ← Requests JWT token                   │
│  - get_analytics_auth_headers()                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              IBM Video Streaming Analytics API               │
│           https://analytics-api.video.ibm.com               │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
1. User opens Analytics Dashboard
   │
   ▼
2. Dashboard requests channel analytics
   │
   ▼
3. Analytics Manager calls client.analytics_get()
   │
   ▼
4. Client checks for valid JWT token
   │
   ├─ Token valid? → Use existing token
   │
   └─ Token invalid/expired? → Request new JWT token
      │
      ▼
5. Auth Manager requests JWT token
   - POST to /oauth2/token
   - Include token_type=jwt parameter
   - Receive JWT token
   │
   ▼
6. Client makes Analytics API request
   - Authorization: Bearer {jwt_token}
   │
   ▼
7. Analytics API returns data
   │
   ▼
8. Dashboard displays analytics
```

## Future Enhancements

### Planned Features

1. **Data Visualization**
   - Line charts for viewer count over time
   - Bar charts for geographic distribution
   - Pie charts for device breakdown
   - Retention curves for videos

2. **Advanced Filtering**
   - Filter by traffic source
   - Filter by device type
   - Filter by geographic region
   - Custom metric selection

3. **Comparison Tools**
   - Compare multiple channels
   - Compare multiple videos
   - Compare time periods
   - Benchmark against averages

4. **Export Enhancements**
   - PDF reports
   - Scheduled exports
   - Email reports
   - Custom report templates

5. **Real-time Alerts**
   - Viewer threshold alerts
   - Stream health alerts
   - Engagement drop alerts
   - Custom alert rules

## References

- [IBM Video Streaming Developer Docs](https://github.com/IBM/video-streaming-developer-docs)
- [Analytics API Documentation](https://github.com/IBM/video-streaming-developer-docs/blob/master/src/pages/analytics-api-getting-started.mdx)
- [OAuth 2.0 Authentication](https://github.com/IBM/video-streaming-developer-docs/blob/master/src/pages/api-basics-authentication.mdx)

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review IBM Video Streaming documentation
3. Check application logs for detailed error messages
4. Verify API credentials and permissions

---

**Made with Bob** 🤖