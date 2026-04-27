@echo off
echo ========================================
echo PestVid Complete System Test
echo ========================================
echo.

echo Step 1: Checking if backend is running...
echo.
curl -s http://localhost:3001 >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Backend is not running!
    echo Please start the backend first:
    echo   cd PestVid-main\backend
    echo   node server.js
    echo.
    pause
    exit /b 1
)

echo [OK] Backend is running
echo.

echo Step 2: Testing backend API endpoint...
echo.
curl -s http://localhost:3001
echo.
echo.

echo Step 3: Testing user registration...
echo.
curl -X POST http://localhost:3001/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test Farmer\",\"email\":\"testfarmer%RANDOM%@example.com\",\"password\":\"password123\",\"role\":\"farmer\"}"
echo.
echo.

echo Step 4: Testing user login...
echo.
curl -X POST http://localhost:3001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"testfarmer@example.com\",\"password\":\"password123\"}"
echo.
echo.

echo ========================================
echo Test Results
echo ========================================
echo.
echo If you see:
echo   - "PestiVid Backend API (Supabase) is running" = Backend OK
echo   - "User registered successfully" = Registration OK
echo   - "Logged in successfully" or "Invalid credentials" = Login endpoint OK
echo.
echo If you see errors:
echo   - "SUPABASE_SERVICE_KEY is not set" = Add service key to .env
echo   - "relation 'users' does not exist" = Run SQL script in Supabase
echo   - "Invalid API key" = Check your Supabase keys
echo.
echo ========================================
pause
