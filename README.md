# IBM Video Streaming API Manager

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/bofika/IBMVS)

A comprehensive cross-platform **web-based application** for managing IBM Video Streaming services through their API. Built with Python and Flask, accessible from any modern web browser.

> **Note**: This application now uses a web-based interface instead of the previous Qt desktop application to ensure consistent behavior across all platforms.

## ✨ Features

### 🎥 Channel Management
- View and browse all channels
- Quick access to channel videos
- Search and filter channels
- Channel metadata display

### 📹 Video Management
- **View videos with smart pagination** (50/100/200 per page)
- **Toggle video protection status** (Public/Private) with instant feedback
- Search videos by title or metadata
- Real-time status updates
- Optimistic UI updates for better user experience
- Verified changes through IBM Dashboard

### 🎮 Player Configuration *(Coming Soon)*
- Customize player appearance
- Configure autoplay and controls
- Set color schemes and branding
- Generate embed codes

### 💬 Interactivity Controls *(Coming Soon)*
- Enable/disable live chat
- Create and manage polls
- Configure Q&A sessions
- Moderation tools

### 📊 Analytics & Monitoring *(Coming Soon)*
- Stream monitoring dashboard
- Viewer analytics
- Performance metrics
- Historical data visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- IBM Video Streaming API credentials (OAuth 2.0 Client ID and Secret)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/bofika/IBMVS.git
cd IBMVS
```

2. **Create and activate virtual environment**:
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Start the application**:
```bash
# On macOS/Linux:
./start_web_app.sh

# On Windows:
start_web_app.bat

# Or directly:
python web_app.py
```

5. **Access the application**:
Open your web browser and navigate to:
```
http://localhost:8080
```

## 📖 Configuration

### First-Time Setup

1. Open the application in your browser
2. Click **Settings** in the sidebar
3. Enter your IBM Video Streaming OAuth 2.0 credentials:
   - **Client ID** (40-character string)
   - **Client Secret**
4. Click **Save Credentials**
5. Click **Test Connection** to verify

### Obtaining OAuth 2.0 Credentials

1. Log in to your [IBM Video Streaming account](https://video.ibm.com/)
2. Navigate to **Dashboard** → **API/Channel Settings**
3. Create new **OAuth 2.0 client credentials**
4. Copy the Client ID and Client Secret
5. Keep these credentials secure

## 💡 Usage

### Managing Videos

1. Click **Videos** in the sidebar
2. Select a channel from the dropdown
3. Browse videos with pagination controls
4. **Toggle video status**:
   - Click "Make Private" to hide a video
   - Click "Make Public" to publish a video
   - Status updates instantly with visual feedback
   - Changes are verified on IBM's servers

### Search and Filter

- Use the search box to find specific videos
- Adjust page size (50/100/200 videos)
- Navigate with Previous/Next buttons
- View total video count and current page

## 🏗️ Architecture

### Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, Bootstrap 5, jQuery
- **API Client**: Custom Python modules for IBM Video Streaming API
- **Authentication**: OAuth 2.0 Client Credentials flow
- **Storage**: System keyring for secure credential storage

### Project Structure

```
IBMVS/
├── web_app.py              # Flask application entry point
├── start_web_app.sh        # macOS/Linux startup script
├── start_web_app.bat       # Windows startup script
├── src/
│   ├── api/                # API client modules
│   │   ├── channels.py     # Channel management
│   │   ├── videos.py       # Video management
│   │   ├── client.py       # HTTP client
│   │   └── ...
│   └── core/               # Core functionality
│       ├── auth.py         # OAuth 2.0 authentication
│       ├── config.py       # Configuration management
│       └── logger.py       # Logging system
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Main dashboard
│   └── settings.html      # Settings page
├── static/                 # Static assets (CSS, JS)
├── docs/                   # Documentation
└── tests/                  # Test suite
```

## 🔧 Development

### Running in Development Mode

```bash
# Enable debug mode
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows

python web_app.py
```

### Adding New Features

1. **Backend**: Add API endpoints in `web_app.py`
2. **Frontend**: Update templates in `templates/`
3. **API Integration**: Extend modules in `src/api/`

### Testing

```bash
# Run tests
pytest tests/

# Run specific test file
pytest tests/test_api/test_videos.py
```

## 📚 Documentation

- **[WEB_APP_README.md](WEB_APP_README.md)** - Detailed web app documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[API_REFERENCE.md](API_REFERENCE.md)** - API endpoint documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Change port in web_app.py or use environment variable
export PORT=8081
python web_app.py
```

#### "Failed to connect to API"
- Verify credentials in Settings
- Test connection using the "Test Connection" button
- Check internet connectivity
- Review logs in terminal

#### Video Status Not Changing
- Ensure you have admin permissions on the IBM account
- Check browser console for errors (F12)
- Verify the change in IBM Dashboard
- Review application logs

### Logs

Application logs are displayed in the terminal and stored in:
- **macOS**: `~/Library/Application Support/IBM Video Manager/logs/`
- **Windows**: `%APPDATA%\IBM Video Manager\logs\`

## 🎯 Why Web-Based?

The application was migrated from a Qt desktop application to a web-based interface to resolve persistent rendering issues on macOS. The web version offers:

- ✅ **Consistent behavior** across all platforms
- ✅ **No rendering bugs** - tables and UI update correctly
- ✅ **Better user experience** with instant visual feedback
- ✅ **Easier maintenance** and development
- ✅ **Remote access** capability
- ✅ **Mobile-friendly** responsive design

For more details, see [WEB_APP_README.md](WEB_APP_README.md).

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IBM Video Streaming for providing the API
- Flask team for the excellent web framework
- Bootstrap team for the UI components
- All contributors and users

## 🗺️ Roadmap

### Version 1.1 (Current)
- ✅ Web-based interface
- ✅ Channel browsing
- ✅ Video management with pagination
- ✅ Video protection toggle (Public/Private)
- ✅ Search functionality
- ✅ Settings management

### Version 1.2 (Planned)
- [ ] Video upload with progress tracking
- [ ] Batch operations (multi-select)
- [ ] Advanced search and filtering
- [ ] Player configuration UI
- [ ] Analytics dashboard

### Version 2.0 (Future)
- [ ] Stream monitoring
- [ ] Interactive features (chat, polls, Q&A)
- [ ] Multi-account support
- [ ] Scheduled operations
- [ ] Export functionality
- [ ] Dark/Light theme toggle

## 📞 Support

For issues, questions, or suggestions:
- **GitHub Issues**: [https://github.com/bofika/IBMVS/issues](https://github.com/bofika/IBMVS/issues)
- **Documentation**: Check the `docs/` folder
- **API Documentation**: [https://developers.video.ibm.com/](https://developers.video.ibm.com/)

## ⚠️ Disclaimer

This application is not officially affiliated with IBM. It is an independent tool built using the public IBM Video Streaming API.

---

**Made with ❤️ for the IBM Video Streaming community**