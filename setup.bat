@echo off
REM AI-Powered Jira Dashboard Setup Script for Windows
REM This script helps you set up all three components of the system

echo.
echo AI-Powered Jira Dashboard Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed. Please install Python 3.9 or higher.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18 or higher.
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM Setup Jira Tool Server
echo Setting up Jira Tool Server...
cd jira-tool-server

if not exist ".env" (
    copy .env.example .env
    echo [WARNING] Created .env file. Please edit jira-tool-server\.env with your Jira credentials.
) else (
    echo [OK] .env file already exists
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Installing dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
call deactivate

echo [OK] Jira Tool Server setup complete
echo.

REM Setup Agent Server
echo Setting up Agent Server...
cd ..\agent-server

if not exist ".env" (
    copy .env.example .env
    echo [WARNING] Created .env file. Please edit agent-server\.env with your API keys.
) else (
    echo [OK] .env file already exists
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Installing dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
call deactivate

echo [OK] Agent Server setup complete
echo.

REM Setup Frontend
echo Setting up Frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
) else (
    echo [OK] Dependencies already installed
)

echo [OK] Frontend setup complete
echo.

REM Final instructions
echo ====================================
echo Setup Complete!
echo.
echo Next steps:
echo.
echo 1. Configure your environment variables:
echo    - Edit jira-tool-server\.env with your Jira credentials and project key
echo    - Edit agent-server\.env with your LangSmith and LLM provider API keys
echo.
echo 2. Start the servers (in separate terminals):
echo.
echo    Terminal 1 - Jira Tool Server:
echo    $ cd jira-tool-server
echo    $ venv\Scripts\activate.bat
echo    $ python app.py
echo.
echo    Terminal 2 - Agent Server:
echo    $ cd agent-server
echo    $ venv\Scripts\activate.bat
echo    $ python app.py
echo.
echo    Terminal 3 - Frontend:
echo    $ cd frontend
echo    $ npm run dev
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo For detailed setup instructions, see:
echo   - README.md (main documentation)
echo   - LANGSMITH_SETUP.md (LangSmith configuration)
echo.
echo Happy coding!
echo.

cd ..

