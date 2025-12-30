# IBM Video Streaming API Reference

This document provides a comprehensive reference for the IBM Video Streaming API endpoints used in this application.

## Base URL

```
https://api.video.ibm.com
```

## Authentication

All API requests require authentication using OAuth 2.0 Bearer tokens.

### Headers

```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

## API Endpoints

### Channel Management

#### List Channels

Get a list of all channels for the authenticated user.

```http
GET /users/self/channels.json
```

**Query Parameters:**
- `p` (integer, optional): Page number (default: 1)
- `pagesize` (integer, optional): Items per page (default: 100, max: 100)
- `q` (string, optional): Search query for channel title/description

**Response:**
```json
{
  "channels": [
    {
      "id": "12345",
      "title": "My Channel",
      "description": "Channel description",
      "url": "https://video.ibm.com/channel/12345",
      "status": "live",
      "viewer_count": 150,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "paging": {
    "page": 1,
    "pagesize": 100,
    "total": 5
  }
}
```

#### Get Channel Details

Get detailed information about a specific channel.

```http
GET /channels/{channelId}.json
```

**Response:**
```json
{
  "channel": {
    "id": "12345",
    "title": "My Channel",
    "description": "Channel description",
    "url": "https://video.ibm.com/channel/12345",
    "status": "live",
    "viewer_count": 150,
    "created_at": "2024-01-01T00:00:00Z",
    "owner": {
      "id": "67890",
      "username": "user123"
    },
    "settings": {
      "privacy": "public",
      "chat_enabled": true,
      "recording_enabled": true
    }
  }
}
```

#### Create Channel

Create a new channel.

```http
POST /users/self/channels.json
```

**Request Body:**
```json
{
  "title": "New Channel",
  "description": "Channel description",
  "tags": ["tag1", "tag2"]
}
```

**Response:**
```json
{
  "channel": {
    "id": "12346",
    "title": "New Channel",
    "description": "Channel description",
    "url": "https://video.ibm.com/channel/12346",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Update Channel

Update an existing channel.

```http
PUT /channels/{channelId}.json
```

**Request Body:**
```json
{
  "title": "Updated Channel Title",
  "description": "Updated description",
  "tags": ["new-tag"]
}
```

**Response:**
```json
{
  "channel": {
    "id": "12345",
    "title": "Updated Channel Title",
    "description": "Updated description",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

#### Delete Channel

Delete a channel permanently.

```http
DELETE /channels/{channelId}.json
```

**Response:**
```json
{
  "success": true,
  "message": "Channel deleted successfully"
}
```

### Video Management

#### List Videos

Get all videos for a specific channel.

```http
GET /channels/{channelId}/videos.json
```

**Query Parameters:**
- `p` (integer, optional): Page number
- `pagesize` (integer, optional): Items per page
- `q` (string, optional): Search query

**Response:**
```json
{
  "videos": [
    {
      "id": "98765",
      "title": "Video Title",
      "description": "Video description",
      "duration": 3600,
      "thumbnail": "https://cdn.example.com/thumb.jpg",
      "views": 1250,
      "status": "ready",
      "created_at": "2024-01-10T15:00:00Z"
    }
  ],
  "paging": {
    "page": 1,
    "pagesize": 50,
    "total": 25
  }
}
```

#### Get Video Details

Get detailed information about a specific video.

```http
GET /videos/{videoId}.json
```

**Response:**
```json
{
  "video": {
    "id": "98765",
    "channel_id": "12345",
    "title": "Video Title",
    "description": "Video description",
    "duration": 3600,
    "thumbnail": "https://cdn.example.com/thumb.jpg",
    "views": 1250,
    "status": "ready",
    "created_at": "2024-01-10T15:00:00Z",
    "media_urls": {
      "hls": "https://stream.example.com/video.m3u8",
      "rtmp": "rtmp://stream.example.com/video"
    }
  }
}
```

#### Upload Video

Upload a new video to a channel.

```http
POST /channels/{channelId}/videos.json
```

**Request:** Multipart form data

**Form Fields:**
- `file`: Video file (binary)
- `title`: Video title (string)
- `description`: Video description (string, optional)
- `tags`: Comma-separated tags (string, optional)

**Response:**
```json
{
  "video": {
    "id": "98766",
    "title": "New Video",
    "status": "processing",
    "upload_id": "upload-123",
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

#### Update Video

Update video metadata.

```http
PUT /videos/{videoId}.json
```

**Request Body:**
```json
{
  "title": "Updated Video Title",
  "description": "Updated description",
  "tags": ["tag1", "tag2"]
}
```

**Response:**
```json
{
  "video": {
    "id": "98765",
    "title": "Updated Video Title",
    "description": "Updated description",
    "updated_at": "2024-01-15T12:30:00Z"
  }
}
```

#### Delete Video

Delete a video permanently.

```http
DELETE /videos/{videoId}.json
```

**Response:**
```json
{
  "success": true,
  "message": "Video deleted successfully"
}
```

### Player Configuration

#### Get Player Settings

Get player configuration for a channel.

```http
GET /channels/{channelId}/settings/player.json
```

**Response:**
```json
{
  "player": {
    "autoplay": true,
    "controls": true,
    "responsive": true,
    "color_scheme": "dark",
    "primary_color": "#007bff",
    "logo_url": "https://example.com/logo.png",
    "logo_position": "top-right"
  }
}
```

#### Update Player Settings

Update player configuration.

```http
PUT /channels/{channelId}/settings/player.json
```

**Request Body:**
```json
{
  "autoplay": false,
  "controls": true,
  "responsive": true,
  "color_scheme": "light",
  "primary_color": "#ff0000"
}
```

**Response:**
```json
{
  "player": {
    "autoplay": false,
    "controls": true,
    "responsive": true,
    "color_scheme": "light",
    "primary_color": "#ff0000",
    "updated_at": "2024-01-15T13:00:00Z"
  }
}
```

#### Get Embed Code

Get HTML embed code for a channel.

```http
GET /channels/{channelId}/embed.json
```

**Query Parameters:**
- `width` (integer, optional): Player width
- `height` (integer, optional): Player height
- `responsive` (boolean, optional): Responsive embed

**Response:**
```json
{
  "embed_code": "<iframe src=\"https://video.ibm.com/embed/12345\" width=\"640\" height=\"360\" frameborder=\"0\" allowfullscreen></iframe>"
}
```

### Interactivity

#### Get Chat Settings

Get chat configuration for a channel.

```http
GET /channels/{channelId}/settings/chat.json
```

**Response:**
```json
{
  "chat": {
    "enabled": true,
    "moderation": "auto",
    "require_login": false,
    "slow_mode": false,
    "slow_mode_interval": 0
  }
}
```

#### Update Chat Settings

Update chat configuration.

```http
PUT /channels/{channelId}/settings/chat.json
```

**Request Body:**
```json
{
  "enabled": true,
  "moderation": "manual",
  "require_login": true,
  "slow_mode": true,
  "slow_mode_interval": 5
}
```

**Response:**
```json
{
  "chat": {
    "enabled": true,
    "moderation": "manual",
    "require_login": true,
    "slow_mode": true,
    "slow_mode_interval": 5,
    "updated_at": "2024-01-15T14:00:00Z"
  }
}
```

#### List Polls

Get all polls for a channel.

```http
GET /channels/{channelId}/polls.json
```

**Response:**
```json
{
  "polls": [
    {
      "id": "poll-123",
      "question": "What's your favorite feature?",
      "options": [
        {"id": "opt-1", "text": "Live Chat", "votes": 45},
        {"id": "opt-2", "text": "HD Streaming", "votes": 67}
      ],
      "status": "active",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

#### Create Poll

Create a new poll.

```http
POST /channels/{channelId}/polls.json
```

**Request Body:**
```json
{
  "question": "What's your favorite feature?",
  "options": [
    {"text": "Live Chat"},
    {"text": "HD Streaming"},
    {"text": "Analytics"}
  ],
  "duration": 300
}
```

**Response:**
```json
{
  "poll": {
    "id": "poll-124",
    "question": "What's your favorite feature?",
    "options": [
      {"id": "opt-3", "text": "Live Chat", "votes": 0},
      {"id": "opt-4", "text": "HD Streaming", "votes": 0},
      {"id": "opt-5", "text": "Analytics", "votes": 0}
    ],
    "status": "active",
    "created_at": "2024-01-15T15:00:00Z",
    "expires_at": "2024-01-15T15:05:00Z"
  }
}
```

#### Delete Poll

Delete a poll.

```http
DELETE /channels/{channelId}/polls/{pollId}.json
```

**Response:**
```json
{
  "success": true,
  "message": "Poll deleted successfully"
}
```

### Analytics

#### Get Channel Metrics

Get analytics metrics for a channel.

```http
GET /channels/{channelId}/metrics.json
```

**Query Parameters:**
- `start_date` (string, optional): Start date (ISO 8601)
- `end_date` (string, optional): End date (ISO 8601)
- `metrics` (string, optional): Comma-separated metric names

**Response:**
```json
{
  "metrics": {
    "total_views": 15000,
    "unique_viewers": 8500,
    "avg_watch_time": 1800,
    "peak_concurrent_viewers": 450,
    "total_watch_time": 15300000,
    "engagement_rate": 0.75
  },
  "period": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-15T23:59:59Z"
  }
}
```

#### Get Current Viewers

Get real-time viewer count.

```http
GET /channels/{channelId}/viewers.json
```

**Response:**
```json
{
  "viewers": {
    "current": 150,
    "peak_today": 320,
    "countries": [
      {"code": "US", "count": 75},
      {"code": "GB", "count": 30},
      {"code": "DE", "count": 25}
    ]
  },
  "timestamp": "2024-01-15T16:00:00Z"
}
```

#### Get Stream Health

Get stream health metrics.

```http
GET /channels/{channelId}/health.json
```

**Response:**
```json
{
  "health": {
    "status": "healthy",
    "bitrate": 4500,
    "framerate": 30,
    "resolution": "1920x1080",
    "dropped_frames": 0,
    "buffer_health": 100,
    "latency": 2.5
  },
  "timestamp": "2024-01-15T16:00:00Z"
}
```

## Data Models

### Channel

```python
@dataclass
class Channel:
    id: str
    title: str
    description: str
    url: str
    status: str  # 'live', 'offline', 'recorded'
    viewer_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: str
    settings: Dict[str, Any]
    tags: List[str]
```

### Video

```python
@dataclass
class Video:
    id: str
    channel_id: str
    title: str
    description: str
    duration: int  # seconds
    thumbnail_url: str
    views: int
    status: str  # 'processing', 'ready', 'error'
    created_at: datetime
    updated_at: Optional[datetime]
    media_urls: Dict[str, str]
    tags: List[str]
```

### PlayerConfig

```python
@dataclass
class PlayerConfig:
    channel_id: str
    autoplay: bool
    controls: bool
    responsive: bool
    color_scheme: str  # 'light', 'dark'
    primary_color: str
    logo_url: Optional[str]
    logo_position: str  # 'top-left', 'top-right', 'bottom-left', 'bottom-right'
```

### ChatSettings

```python
@dataclass
class ChatSettings:
    channel_id: str
    enabled: bool
    moderation: str  # 'auto', 'manual', 'off'
    require_login: bool
    slow_mode: bool
    slow_mode_interval: int  # seconds
```

### Poll

```python
@dataclass
class PollOption:
    id: str
    text: str
    votes: int

@dataclass
class Poll:
    id: str
    channel_id: str
    question: str
    options: List[PollOption]
    status: str  # 'active', 'closed'
    created_at: datetime
    expires_at: Optional[datetime]
```

### Metrics

```python
@dataclass
class ChannelMetrics:
    channel_id: str
    total_views: int
    unique_viewers: int
    avg_watch_time: int  # seconds
    peak_concurrent_viewers: int
    total_watch_time: int  # seconds
    engagement_rate: float
    period_start: datetime
    period_end: datetime
```

### StreamHealth

```python
@dataclass
class StreamHealth:
    channel_id: str
    status: str  # 'healthy', 'warning', 'critical'
    bitrate: int  # kbps
    framerate: int
    resolution: str
    dropped_frames: int
    buffer_health: int  # percentage
    latency: float  # seconds
    timestamp: datetime
```

## Error Responses

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

### Common Error Codes

- `400` - Bad Request: Invalid parameters
- `401` - Unauthorized: Invalid or expired token
- `403` - Forbidden: Insufficient permissions
- `404` - Not Found: Resource doesn't exist
- `429` - Too Many Requests: Rate limit exceeded
- `500` - Internal Server Error: Server-side error

## Rate Limiting

- **Rate Limit**: 100 requests per minute per API key
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests per minute
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `p`: Page number (1-based)
- `pagesize`: Items per page (max: 100)

**Response includes:**
```json
{
  "paging": {
    "page": 1,
    "pagesize": 50,
    "total": 150
  }
}
```

## Best Practices

1. **Cache responses** when appropriate (use ETags)
2. **Implement retry logic** with exponential backoff
3. **Respect rate limits** to avoid throttling
4. **Use pagination** for large datasets
5. **Handle errors gracefully** with user-friendly messages
6. **Keep tokens secure** and refresh before expiration
7. **Use HTTPS** for all API requests
8. **Validate input** before sending requests
9. **Log API calls** for debugging
10. **Monitor API usage** to stay within limits