@echo off
echo Starting CEED Score Calculator...
echo.

start "Backend Server" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python app.py"

timeout /t 3 /nobreak >nul

start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C in each terminal window to stop the servers.
