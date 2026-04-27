@echo off
REM PestVid - Start All Servers Script
REM This script starts both Flask AI server and Node.js backend

echo ========================================
echo    PestVid Server Startup Script
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "flask_server.py" (
    echo ERROR: Please run this script from the PestVid-main directory
    pause
    exit /b 1
)

echo [1/3] Starting Flask AI Server (Port 5000)...
echo.
start "PestVid Flask AI Server" cmd /k "python flask_server.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Node.js Backend (Port 3001)...
echo.
start "PestVid Node Backend" cmd /k "cd backend && npm start"
timeout /t 3 /nobreak >nul

echo [3/3] Opening Frontend...
echo.
start "" "public\index.html"

echo.
echo ========================================
echo    All Servers Started Successfully!
echo ========================================
echo.
echo Flask AI Server:  http://localhost:5000
echo Node.js Backend:  http://localhost:3001
echo Frontend:         public/index.html
echo.
echo Press any key to close this window...
echo (Servers will continue running in separate windows)
pause >nul
