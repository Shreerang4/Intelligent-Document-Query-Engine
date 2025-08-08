@echo off
echo === Deploying Updated RAG API to Railway ===

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ Error: main.py not found. Please run this script from the project root.
    exit /b 1
)

echo ✅ Found main.py

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Railway CLI not found. Please install it first:
    echo npm install -g @railway/cli
    exit /b 1
)

echo ✅ Railway CLI found

REM Deploy to Railway
echo 🚀 Deploying to Railway...
railway up

echo ✅ Deployment completed!
echo.
echo 📋 Next steps:
echo 1. Test the health endpoint: https://bajajhack-production-cf2c.up.railway.app/health
echo 2. Run the hackathon test: python test_hackathon.py
echo 3. Or use PowerShell: .\test_hackathon.ps1
echo.
echo 🔧 The application now supports up to 10 questions for hackathon requirements. 