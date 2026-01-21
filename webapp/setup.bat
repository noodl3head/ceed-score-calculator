@echo off
echo ===================================
echo CEED Score Calculator - Setup Script
echo ===================================
echo.

echo Step 1: Setting up Backend...
cd webapp\backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file from template...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it with your Supabase credentials.
) else (
    echo .env file already exists.
)

echo.
echo ===================================
echo Step 2: Setting up Frontend...
cd ..\frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo Creating .env file from template...
if not exist .env (
    copy .env.example .env
    echo .env file created!
) else (
    echo .env file already exists.
)

cd ..\..

echo.
echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo IMPORTANT: Before running the app:
echo 1. Edit webapp\backend\.env with your Supabase credentials
echo 2. Run the SQL setup in your Supabase dashboard (see QUICKSTART.md)
echo.
echo To start the application:
echo.
echo Backend (in one terminal):
echo   cd webapp\backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Frontend (in another terminal):
echo   cd webapp\frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo ===================================

pause
