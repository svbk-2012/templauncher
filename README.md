# Launcher Wrapper

A desktop application that acts as a wrapper for downloaders and installers. Instead of running launchers directly in Windows, you can drag and drop them into this app, which will execute the download process and save the actual application files for you.

## Features

- **Drag & Drop Interface**: Simply drag launcher files (.exe, .msi, .zip) into the app
- **Automatic Download Monitoring**: Detects and saves downloaded files automatically
- **File Organization**: Organizes downloaded apps with timestamps in the downloads folder
- **Process Control**: Start, stop, and monitor download progress
- **File Management**: View and access all downloaded applications

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Drag and drop a launcher file into the drop zone
3. Click "Launch Download" to start the download process
4. The app will monitor and automatically save downloaded files
5. Access downloaded apps from the list or open the downloads folder

## Supported File Types

- `.exe` - Windows executables and installers
- `.msi` - Windows Installer packages
- `.zip` - Compressed archives
- `.7z` - 7-Zip archives
- `.rar` - RAR archives

## How It Works

1. You drop a launcher file into the app
2. The app creates a temporary session directory
3. The launcher is executed in an isolated environment
4. File monitoring detects new files created during download
5. Downloaded files are automatically moved to the downloads folder
6. Files are organized with timestamps for easy identification

## Download Location

Downloaded applications are saved to:
```
~/Downloads/LauncherWrapper/
```

## Safety Notes

- Always verify the source of launcher files before using
- The app runs launchers in isolated sessions but doesn't provide full sandboxing
- Scan downloaded files with antivirus before opening
