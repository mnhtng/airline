@echo off
echo ========================================
echo Starting Airline Application
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM === Start Backend (FastAPI) ===
echo [1/2] Starting Backend Server...
cd /d "%SCRIPT_DIR%backend"
start "Airline Backend" cmd /k ".venv\Scripts\activate && fastapi dev main.py"
echo Backend server starting at http://localhost:8000
echo.

REM Wait a moment for backend to initialize
timeout /t 2 /nobreak >nul

REM === Start Frontend (Vite) ===
echo [2/2] Starting Frontend Server...
cd /d "%SCRIPT_DIR%frontend"
start "Airline Frontend" cmd /k "npm run dev"
echo Frontend server starting at http://localhost:5173
echo.

REM Wait for frontend to initialize
timeout /t 1 /nobreak >nul

REM === Open Frontend in Browser ===
start "" "http://localhost:5173"
echo.

echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
