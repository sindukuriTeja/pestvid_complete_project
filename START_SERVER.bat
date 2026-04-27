@echo off
echo ============================================================
echo PestVid Flask Server Startup
echo ============================================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Testing model loading...
python test_model_loading.py
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Model loading test failed!
    echo ============================================================
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo   1. Missing dependencies - run: pip install torch transformers pillow
    echo   2. Missing model files - ensure .pth files are present
    echo   3. Corrupted model files - re-download the models
    echo ============================================================
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Starting Flask server with PyTorch models...
echo ============================================================
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python flask_server_with_models.py

pause
