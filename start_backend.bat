@echo off
echo ============================================================
echo Starting PestVid Backend Server
echo ============================================================
echo.
echo IMPORTANT: MongoDB must be running first!
echo.
echo Server will run on: http://localhost:3001
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd backend
npm start

pause
