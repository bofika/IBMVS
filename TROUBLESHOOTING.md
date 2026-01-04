# Troubleshooting Guide

This guide covers common issues and their solutions when installing and running the IBM Video Streaming Manager.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Python Issues](#python-issues)
- [Dependency Issues](#dependency-issues)
- [Runtime Errors](#runtime-errors)
- [API Connection Issues](#api-connection-issues)
- [Platform-Specific Issues](#platform-specific-issues)

---

## Installation Issues

### "python: command not found" (macOS/Linux)

**Problem**: The `python` command is not recognized.

**Solution**: On macOS and many Linux distributions, Python 3 is accessed via `python3`:

```bash
# Use python3 instead
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

**Alternative**: Create an alias (macOS/Linux):
```bash
echo 'alias python=python3' >> ~/.zshrc  # or ~/.bashrc
echo 'alias pip=pip3' >> ~/.zshrc
source ~/.zshrc
```

### Python Not Installed

**macOS**:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3

# Verify installation
python3 --version
```

**Windows**:
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify: Open Command Prompt and run `python --version`

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Virtual Environment Creation Fails

**Error**: `No module named venv`

**Solution**:
```bash
# macOS/Linux
python3 -m pip install --user virtualenv
python3 -m virtualenv venv

# Windows
python -m pip install --user virtualenv
python -m virtualenv venv
```

### Virtual Environment Won't Activate

**macOS/Linux**:
```bash
# Try with dot command
. ./venv/bin/activate

# Or use full path
source $(pwd)/venv/bin/activate

# Check if file exists
ls -la venv/bin/activate
```

**Windows PowerShell** (Execution Policy Error):
```powershell
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\activate
```

**Windows Command Prompt**:
```cmd
venv\Scripts\activate.bat
```

---

## Python Issues

### Wrong Python Version

**Check your version**:
```bash
python --version  # or python3 --version
```

**Required**: Python 3.9 or higher

**Solution**: Install the correct version:
- macOS: `brew install python@3.11`
- Windows: Download from python.org
- Linux: `sudo apt install python3.11`

### Multiple Python Versions Conflict

**Solution**: Use specific version:
```bash
# macOS/Linux
python3.11 -m venv venv

# Windows
py -3.11 -m venv venv
```

---

## Dependency Issues

### PyQt6 Installation Fails

**macOS**:
```bash
# Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel

# Install PyQt6
pip install PyQt6

# If still fails, try:
brew install qt6
pip install PyQt6
```

**Windows**:
```bash
# Ensure Visual C++ redistributables are installed
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

# Then install PyQt6
pip install --upgrade pip setuptools wheel
pip install PyQt6
```

**Linux**:
```bash
# Install system dependencies
sudo apt install python3-pyqt6 libqt6widgets6

# Or install via pip
pip install PyQt6
```

### "No module named 'requests'" or Similar

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt

# If that fails, install individually:
pip install requests
pip install PyQt6
pip install keyring
pip install python-vlc
```

### SSL Certificate Errors During Installation

**Solution**:
```bash
# macOS
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Or update certificates
/Applications/Python\ 3.*/Install\ Certificates.command

# Windows/Linux
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Permission Denied During Installation

**Solution**:
```bash
# Don't use sudo! Use virtual environment instead
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# If you must install globally (not recommended):
pip install --user -r requirements.txt
```

---

## Runtime Errors

### "ModuleNotFoundError" When Running

**Problem**: Virtual environment not activated or dependencies not installed.

**Solution**:
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Verify activation (should show venv path)
which python  # macOS/Linux
where python  # Windows

# Install dependencies
pip install -r requirements.txt
```

### "ImportError: cannot import name 'QApplication'"

**Problem**: PyQt6 not properly installed.

**Solution**:
```bash
# Uninstall and reinstall PyQt6
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6

# Verify installation
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

### VLC Player Not Found

**Error**: "VLC player not found" or "No module named 'vlc'"

**Solution**:

**macOS**:
```bash
# Install VLC
brew install --cask vlc

# Install python-vlc
pip install python-vlc
```

**Windows**:
1. Download VLC from https://www.videolan.org/
2. Install VLC (use default installation path)
3. Install python-vlc: `pip install python-vlc`

**Linux**:
```bash
sudo apt install vlc
pip install python-vlc
```

### Keyring/Credential Storage Errors

**Error**: "Failed to unlock keyring" or "No keyring backend available"

**Solution**:

**macOS**: Should work by default with Keychain

**Linux**:
```bash
# Install keyring backend
sudo apt install gnome-keyring
# or
sudo apt install python3-secretstorage
```

**Windows**: Should work by default with Windows Credential Manager

**Workaround** (if keyring fails):
Edit `src/core/auth.py` to use file-based storage (less secure):
```python
# Temporarily store in config file instead of keyring
# (Not recommended for production)
```

---

## API Connection Issues

### "Failed to connect to API"

**Possible causes**:
1. Invalid API credentials
2. No internet connection
3. API endpoint is down
4. Firewall blocking connection

**Solutions**:

1. **Verify credentials**:
   - Go to Settings → API Configuration
   - Re-enter API key and secret
   - Test connection

2. **Check internet**:
   ```bash
   ping api.video.ibm.com
   ```

3. **Check firewall**:
   - Ensure port 443 (HTTPS) is not blocked
   - Try disabling VPN temporarily

4. **Test API manually**:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" https://api.video.ibm.com/channels.json
   ```

### "SSL: CERTIFICATE_VERIFY_FAILED"

**Solution**:
```bash
# macOS - Install certificates
/Applications/Python\ 3.*/Install\ Certificates.command

# Or update certifi
pip install --upgrade certifi

# Windows - Update certificates
pip install --upgrade certifi
```

### Rate Limiting Errors

**Error**: "429 Too Many Requests"

**Solution**: The application has built-in rate limiting, but if you still hit limits:
- Wait a few minutes before retrying
- Reduce the frequency of API calls
- Check if you have multiple instances running

---

## Platform-Specific Issues

### macOS

#### "App is damaged and can't be opened"

**Solution**:
```bash
# Remove quarantine attribute
xattr -cr /path/to/app

# Or allow in System Preferences
# System Preferences → Security & Privacy → Allow
```

#### Gatekeeper Blocking

**Solution**:
```bash
# Right-click app → Open (first time only)
# Or disable Gatekeeper temporarily:
sudo spctl --master-disable
```

#### Permission Issues

**Solution**:
```bash
# Fix permissions
chmod +x src/main.py
chmod -R 755 venv/
```

### Windows

#### "Windows protected your PC"

**Solution**:
- Click "More info"
- Click "Run anyway"

#### Antivirus Blocking

**Solution**:
- Add application folder to antivirus exclusions
- Temporarily disable antivirus during installation

#### Path Too Long Error

**Solution**:
```powershell
# Enable long paths in Windows
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Linux

#### Missing System Libraries

**Ubuntu/Debian**:
```bash
sudo apt install python3-dev python3-pip
sudo apt install libxcb-xinerama0 libxcb-cursor0
sudo apt install qt6-base-dev
```

**Fedora/RHEL**:
```bash
sudo dnf install python3-devel python3-pip
sudo dnf install qt6-qtbase-devel
```

#### Display Issues

**Solution**:
```bash
# Set Qt platform
export QT_QPA_PLATFORM=xcb

# Or try wayland
export QT_QPA_PLATFORM=wayland
```

---

## Getting Help

If you're still experiencing issues:

1. **Check logs**: Look in `logs/app.log` for detailed error messages

2. **Search existing issues**: https://github.com/bofika/IBMVS/issues

3. **Create a new issue**: Include:
   - Operating system and version
   - Python version (`python --version`)
   - Error message (full traceback)
   - Steps to reproduce
   - Log file contents

4. **Community support**: Check the discussions section

---

## Quick Reference

### Verify Installation

```bash
# Check Python
python3 --version  # Should be 3.9+

# Check pip
pip --version

# Check virtual environment
which python  # Should point to venv

# Check dependencies
pip list | grep -E "PyQt6|requests|keyring"

# Test imports
python -c "from PyQt6.QtWidgets import QApplication; print('OK')"
```

### Clean Reinstall

```bash
# Remove virtual environment
rm -rf venv/

# Remove cache
rm -rf __pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} +

# Recreate environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Reset Application Data

```bash
# macOS
rm -rf ~/Library/Application\ Support/IBM\ Video\ Manager/

# Windows
rmdir /s "%APPDATA%\IBM Video Manager"

# Linux
rm -rf ~/.local/share/IBM\ Video\ Manager/
```

---

**Last Updated**: 2026-01-04