Write-Host "Iniciando TrendZone AI OS (backend + frontend)..." -ForegroundColor Cyan

$root = $PSScriptRoot

Start-Process cmd.exe -ArgumentList '/c', "cd /d `"$root\backend`" && `"$root\.venv\Scripts\python.exe`" -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

Start-Sleep -Seconds 3

Start-Process cmd.exe -ArgumentList '/c', "cd /d `"$root\frontend`" && npm run dev"

Write-Host "Backend:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Frontend: http://127.0.0.1:5173" -ForegroundColor Green
Write-Host "Aguarde alguns segundos e abra o navegador." -ForegroundColor Yellow
