@echo off
title OnboardAI
echo.
echo  ================================================
echo   OnboardAI demo
echo   Keep this window open while you use the app.
echo   Close it (or press Ctrl+C) to stop OnboardAI.
echo  ================================================
echo.
cd /d "%~dp0backend"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo Python is not installed.
  echo Install Python 3.12 from https://www.python.org/downloads/
  echo and check "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo First-time setup. This takes a minute or two...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo Could not create the Python environment.
    pause
    exit /b 1
  )
)

echo Checking required libraries...
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo Could not install the required libraries. Check your internet connection and try again.
  pause
  exit /b 1
)

echo Starting OnboardAI. Your browser will open in a few seconds...
start "" cmd /c "timeout /t 4 >nul & start http://localhost:8000"
".venv\Scripts\python.exe" -m uvicorn app.main:app --port 8000
pause
