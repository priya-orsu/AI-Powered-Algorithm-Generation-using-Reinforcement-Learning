@echo off
title Algoverse - Full Stack Launcher
echo ========================================================
echo   Starting AI Algorithm Generation Studio (Full Stack)
echo ========================================================
echo.

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "AlgoGen Backend (FastAPI)" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Vite Frontend on http://localhost:3000 ...
start "AlgoGen Frontend (Vite React)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Both servers are launching!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this launcher window...
pause >nul
