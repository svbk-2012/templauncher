# Universal App Runner

A desktop application that acts as a universal wrapper for launchers and applications. It supports two modes:

1. **Launcher Mode** - Download and save applications from installers/launchers
2. **App Mode** - Run applications directly in temporary environments

## Features

- **Dual Mode Operation**: Switch between Launcher Mode and App Mode
- **Drag & Drop Interface**: Simply drag files into the app
- **Automatic Download Monitoring**: Detects and saves downloaded files automatically
- **File Organization**: Organizes files with timestamps
- **Process Control**: Start, stop, and monitor running processes
- **Self-Contained**: Auto-installs dependencies, no manual setup needed

## Quick Start (For Users)

### Option 1: Download Standalone Executable (Recommended)
1. Download `UniversalAppRunner.exe` from the [Releases](../../releases) page
2. Double-click to run - no installation required!

### Option 2: Run from Source
1. Clone this repository
2. Run `python main.py` or double-click `run.bat`

## Usage

### Launcher Mode (Download & Save)
1. Select "Launcher Mode" 
2. Drag and drop installer/launcher files (.exe, .msi, .zip)
3. Click "Launch Download"
4. The app monitors and saves downloaded files automatically

### App Mode (Run Directly)
1. Select "App Mode"
2. Drag and drop applications/games (.exe, .bat)
3. Click "Run Application"
4. The app runs in a temporary environment

## For Developers - Building the Executable

### Prerequisites
- Python 3.6 or higher
- Windows (for .exe build)

### Build Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/universal-app-runner.git
   cd universal-app-runner
   ```

2. **Build the executable:**
   ```bash
   python build.py
   ```

3. **Find your files:**
   - Executable: `dist/UniversalAppRunner.exe`
   - Zip file: `UniversalAppRunner.zip`

### Manual Build (Alternative)
```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name=UniversalAppRunner main.py
```

## Supported File Types

### Launcher Mode
- `.exe` - Windows executables and installers
- `.msi` - Windows Installer packages
- `.zip` - Compressed archives
- `.7z` - 7-Zip archives
- `.rar` - RAR archives

### App Mode
- `.exe` - Windows applications and games
- `.bat` - Batch files
- `.cmd` - Command files

## How It Works

### Launcher Mode
1. You drop a launcher file into the app
2. Creates a temporary session directory
3. Executes the launcher in isolated environment
4. Monitors for new files created during download
5. Automatically moves downloaded files to permanent storage
6. Files are organized with timestamps

### App Mode
1. You drop an application file into the app
2. Creates a temporary execution environment
3. Runs the application directly from temp directory
4. Allows playing games or using apps without permanent installation

## File Locations

- **Downloaded apps**: `~/Downloads/UniversalRunner/`
- **Temporary files**: `~/Downloads/UniversalRunner/temp/`

## Safety Notes

- Always verify the source of files before using
- The app runs files in isolated sessions but doesn't provide full sandboxing
- Scan downloaded files with antivirus before opening
- Use App Mode for trusted applications only

## GitHub Distribution

### For End Users
- Download the standalone executable from Releases
- No installation or setup required

### For Developers
- Clone the repository for source code
- Use the build script to create your own executable
- Modify and redistribute under the same license

## Requirements

- **For running the executable**: None (self-contained)
- **For building from source**: Python 3.6+, Windows OS
- **Dependencies**: Auto-installed by the application
