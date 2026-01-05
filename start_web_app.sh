#!/bin/bash

# IBM Video Streaming Manager - Web Application Launcher
# This script starts the Flask web application

echo "========================================="
echo "IBM Video Streaming Manager - Web App"
echo "========================================="
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask is not installed!"
    echo ""
    echo "Installing Flask and dependencies..."
    pip3 install Flask Flask-CORS
    echo ""
fi

# Check if credentials exist
if [ ! -f "$HOME/Library/Application Support/IBM Video Manager/credentials.json" ]; then
    echo "ℹ️  No credentials found. You'll need to configure them in Settings."
    echo ""
fi

echo "Starting web server..."
echo ""
echo "📱 Access the application at: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "========================================="
echo ""

# Start the Flask application
python3 web_app.py

# Made with Bob
