@echo off
echo ========================================
echo Testing Supabase Backend Connection
echo ========================================
echo.

echo 1. Testing if backend is running...
curl -s http://localhost:3001
echo.
echo.

echo 2. Testing user registration...
curl -X POST http://localhost:3001/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test Farmer\",\"email\":\"testfarmer@example.com\",\"password\":\"password123\",\"role\":\"farmer\"}"
echo.
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If you see success messages above, your backend is working!
echo If you see errors, check:
echo   1. Backend is running (node backend/server.js)
echo   2. Service role key is in backend/.env
echo   3. SQL tables are created in Supabase
echo.
pause
