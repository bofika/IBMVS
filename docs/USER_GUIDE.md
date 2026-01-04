# IBM Video Streaming Manager - User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Using the Application](#using-the-application)
5. [Features](#features)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Getting Started

IBM Video Streaming Manager is a desktop application that allows you to manage your IBM Video Streaming channels, videos, and settings through an intuitive graphical interface.

### System Requirements

- **Operating System**: macOS 10.14+ or Windows 10+
- **Python**: 3.9 or higher
- **VLC Media Player**: Required for stream preview
- **Internet Connection**: Required for API access

## Installation

### Method 1: From Source

1. **Install Python 3.9+**
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install VLC Media Player**
   - macOS: Download from [videolan.org](https://www.videolan.org/)
   - Windows: Download from [videolan.org](https://www.videolan.org/)

3. **Clone or Download the Application**
   ```bash
   git clone https://github.com/bofika/IBMVS.git
   cd IBMVS
   ```

4. **Create Virtual Environment**
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application**
   ```bash
   python src/main.py
   ```

**Note for macOS users**: If you get "python: command not found", use `python3` instead of `python` in step 4.

### Method 2: Pre-built Installer (Coming Soon)

Download the installer for your platform and follow the installation wizard.

## Configuration

### First-Time Setup

1. **Launch the Application**
   - The application will prompt you for API credentials on first launch

2. **Enter API Credentials**
   - Go to Settings (⚙️) or use the prompt
   - Enter your IBM Video Streaming API Key
   - Enter your IBM Video Streaming API Secret
   - Click "Save"

3. **Obtain API Credentials**
   - Log in to your IBM Video Streaming account
   - Navigate to Dashboard → API/Channel Settings
   - Generate new API credentials
   - Copy the API Key and Secret

### Settings

Access settings through:
- Menu: Edit → Preferences
- Sidebar: Click Settings (⚙️)
- Keyboard: Ctrl+, (Cmd+, on Mac)

## Using the Application

### Main Window

The application has a sidebar navigation with six main sections:

1. **📺 Channels** - Manage your channels
2. **🎬 Videos** - Upload and manage videos
3. **▶️ Players** - Configure player appearance
4. **💬 Interactive** - Manage chat, polls, and Q&A
5. **📊 Monitor** - View analytics and stream health
6. **⚙️ Settings** - Application and API settings

### Keyboard Shortcuts

- `Ctrl+R` (Cmd+R): Refresh current panel
- `Ctrl+Q` (Cmd+Q): Quit application
- `Ctrl+,` (Cmd+,): Open preferences
- `Ctrl+1`: Switch to Channels
- `Ctrl+2`: Switch to Videos
- `Ctrl+3`: Switch to Monitor

## Features

### 1. Channel Management

**View Channels**
- All your channels are listed in a table
- Shows: ID, Title, Status, Current Viewers
- Use search box to filter channels

**Create Channel**
1. Click "Create Channel" button
2. Enter channel title (required)
3. Enter description (optional)
4. Add tags (optional)
5. Click "Create"

**Edit Channel**
1. Click "Edit" button next to channel
2. Modify title, description, or tags
3. Click "Save"

**Delete Channel**
1. Click "Delete" button next to channel
2. Confirm deletion
3. Channel will be permanently removed

### 2. Video Management

**View Videos**
1. Select a channel from dropdown
2. All videos for that channel are displayed
3. Shows: Title, Duration, Views, Status

**Upload Video**
1. Click "Upload Video" button
2. Select channel
3. Click "Browse" to select video file
4. Enter title (required)
5. Enter description (optional)
6. Add tags (optional)
7. Click "OK" to start upload
8. Monitor upload progress

**Supported Video Formats**
- MP4, MOV, AVI, MKV, FLV, WMV, WebM

**Edit Video**
1. Click "Edit" button next to video
2. Modify title, description, or tags
3. Click "Save"

**Delete Video**
1. Click "Delete" button next to video
2. Confirm deletion

### 3. Player Configuration

**Configure Player**
1. Select a channel
2. Adjust settings:
   - **Autoplay**: Start playing automatically
   - **Show Controls**: Display player controls
   - **Responsive**: Adapt to screen size
   - **Color Scheme**: Dark or Light
   - **Primary Color**: Choose brand color
   - **Logo**: Add custom logo with URL
   - **Logo Position**: Choose corner placement

3. Click "Save Settings"

**Generate Embed Code**
1. Set desired width and height
2. Click "Generate Embed Code"
3. Copy the HTML code
4. Paste into your website

**Preview Player**
- Click "Preview Player" to open in browser

### 4. Interactive Features

**Chat Settings**
1. Select a channel
2. Configure:
   - Enable/Disable chat
   - Moderation mode (auto/manual/off)
   - Require login to chat
   - Slow mode with interval
3. Click "Save Chat Settings"

**Create Poll**
1. Click "Create Poll"
2. Enter question
3. Add 2-10 options
4. Set duration (optional)
5. Click "OK"

**Manage Polls**
- View active polls
- Close polls when finished
- See poll results

**Q&A Settings**
1. Enable/Disable Q&A
2. Enable moderation
3. Click "Save Q&A Settings"

### 5. Stream Monitoring

**View Current Stats**
- Current viewer count
- Stream status (Live/Offline)
- Stream health
- Peak viewers today

**Stream Preview**
- Live stream preview (requires VLC)
- Open stream in browser

**Analytics**
1. Select time range:
   - Last Hour
   - Last 24 Hours
   - Last 7 Days
   - Last 30 Days

2. View metrics:
   - Total views
   - Unique viewers
   - Average watch time
   - Peak concurrent viewers
   - Total watch time
   - Engagement rate

**Auto-Refresh**
- Click "Auto-Refresh" to enable
- Updates every 5 seconds
- Click again to disable

### 6. Settings

**API Credentials**
- View credential status
- Change credentials
- Clear stored credentials

**Application Settings**
- Theme selection (coming soon)
- Cache settings (coming soon)
- Log level (coming soon)

## Troubleshooting

### Common Issues

**"Failed to connect to API"**
- Check your internet connection
- Verify API credentials in Settings
- Ensure API endpoints are accessible
- Check firewall settings

**"Authentication failed"**
- Verify API Key and Secret are correct
- Regenerate credentials in IBM dashboard
- Clear and re-enter credentials

**"VLC player not found"**
- Install VLC Media Player
- Ensure VLC is in system PATH
- Restart application after installing VLC

**"Video upload fails"**
- Check video file format
- Verify file size (max 5GB)
- Ensure stable internet connection
- Check available disk space

**"No channels displayed"**
- Verify you have channels in your IBM account
- Click "Refresh" button
- Check API credentials

### Log Files

Application logs are stored in:
- **macOS**: `~/Library/Application Support/IBM Video Manager/logs/`
- **Windows**: `%APPDATA%\IBM Video Manager\logs\`

Check `app.log` for general logs and `error.log` for errors.

### Getting Help

1. Check this user guide
2. Review log files
3. Check IBM Video Streaming API documentation
4. Contact support

## FAQ

**Q: Is this application official from IBM?**  
A: No, this is an independent application built using the public IBM Video Streaming API.

**Q: Do I need an IBM Video Streaming account?**  
A: Yes, you need an active IBM Video Streaming account with API access.

**Q: Can I manage multiple accounts?**  
A: Currently, the application supports one account at a time. Multi-account support is planned for future versions.

**Q: Is my data secure?**  
A: Yes, API credentials are stored securely using your system's keyring. All communication with IBM servers uses HTTPS.

**Q: Can I use this on Linux?**  
A: The application is designed for macOS and Windows, but may work on Linux with proper dependencies.

**Q: How do I update the application?**  
A: Download the latest version and reinstall, or pull the latest code if using from source.

**Q: Can I schedule streams?**  
A: Scheduled streaming is planned for a future version.

**Q: Does this work with IBM Cloud Video?**  
A: Yes, IBM Video Streaming is part of IBM Cloud Video.

**Q: Can I export analytics data?**  
A: Analytics export functionality is available through the API and will be added to the UI in a future version.

**Q: What video formats are supported?**  
A: MP4, MOV, AVI, MKV, FLV, WMV, WebM, and other common formats.

## Tips & Best Practices

1. **Regular Backups**: Keep backups of important video files
2. **Test Before Live**: Test settings before going live
3. **Monitor Performance**: Use the Monitor panel during live streams
4. **Engage Viewers**: Use polls and Q&A for interaction
5. **Optimize Videos**: Compress videos before upload for faster processing
6. **Brand Consistency**: Configure player with your brand colors and logo
7. **Moderate Chat**: Enable moderation for professional streams
8. **Check Analytics**: Review analytics regularly to understand your audience

## Support & Resources

- **IBM Video Streaming Documentation**: https://developers.video.ibm.com/
- **Application Repository**: https://github.com/yourusername/ibm-video-manager
- **Report Issues**: Use GitHub Issues
- **Email Support**: support@example.com

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-30