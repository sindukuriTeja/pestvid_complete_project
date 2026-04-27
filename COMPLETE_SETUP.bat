@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                    PESTIVID COMPLETE SETUP                                 ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

echo Testing Supabase connection...
cd backend
node test-supabase-connection.js
cd ..

echo.
echo ========================================
echo.
echo Do you want to:
echo   1. Create tables in Supabase (opens browser)
echo   2. Start backend with Supabase
echo   3. Start backend with simple JSON files
echo   4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto create_tables
if "%choice%"=="2" goto start_supabase
if "%choice%"=="3" goto start_simple
if "%choice%"=="4" goto end

:create_tables
echo.
echo Opening Supabase SQL Editor...
start https://supabase.com/dashboard/project/zdkeisiffbncmvonqhdf/sql/new
timeout /t 2 /nobreak >nul

echo Opening SQL file...
start notepad CREATE_TABLES.sql

echo.
echo ========================================
echo COPY-PASTE INSTRUCTIONS:
echo ========================================
echo.
echo 1. In Notepad (SQL file):
echo    - Press Ctrl+A (select all)
echo    - Press Ctrl+C (copy)
echo.
echo 2. In Browser (Supabase):
echo    - Click in the text area
echo    - Press Ctrl+V (paste)
echo    - Click "Run" button
echo    - Wait for "Success"
echo.
echo 3. Come back here and press any key
echo.
pause
goto start_supabase

:start_supabase
echo.
echo Starting backend with Supabase...
cd backend
start cmd /k "echo Backend with Supabase && node server.js"
cd ..
timeout /t 2 /nobreak >nul

echo.
echo Starting frontend...
cd public
start cmd /k "echo Frontend Server && python -m http.server 3000"
cd ..

echo.
echo ========================================
echo ✅ SERVERS STARTED!
echo ========================================
echo.
echo Backend: http://localhost:3001 (Supabase)
echo Frontend: http://localhost:3000
echo.
echo Open: http://localhost:3000
echo Test: Create Account button
echo.
goto end

:start_simple
echo.
echo Starting backend with JSON files...
cd backend
start cmd /k "echo Backend with JSON && node server-simple.js"
cd ..
timeout /t 2 /nobreak >nul

echo.
echo Starting frontend...
cd public
start cmd /k "echo Frontend Server && python -m http.server 3000"
cd ..

echo.
echo ========================================
echo ✅ SERVERS STARTED!
echo ========================================
echo.
echo Backend: http://localhost:3001 (JSON Files)
echo Frontend: http://localhost:3000
echo.
echo Open: http://localhost:3000
echo Test: Create Account button
echo.
echo NOTE: JSON files work locally but NOT for hosting!
echo.
goto end

:end
echo.
echo Press any key to exit...
pause >nul
