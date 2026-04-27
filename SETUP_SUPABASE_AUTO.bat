@echo off
echo ========================================
echo Supabase Automatic Setup
echo ========================================
echo.

echo Step 1: Opening Supabase SQL Editor...
start https://supabase.com/dashboard/project/zdkeisiffbncmvonqhdf/sql/new

timeout /t 3 /nobreak >nul

echo.
echo Step 2: Opening SQL file...
start notepad CREATE_TABLES.sql

echo.
echo ========================================
echo INSTRUCTIONS:
echo ========================================
echo.
echo 1. Supabase SQL Editor is now open in your browser
echo 2. The SQL file is open in Notepad
echo.
echo 3. In Notepad:
echo    - Press Ctrl+A (select all)
echo    - Press Ctrl+C (copy)
echo.
echo 4. In Supabase SQL Editor:
echo    - Click in the text area
echo    - Press Ctrl+V (paste)
echo    - Click "Run" button
echo.
echo 5. Wait for "Success" message
echo.
echo 6. Come back here and press any key to start the backend
echo.
pause

echo.
echo Starting backend server...
cd backend
start cmd /k "node server.js"

echo.
echo ========================================
echo Backend started!
echo ========================================
echo.
echo Your backend is now running on port 3001
echo.
echo Next: Open http://localhost:3000 and test Create Account
echo.
pause
