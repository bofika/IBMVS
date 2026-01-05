# IBM Video Streaming Manager - Web Application

## Overview

This is a **web-based version** of the IBM Video Streaming Manager, created to resolve persistent UI rendering issues with the Qt-based desktop application on macOS.

### Why Web-Based?

After extensive investigation, we discovered that Qt (both PyQt6 and PySide6) has an unfixable rendering bug on macOS where table cells don't update visually despite data being correct. We tried:

- ✗ QTableWidget with 8+ different refresh methods
- ✗ Switching from PyQt6 to PySide6
- ✗ QTableView with QAbstractTableModel (Model/View architecture)
- ✗ Force repaints, viewport updates, hide/show tricks

**Solution:** Web-based UI using Flask + HTML/JavaScript, which:
- ✅ Works perfectly on all platforms (macOS, Windows, Linux)
- ✅ No rendering issues
- ✅ Real-time updates work correctly
- ✅ Easier to maintain and extend
- ✅ Accessible from any device with a browser

## Features

### Current Implementation

- **Dashboard**: Overview of channels and videos
- **Channel Management**: View and select channels
- **Video Management**: 
  - View videos with pagination
  - Toggle video status (Public/Private) - **WORKS CORRECTLY!**
  - Search videos
  - Adjustable page size (50/100/200)
  - Real-time status updates
- **Settings**: Configure API credentials

### Planned Features

- Channel creation/editing/deletion
- Video upload
- Player configuration
- Interactive features (chat, polls, Q&A)
- Analytics dashboard
- Stream monitoring

## Installation

### 1. Install Dependencies

```bash
pip install Flask Flask-CORS
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

You have two options:

**Option A: Use existing credentials**
If you already configured credentials in the Qt app, they will work automatically.

**Option B: Configure via web interface**
1. Start the web app (see below)
2. Go to Settings
3. Enter your Client ID and Client Secret
4. Click "Save Credentials"
5. Click "Test Connection"

## Running the Application

### Start the Web Server

```bash
python3 web_app.py
```

The application will start on `http://localhost:5000`

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### 1. Configure Credentials (First Time)

1. Click "Settings" in the sidebar
2. Enter your IBM Video Streaming API credentials
3. Click "Save Credentials"
4. Click "Test Connection" to verify

### 2. View Channels

1. Click "Channels" in the sidebar or "View Channels" on the dashboard
2. Browse your channels
3. Click "View Videos" on any channel to see its videos

### 3. Manage Videos

1. Select a channel from the dropdown
2. Videos will load automatically
3. **Toggle video status**: Click "Make Private" or "Make Public"
   - Status updates immediately (no refresh needed!)
   - Table updates automatically after 1 second
4. Use pagination to navigate through videos
5. Search for specific videos
6. Change page size (50/100/200 videos per page)

## Architecture

### Backend (Flask)

- **web_app.py**: Main Flask application
- **API Routes**: RESTful endpoints for all operations
- **Reuses existing modules**: All `src/api/*` and `src/core/*` modules

### Frontend (HTML/JavaScript)

- **templates/base.html**: Base template with navigation
- **templates/index.html**: Main dashboard and video management
- **templates/settings.html**: API credentials configuration
- **Bootstrap 5**: Modern, responsive UI
- **jQuery**: AJAX requests for real-time updates

### API Endpoints

#### Authentication
- `GET /api/auth/credentials` - Check if credentials exist
- `POST /api/auth/credentials` - Save credentials
- `POST /api/auth/test` - Test API connection

#### Channels
- `GET /api/channels` - List channels
- `GET /api/channels/<id>` - Get channel details

#### Videos
- `GET /api/channels/<id>/videos` - List videos for channel
- `GET /api/videos/<id>` - Get video details
- `PUT /api/videos/<id>/protection` - Update video status

## Advantages Over Qt Version

### 1. **No Rendering Issues**
- Tables update correctly
- Status changes are visible immediately
- No need to restart application

### 2. **Cross-Platform**
- Works on macOS, Windows, Linux
- No platform-specific bugs
- Consistent behavior everywhere

### 3. **Accessible**
- Access from any device with a browser
- Can run on a server and access remotely
- Mobile-friendly (responsive design)

### 4. **Easier Development**
- HTML/CSS/JavaScript is easier to debug
- Browser dev tools for inspection
- Faster iteration and testing

### 5. **Better User Experience**
- Modern, clean interface
- Real-time updates without page refresh
- Smooth animations and transitions

## Comparison: Qt vs Web

| Feature | Qt Version | Web Version |
|---------|-----------|-------------|
| Table Refresh | ❌ Broken on macOS | ✅ Works perfectly |
| Status Toggle | ❌ No visual update | ✅ Updates immediately |
| Cross-Platform | ⚠️ macOS issues | ✅ Works everywhere |
| Installation | Complex (Qt dependencies) | Simple (Flask only) |
| Maintenance | Difficult | Easy |
| Remote Access | ❌ No | ✅ Yes |
| Mobile Support | ❌ No | ✅ Yes (responsive) |

## Development

### Adding New Features

1. **Add API endpoint** in `web_app.py`:
```python
@app.route('/api/your-endpoint')
def your_endpoint():
    # Your logic here
    return jsonify(result)
```

2. **Add frontend code** in templates:
```javascript
function yourFunction() {
    $.ajax({
        url: '/api/your-endpoint',
        success: function(response) {
            // Handle response
        }
    });
}
```

### Debugging

- **Backend**: Check terminal output for Flask logs
- **Frontend**: Use browser Developer Tools (F12)
- **Network**: Monitor AJAX requests in Network tab
- **Console**: Check for JavaScript errors

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:

```bash
# Change port in web_app.py
app.run(debug=True, host='0.0.0.0', port=8080)
```

### CORS Issues

If accessing from a different domain, CORS is already configured via Flask-CORS.

### API Errors

1. Check credentials in Settings
2. Test connection
3. Check terminal logs for detailed error messages

## Future Enhancements

- [ ] Video upload with progress bar
- [ ] Drag-and-drop file upload
- [ ] Bulk operations (multi-select)
- [ ] Advanced search and filtering
- [ ] Real-time notifications
- [ ] User management
- [ ] Activity logs
- [ ] Export data (CSV, JSON)
- [ ] Dark/Light theme toggle
- [ ] Keyboard shortcuts

## Migration from Qt Version

The web version uses the same backend API modules, so:

1. **Credentials**: Automatically shared
2. **Configuration**: Same config files
3. **Logs**: Same logging system
4. **Data**: No migration needed

You can run both versions simultaneously if needed.

## License

Same as the main project - see LICENSE file.

## Support

For issues specific to the web version, please note "Web App" in your issue title.

## Conclusion

The web-based version solves all the rendering issues we encountered with Qt on macOS while providing a better user experience and easier maintenance. This is now the **recommended version** for all users.