@echo off
echo Building Universal App Runner...
echo.

cd /d "%~dp0"

python build.py

echo.
echo Build complete!
echo.
echo Check the 'dist' folder for UniversalAppRunner.exe
echo Check for UniversalAppRunner.zip file
echo.
pause
