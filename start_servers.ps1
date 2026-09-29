Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting AI Algorithm Generation Studio (Full Stack)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "`n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$Root/backend'; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting Vite Frontend on http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$Root/frontend'; npm run dev"

Write-Host "`nBoth servers launched in dedicated PowerShell windows!" -ForegroundColor Green
Write-Host "Backend API docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend Studio:  http://localhost:3000" -ForegroundColor Cyan
