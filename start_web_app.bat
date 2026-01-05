@echo off
REM IBM Video Streaming Manager - Web Application Launcher (Windows)
REM This script starts the Flask web application

echo =========================================
echo IBM Video Streaming Manager - Web App
echo =========================================
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo WARNING: Flask is not installed!
    echo.
    echo Installing Flask and dependencies...
    pip install Flask Flask-CORS
    echo.
)

echo Starting web server...
echo.
echo Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo =========================================
echo.

REM Start the Flask application
python web_app.py

pause

@REM Made with Bob
