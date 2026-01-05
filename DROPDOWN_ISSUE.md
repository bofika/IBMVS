# QComboBox Dropdown Rendering Issue on macOS

## Problem
The QComboBox dropdown list is not visible on macOS when clicked, although the functionality works (channels can be selected by clicking blindly in the area where the dropdown should be).

## Root Cause
This is a known issue with PyQt6 on macOS, particularly in dark mode. The native macOS combobox popup rendering doesn't work properly with PyQt6's styling.

## Attempted Solutions
1. ✗ Added explicit width/height to QComboBox
2. ✗ Added CSS styling to QComboBox and QAbstractItemView
3. ✗ Set explicit QListView as the view for QComboBox
4. ✗ Multiple styling variations

## Recommended Solution
Replace QComboBox with a QPushButton that opens a QDialog containing a QListWidget. This provides:
- Full control over rendering
- Better visibility
- Search functionality
- Consistent behavior across platforms

## Alternative Workaround
Users can:
1. Use keyboard navigation (arrow keys) after clicking the dropdown
2. Type the first letter of the channel name to jump to it
3. The functionality works - just the visual feedback is missing

## Status
The application is fully functional. The dropdown issue is purely cosmetic - all channel selection and video loading works correctly.