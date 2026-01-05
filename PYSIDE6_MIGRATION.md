# PySide6 Migration Guide

## What Changed

We've migrated from PyQt6 to PySide6 to resolve the table refresh issue on macOS. PySide6 is the official Qt binding from the Qt Company and may have different rendering behavior.

## Installation Steps

### 1. Uninstall PyQt6

```bash
pip uninstall PyQt6 PyQt6-WebEngine -y
```

### 2. Install PySide6

```bash
pip install PySide6
```

### 3. Install Other Dependencies

```bash
pip install -r requirements.txt
```

## What Was Changed

- All imports changed from `PyQt6` to `PySide6`
- Signal decorator changed from `pyqtSignal` to `Signal`
- All functionality remains the same - API is nearly identical

## Testing

After installation, run the application:

```bash
python3 src/main.py
```

Test the video status toggle feature:
1. Select "Bofika Test Channel"
2. Toggle a video status
3. Check if the table updates visually

## If Issues Persist

If PySide6 doesn't resolve the table refresh issue, we have two options:

1. **Refactor to QTableView + QAbstractTableModel** (complex but keeps all features)
2. **Switch to Tkinter** (simpler but loses browser integration for monitoring)

## Rollback

To rollback to PyQt6:

```bash
pip uninstall PySide6 -y
pip install PyQt6 PyQt6-WebEngine
```

Then run:
```bash
find src -name "*.py" -type f -exec sed -i '' 's/from PySide6/from PyQt6/g' {} \;
find src -name "*.py" -type f -exec sed -i '' 's/import PySide6/import PyQt6/g' {} \;
sed -i '' 's/Signal/pyqtSignal/g' src/ui/videos_panel.py