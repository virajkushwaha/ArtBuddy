# ArtBuddy Docker Startup Script
Write-Host "Starting ArtBuddy with Docker..." -ForegroundColor Green

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Please edit .env file and add your HuggingFace token (HF_TOKEN)" -ForegroundColor Red
    Write-Host "You can get a token from: https://huggingface.co/settings/tokens" -ForegroundColor Cyan
    Read-Host "Press Enter after updating the .env file to continue"
}

# Check if Docker is running
try {
    docker version | Out-Null
} catch {
    Write-Host "Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "Building and starting containers..." -ForegroundColor Yellow
docker-compose up --build

Write-Host ""
Write-Host "ArtBuddy containers are running!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan