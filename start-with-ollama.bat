@echo off
REM Quick start script for Jira Dashboard with Ollama (Windows)

echo.
echo Jira Dashboard with Ollama - Quick Start
echo ============================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama is not installed.
    echo.
    echo Please install Ollama first:
    echo   Download from https://ollama.com/download/windows
    echo.
    exit /b 1
)

echo [OK] Ollama is installed
echo.

REM Check if Ollama is running
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running. Please start Ollama from the Start menu.
    echo.
    pause
)

echo [OK] Ollama is running
echo.

REM Check if llama3.1 model is available
ollama list | findstr "llama3.1" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Downloading Llama 3.1 model (this may take a few minutes)...
    ollama pull llama3.1
)

echo [OK] Llama 3.1 model is ready
echo.

REM Update .env file if it exists
if exist "agent-server\.env" (
    echo Updating agent-server\.env for Ollama...
    
    REM Create a temporary file with updated config
    (
        for /f "delims=" %%i in (agent-server\.env) do (
            echo %%i | findstr /b "LLM_PROVIDER=" >nul
            if errorlevel 1 (
                echo %%i | findstr /b "OLLAMA_MODEL=" >nul
                if errorlevel 1 (
                    echo %%i
                ) else (
                    echo OLLAMA_MODEL=llama3.1
                )
            ) else (
                echo LLM_PROVIDER=ollama
            )
        )
    ) > agent-server\.env.tmp
    
    REM Check if LLM_PROVIDER was in the file
    findstr "LLM_PROVIDER" agent-server\.env.tmp >nul 2>&1
    if errorlevel 1 (
        echo. >> agent-server\.env.tmp
        echo # LLM Provider Configuration >> agent-server\.env.tmp
        echo LLM_PROVIDER=ollama >> agent-server\.env.tmp
        echo OLLAMA_BASE_URL=http://localhost:11434 >> agent-server\.env.tmp
        echo OLLAMA_MODEL=llama3.1 >> agent-server\.env.tmp
    )
    
    move /y agent-server\.env.tmp agent-server\.env >nul
    echo [OK] Configuration updated
) else (
    echo [WARNING] agent-server\.env not found. Creating from template...
    copy agent-server\.env.example agent-server\.env
    echo [OK] Created agent-server\.env
    echo.
    echo [WARNING] Please edit agent-server\.env and add your:
    echo    - LANGCHAIN_API_KEY (from LangSmith)
    echo.
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Make sure you have configured:
echo    - jira-tool-server\.env (Jira credentials)
echo    - agent-server\.env (LangSmith API key)
echo.
echo 2. Start the servers (in 3 separate terminals):
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
echo For detailed setup, see OLLAMA_SETUP.md
echo.
pause

