@echo off
echo ========================================
echo PestVid Setup Checker
echo ========================================
echo.

cd PestVid-main\backend

echo Checking configuration...
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please create backend/.env file
    pause
    exit /b 1
)

REM Check for service key placeholder
findstr /C:"YOUR_SERVICE_ROLE_KEY_HERE" .env >nul
if %errorlevel% equ 0 (
    echo [ERROR] Service role key not configured!
    echo.
    echo Please update backend/.env with your actual service_role key:
    echo 1. Go to: https://supabase.com/dashboard/project/zdkeisiffbncmvonqhdf/settings/api
    echo 2. Copy the service_role key
    echo 3. Replace YOUR_SERVICE_ROLE_KEY_HERE in .env
    echo.
    pause
    exit /b 1
)

echo [OK] Service role key is configured
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo [WARNING] node_modules not found
    echo Installing dependencies...
    call npm install
    echo.
)

echo [OK] Dependencies installed
echo.

echo ========================================
echo Configuration Check Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure you created database tables in Supabase
echo    (See FINAL_SETUP_STEPS.md Step 2)
echo 2. Start the backend: node server.js
echo 3. Start the frontend: python -m http.server 3000
echo.
pause
