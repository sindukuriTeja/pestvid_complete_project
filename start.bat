@echo off
title PestVid - Startup
color 0A

echo.
echo  ==========================================
echo     PestVid - Agricultural Blockchain
echo     Starting All Services...
echo  ==========================================
echo.

REM ---- Check Node.js ----
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Node.js is not installed. Please install from https://nodejs.org
    pause
    exit /b 1
)

REM ---- Install backend deps if needed ----
if not exist "backend\node_modules" (
    echo  [SETUP] Installing backend dependencies...
    cd backend && npm install && cd ..
    echo  [OK] Backend dependencies installed.
)

REM ---- Start Node.js Backend on port 3001 ----
echo  [1/2] Starting Node.js Backend (port 3001)...
start "PestVid - Backend API" cmd /k "cd /d %~dp0backend && node server.js"
timeout /t 3 /nobreak >nul

REM ---- Start Frontend on port 3000 using node server.js ----
echo  [2/2] Starting Frontend Server (port 3000)...

echo  [SETUP] Checking frontend server dependencies...
if not exist "%~dp0public\node_modules\express" (
    echo  [SETUP] Installing express for frontend server...
    cd /d %~dp0public && npm install express
)
start "PestVid - Frontend" cmd /k "cd /d %~dp0public && node server.js"

timeout /t 2 /nobreak >nul
echo.
echo  ==========================================
echo   PestVid is Running!
echo  ==========================================
echo.
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:3001/api
echo   Flask AI:  http://localhost:5000

echo.
echo  [3/3] Starting Flask AI Server (port 5000)...
where python >nul 2>&1
if %errorlevel% equ 0 (
    start "PestVid - Flask AI" cmd /k "cd /d %~dp0 && python flask_server.py"
) else (
    echo  [WARN] Python is not found. Please install Python to run the AI server.
)
echo.
echo   Demo Accounts:
echo     Farmer:   demo.farmer@example.com / password123
echo     Buyer:    demo.buyer@example.com  / password123
echo     Investor: demo.investor@example.com / password123
echo.

start "" "http://localhost:3000"

:done
echo  Press any key to close this launcher...
pause >nul
