#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/SWE-Task-list"
APP_FILE="app.py"
VENV_DIR="$APP_DIR/venv"

cd "$APP_DIR"

# Pull latest code (rebase is risky in automation; use a clean sync)
git fetch --all
git reset --hard origin/master

# Ensure venv exists and is built with Python 3.11+
if [ ! -d "$VENV_DIR" ]; then
  if command -v python3.11 >/dev/null 2>&1; then
    python3.11 -m venv "$VENV_DIR"
  else
    echo "ERROR: venv missing and python3.11 not found. Install python3.11 or create venv manually." >&2
    exit 1
  fi
fi

PY="$VENV_DIR/bin/python"

# Install/update deps
"$PY" -m pip install -U pip
"$PY" -m pip install -r requirements.txt

# Stop previous process (if any) by matching the exact command
pkill -f "$PY $APP_FILE" || true

# Start new process
nohup "$PY" "$APP_FILE" > log.txt 2>&1 &

echo "Started. Tail logs with: tail -n 200 -f $APP_DIR/log.txt"