Write-Host "Stopping all processes..." -ForegroundColor Red
taskkill /f /im python.exe 2>$null
taskkill /f /im node.exe 2>$null

Start-Sleep -Seconds 2

Write-Host "Starting backend on port 8001..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "cd /d `"$PSScriptRoot\backend`" && python working_app.py"

Start-Sleep -Seconds 5

Write-Host "Testing backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/test" -UseBasicParsing
    Write-Host "Backend test: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "Backend test: FAILED" -ForegroundColor Red
}

Write-Host "Starting frontend..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "cd /d `"$PSScriptRoot\frontend`" && npm start"

Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8001/test" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White