# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Multi-account support
- Batch operations for videos and channels
- Advanced analytics with export functionality
- Scheduled streaming capabilities
- Enhanced moderation tools
- Video upload functionality in web UI
- Player configuration in web UI
- Analytics dashboard in web UI
- Stream monitoring in web UI

## [1.1.0] - 2026-01-05

### Added
- **Web-based UI** using Flask to replace Qt desktop application
- Optimistic UI updates for video protection toggle
- Loading states and visual feedback for all operations
- Smart pagination supporting 50/100/200 videos per page
- Real-time video status updates without page refresh
- Responsive Bootstrap 5 design
- Cross-platform compatibility (macOS, Windows, Linux)

### Fixed
- **Critical**: Video protection toggle now works correctly
  - Changed from JSON to form-encoded data for IBM API compatibility
  - Added verification of status changes
  - Implemented optimistic UI updates with automatic revert on failure
- Pagination parameter corrected from 'p' to 'page'
- Total count field corrected from 'total' to 'item_count'
- Video details now use 'detail_level=owner' to retrieve protection status
- Qt table refresh issues on macOS (resolved by migrating to web UI)

### Changed
- **Breaking**: Primary interface is now web-based (Flask) instead of Qt desktop
- Video protection API calls now use form data instead of JSON
- Improved user feedback with instant visual updates
- Enhanced error messages and logging

### Technical
- Migrated from PyQt6/PySide6 to Flask web framework
- Implemented optimistic UI pattern for better UX
- Added comprehensive logging for API interactions
- Fixed f-string syntax errors in logging statements

## [1.0.0] - 2025-12-30

### Added
- Initial release of IBM Video Streaming API Manager
- Complete channel management (create, edit, delete, search)
- Video upload with progress tracking
- Video management (edit metadata, delete, organize playlists)
- Player configuration with customization options
- Embed code generation for players
- Interactivity controls (chat, polls, Q&A)
- Real-time stream monitoring dashboard
- Analytics dashboard with metrics visualization
- Secure credential storage using system keyring
- Cross-platform support (macOS and Windows)
- Comprehensive error handling and logging
- User-friendly PyQt6 GUI with sidebar navigation
- Settings panel for API configuration
- Auto-refresh for monitoring data
- Search and filter functionality for channels
- Keyboard shortcuts for common actions
- Complete user documentation
- API reference documentation
- Technical implementation guide

### Security
- Secure credential storage using OS keyring
- API key and secret encryption
- No plaintext credential storage

### Documentation
- Comprehensive USER_GUIDE.md
- API_REFERENCE.md with all endpoints
- IMPLEMENTATION_GUIDE.md for developers
- TECHNICAL_PLAN.md with architecture details
- CONTRIBUTING.md for contributors
- Issue and PR templates

## [0.1.0] - Development

### Added
- Project structure setup
- Core API client implementation
- Basic authentication module
- Initial UI framework

---

## Version History

- **1.0.0** - First stable release with full feature set
- **0.1.0** - Initial development version

## Links

- [GitHub Repository](https://github.com/bofika/IBMVS)
- [Issue Tracker](https://github.com/bofika/IBMVS/issues)
- [IBM Video Streaming API Documentation](https://developers.video.ibm.com/)