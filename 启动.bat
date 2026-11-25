@echo off
setlocal
cd /d "%~dp0"
title Campus Panorama - Local Server
set "PORT=8000"
set "SERVER="

where python >nul 2>nul
if not errorlevel 1 set "SERVER=python -m http.server %PORT% --bind 127.0.0.1"

if not defined SERVER (
  where node >nul 2>nul
  if not errorlevel 1 set "SERVER=node server.js"
)

if not defined SERVER goto nopython

echo.
echo   Jiangsu Electronic Information Vocational College
echo   720 Campus Panorama
echo.
echo   Starting local server at http://127.0.0.1:%PORT%/
echo.
start "" /b %SERVER%
ping -n 3 127.0.0.1 >nul
start "" "http://127.0.0.1:%PORT%/"
echo   Server is running. Keep this window open while viewing.
echo   Close this window to stop the server.
echo.
pause >nul
goto :eof

:nopython
echo.
echo   Python or Node.js was not found on this computer.
echo.
echo   Install Python 3 from https://www.python.org/downloads/
echo   and tick "Add Python to PATH" during setup, then run this file again.
echo.
echo   (Or install Node.js from https://nodejs.org/ and run this file.)
echo.
pause
