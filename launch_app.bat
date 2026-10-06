@echo off
title AlgoGen Studio Desktop App Launcher
echo Starting AlgoGen Studio AI Engine...

:: 1. Start FastAPI Backend Server on Port 8000
start /B python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > NUL 2>&1

:: 2. Start Frontend Dev Server on Port 3000
cd frontend
start /B npm run dev > NUL 2>&1
cd ..

:: Wait 3 seconds for servers to initialize
timeout /t 3 /nobreak > NUL

:: 3. Open Standalone Native App Window in Chrome or Edge
start "" "msedge" --app=http://localhost:3000 || start "" "chrome" --app=http://localhost:3000 || start http://localhost:3000

echo AlgoGen Studio launched successfully!
