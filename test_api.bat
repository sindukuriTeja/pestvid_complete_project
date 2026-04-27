@echo off
echo ============================================================
echo Testing PestVid API Endpoints
echo ============================================================
echo.
echo Make sure Flask server is running on port 5000
echo.

echo Testing health check...
curl http://localhost:5000/
echo.
echo.

echo Testing quick tips...
curl http://localhost:5000/quick-tips
echo.
echo.

echo Testing AI advice...
curl -X POST http://localhost:5000/simple-ai-advice -H "Content-Type: application/json" -d "{\"query\": \"How to grow tomatoes?\"}"
echo.
echo.

echo ============================================================
echo Test complete!
echo ============================================================
pause
