#!/bin/bash
echo
echo " ================================================"
echo "  OnboardAI demo"
echo "  Keep this window open while you use the app."
echo "  Close it (or press Ctrl+C) to stop OnboardAI."
echo " ================================================"
echo
cd "$(dirname "$0")/backend" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python is not installed. Install Python 3.12 from https://www.python.org/downloads/"
  read -r -p "Press Enter to close."
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "First-time setup. This takes a minute or two..."
  python3 -m venv .venv || { read -r -p "Could not create the Python environment. Press Enter to close."; exit 1; }
fi

echo "Checking required libraries..."
.venv/bin/python -m pip install -q -r requirements.txt || {
  read -r -p "Could not install the required libraries. Check your internet connection. Press Enter to close."
  exit 1
}

echo "Starting OnboardAI. Your browser will open in a few seconds..."
(sleep 4; open http://localhost:8000) &
.venv/bin/python -m uvicorn app.main:app --port 8000
