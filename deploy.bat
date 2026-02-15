@echo off
REM Asclepius Backend Deployment Script
REM This script deploys the fixed backend to Google Cloud Run

echo ==========================================
echo   Asclepius Backend Deployment
echo ==========================================
echo.

REM Check if gcloud is installed
gcloud version >nul 2>&1
if errorlevel 1 (
    echo ERROR: gcloud is not installed or not in PATH
    echo Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Navigate to backend directory
cd /d "%~dp0backend"
if not exist "Dockerfile" (
    echo ERROR: Dockerfile not found in backend directory
    pause
    exit /b 1
)

echo.
echo Starting deployment...
echo Project: asclepius-300388107814
echo Region: asia-south1
echo Service: asclepius-backend
echo.

REM Deploy to Cloud Run
gcloud run deploy asclepius-backend ^
    --source . ^
    --region asia-south1 ^
    --allow-unauthenticated ^
    --timeout 3600 ^
    --memory 2Gi ^
    --cpu 2 ^
    --port 8000

if errorlevel 1 (
    echo.
    echo ERROR: Deployment failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Deployment Successful!
echo ==========================================
echo.
echo Your backend is now deployed at:
echo https://asclepius-backend-asia-south1-run.app
echo.
echo Test with:
echo curl https://asclepius-backend-asia-south1-run.app/health
echo.
echo To view logs:
echo gcloud run logs read asclepius-backend --region asia-south1
echo.
pause

