# Start Working ArtBuddy
Write-Host "Starting ArtBuddy (Working Version)..." -ForegroundColor Green

# Create .env
if (-not (Test-Path ".env")) {
    @"
HF_TOKEN=your_huggingface_token_here
SECRET_KEY=dev-secret-key
"@ | Out-File -FilePath ".env" -Encoding UTF8
}

# Start Flask backend
Write-Host "Starting Flask backend on port 8001..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; pip install flask flask-cors python-dotenv; python flask_app.py"

Start-Sleep -Seconds 3

# Start new frontend
Write-Host "Starting React frontend on port 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm start"

Write-Host ""
Write-Host "ArtBuddy Working Version Started!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8001" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Click 'Test Backend Connection' to verify everything works!" -ForegroundColor White