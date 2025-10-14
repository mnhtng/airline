@echo off
echo ========================================
echo Stopping Airline Application
echo ========================================
echo.

echo Stopping Backend Server (Python/FastAPI)...
taskkill /F /IM python.exe /T >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend stopped successfully
) else (
    echo [INFO] No backend process found
)
echo.

echo Stopping Frontend Server (Node/Vite)...
taskkill /F /IM node.exe /T >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Frontend stopped successfully
) else (
    echo [INFO] No frontend process found
)
echo.

echo ========================================
echo All servers stopped!
echo ========================================
echo.
pause
