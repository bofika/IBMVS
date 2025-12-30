# IBM Video Streaming API Manager

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6%2B-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/bofika/IBMVS)

A comprehensive cross-platform desktop application for managing IBM Video Streaming services through their API. Built with Python and PyQt6, supporting both macOS and Windows.

## Features

### 🎥 Channel Management
- Create, edit, and delete channels
- Configure broadcast settings
- Manage channel metadata and descriptions
- Search and filter channels

### 📹 Video Management
- Upload videos with progress tracking
- Edit video metadata (title, description, tags)
- Delete videos with confirmation
- Organize videos into playlists
- Batch operations support

### 🎮 Player Configuration
- Customize player appearance
- Configure autoplay and controls
- Set color schemes and branding
- Generate embed codes
- Preview player configurations

### 💬 Interactivity Controls
- Enable/disable live chat
- Create and manage polls
- Configure Q&A sessions
- Moderation tools
- Real-time interaction management

### 📊 Stream Monitoring & Analytics
- Real-time stream preview with embedded VLC player
- Live viewer count tracking
- Stream health metrics
- Analytics dashboard with charts
- Historical data visualization
- Multi-channel monitoring support

## Technology Stack

- **Python 3.9+**: Core application language
- **PyQt6**: Modern GUI framework
- **VLC**: Video playback and stream preview
- **Matplotlib/PyQtGraph**: Data visualization
- **Requests**: HTTP client for API communication

## Prerequisites

- Python 3.9 or higher
- VLC Media Player installed on your system
- IBM Video Streaming API credentials (API key and secret)

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/bofika/IBMVS.git
cd IBMVS
```

2. Create a virtual environment:
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

### Pre-built Binaries

Download the latest release for your platform:
- **macOS**: `IBM-Video-Manager-macOS.dmg`
- **Windows**: `IBM-Video-Manager-Windows.exe`

## Configuration

### First-Time Setup

1. Launch the application
2. Go to **Settings** → **API Configuration**
3. Enter your IBM Video Streaming API credentials:
   - API Key
   - API Secret
4. Click **Save** and **Test Connection**

### API Credentials

To obtain API credentials:
1. Log in to your IBM Video Streaming account
2. Navigate to **Dashboard** → **API/Channel Settings**
3. Generate new API credentials
4. Copy the API key and secret

## Usage

### Managing Channels

1. Click on **Channels** in the sidebar
2. View all your channels in the list
3. Use the toolbar buttons to:
   - **Create**: Add a new channel
   - **Edit**: Modify channel settings
   - **Delete**: Remove a channel
   - **Refresh**: Update the channel list

### Uploading Videos

1. Navigate to **Videos** panel
2. Click **Upload Video**
3. Select video file(s) from your computer
4. Fill in metadata (title, description, tags)
5. Choose target channel
6. Click **Upload** and monitor progress

### Monitoring Streams

1. Go to **Monitor** panel
2. Select a channel from the dropdown
3. View live stream preview
4. Monitor real-time metrics:
   - Current viewer count
   - Stream bitrate
   - Connection quality
   - Viewer engagement

### Configuring Players

1. Open **Players** panel
2. Select a channel
3. Customize player settings:
   - Appearance (colors, logo)
   - Behavior (autoplay, controls)
   - Responsive design options
4. Preview changes in real-time
5. Save configuration

### Managing Interactivity

1. Navigate to **Interactive** panel
2. Enable/disable features:
   - Live chat
   - Polls
   - Q&A sessions
3. Configure moderation settings
4. Monitor and moderate in real-time

## Project Structure

```
ibm-video-manager/
├── src/
│   ├── main.py              # Application entry point
│   ├── api/                 # API client modules
│   ├── ui/                  # PyQt6 UI components
│   ├── core/                # Core functionality
│   └── utils/               # Utility functions
├── resources/               # Icons, styles, assets
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Run with debug logging:
```bash
python src/main.py --debug
```

### Building from Source

#### macOS
```bash
pyinstaller --windowed --name "IBM Video Manager" \
  --icon resources/icons/app.icns \
  src/main.py
```

#### Windows
```bash
pyinstaller --windowed --name "IBM Video Manager" ^
  --icon resources/icons/app.ico ^
  src/main.py
```

## Troubleshooting

### Common Issues

**Issue**: "Failed to connect to API"
- **Solution**: Verify your API credentials in Settings
- Check your internet connection
- Ensure API endpoints are accessible

**Issue**: "VLC player not found"
- **Solution**: Install VLC Media Player from https://www.videolan.org/
- Ensure VLC is in your system PATH

**Issue**: "Video upload fails"
- **Solution**: Check video format compatibility
- Verify file size limits
- Ensure sufficient disk space

### Logs

Application logs are stored in:
- **macOS**: `~/Library/Application Support/IBM Video Manager/logs/`
- **Windows**: `%APPDATA%\IBM Video Manager\logs\`

## API Documentation

For detailed IBM Video Streaming API documentation, visit:
https://developers.video.ibm.com/

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@example.com

## Acknowledgments

- IBM Video Streaming for providing the API
- PyQt6 team for the excellent GUI framework
- VLC team for the media player library

## Roadmap

### Version 1.0 (Current)
- ✅ Basic channel management
- ✅ Video upload and management
- ✅ Player configuration
- ✅ Stream monitoring
- ✅ Analytics dashboard

### Version 1.1 (Planned)
- [ ] Multi-account support
- [ ] Batch operations
- [ ] Advanced analytics with export
- [ ] Scheduled streaming
- [ ] Enhanced moderation tools

### Version 2.0 (Future)
- [ ] Mobile companion app
- [ ] Plugin system
- [ ] Custom themes
- [ ] Automated workflows
- [ ] Team collaboration features

## Screenshots

*Screenshots will be added after UI implementation*

---

**Note**: This application is not officially affiliated with IBM. It is an independent tool built using the public IBM Video Streaming API.