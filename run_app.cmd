@echo off
echo Starting Healthcare Form Data Extraction PoC...
echo.

REM Set window title
title Healthcare Form Data Extraction PoC

REM Create directories if they don't exist
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\screenshots" mkdir backend\screenshots

REM Check if .env file exists, if not copy from example
if not exist "backend\.env" (
    echo Creating .env file from .env.example...
    copy .env.example backend\.env
    echo Please update the .env file with your API keys if needed.
    echo.
)

REM Start the backend server in a new window
echo Starting backend server...
start "Healthcare Form Data Extraction - Backend" cmd /c "cd backend && .\.venv\Scripts\activate.bat && uvicorn app_compatible:app --reload --port 8001"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

REM Start the frontend server in a new window
echo Starting frontend server...
start "Healthcare Form Data Extraction - Frontend" cmd /c "cd frontend && npm run dev"

REM Open the application in the default browser
echo Opening application in browser...
timeout /t 3 /nobreak > nul
start http://localhost:5173

echo.
echo Healthcare Form Data Extraction PoC is now running!
echo.
echo Backend server: http://localhost:8001
echo Frontend server: http://localhost:5173
echo.
echo Press any key to stop the servers...
pause > nul

REM Kill the server processes when the user presses a key
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq Healthcare Form Data Extraction - Backend*" /F
taskkill /FI "WINDOWTITLE eq Healthcare Form Data Extraction - Frontend*" /F

echo Application stopped.
