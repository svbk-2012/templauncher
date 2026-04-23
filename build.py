"""
Build script to create standalone executable using PyInstaller
"""
import os
import sys
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")

def build_executable():
    """Build the standalone executable"""
    install_pyinstaller()
    
    # Import PyInstaller
    import PyInstaller.__main__
    
    # Build options
    build_args = [
        'main.py',
        '--onefile',                    # Create single executable
        '--windowed',                   # No console window
        '--name=UniversalAppRunner',    # Name of the executable
        '--clean',                      # Clean old builds
        '--noconfirm',                  # Don't ask for confirmation
        '--distpath=dist',              # Output directory
        '--workpath=build',             # Build directory
        '--specpath=.',                 # Spec file location
    ]
    
    # Add icon if it exists
    if os.path.exists('icon.ico'):
        build_args.append('--icon=icon.ico')
        print("Using custom icon")
    else:
        print("No icon.ico found, using default icon")
    
    print("Building executable...")
    print(f"Command: pyinstaller {' '.join(build_args)}")
    
    # Build the executable
    PyInstaller.__main__.run(build_args)
    
    print("Build completed!")
    print(f"Executable created: {Path('dist/UniversalAppRunner.exe').absolute()}")

def create_zip():
    """Create a zip file with the executable"""
    import zipfile
    
    zip_path = "UniversalAppRunner.zip"
    exe_path = "dist/UniversalAppRunner.exe"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.exists(exe_path):
            zipf.write(exe_path, "UniversalAppRunner.exe")
            print(f"Added {exe_path} to zip")
        
        # Add README if it exists
        if os.path.exists("README.md"):
            zipf.write("README.md", "README.md")
            print("Added README.md to zip")
    
    print(f"Zip file created: {Path(zip_path).absolute()}")

if __name__ == "__main__":
    print("=== Universal App Runner Build Script ===")
    print()
    
    try:
        build_executable()
        print()
        create_zip()
        print()
        print("=== Build Complete ===")
        print("Files created:")
        print(f"  - Executable: {Path('dist/UniversalAppRunner.exe').absolute()}")
        print(f"  - Zip file: {Path('UniversalAppRunner.zip').absolute()}")
        print()
        print("You can now distribute the .exe file or the .zip file to users.")
        print("Users only need to download and run the executable - no installation required!")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)
