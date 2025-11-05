# Quick Start ArtBuddy with minimal setup
Write-Host "Quick Starting ArtBuddy..." -ForegroundColor Green

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
HF_TOKEN=your_huggingface_token_here
SECRET_KEY=dev-secret-key
"@ | Out-File -FilePath ".env" -Encoding UTF8
}

# Start simple backend
Write-Host "Starting simple backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; pip install fastapi uvicorn python-dotenv; python simple_main.py"

# Start frontend
Write-Host "Starting frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm start"

Write-Host ""
Write-Host "Quick start initiated!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan