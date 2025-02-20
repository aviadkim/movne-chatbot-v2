# Movne Chatbot System Diagnostic Script
Write-Host "=== Movne Chatbot System Test ===" -ForegroundColor Cyan

# Test 1: Verify Project Structure
Write-Host "`nTest 1: Checking Project Structure" -ForegroundColor Yellow
$requiredDirs = @(".github", "backend", "frontend", "scripts")
$requiredFiles = @(".env", "docker-compose.yml", "railway.toml", "backend/app/main.py", "frontend/package.json")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) { Write-Host "  ✓ $dir exists" -ForegroundColor Green } 
    else { Write-Host "  ✗ $dir missing" -ForegroundColor Red }
}
foreach ($file in $requiredFiles) {
    if (Test-Path $file) { Write-Host "  ✓ $file exists" -ForegroundColor Green } 
    else { Write-Host "  ✗ $file missing" -ForegroundColor Red }
}

# Test 2: Check .env File
Write-Host "`nTest 2: Checking .env" -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    if ($envContent -match "OPENAI_API_KEY=.+") { Write-Host "  ✓ OPENAI_API_KEY set" -ForegroundColor Green }
    else { Write-Host "  ✗ OPENAI_API_KEY missing or empty" -ForegroundColor Red }
} else { Write-Host "  ✗ .env file not found" -ForegroundColor Red }

# Test 3: Verify Docker Installation
Write-Host "`nTest 3: Docker Check" -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  ✓ Docker installed: $dockerVersion" -ForegroundColor Green
    $composeVersion = docker compose version
    Write-Host "  ✓ Docker Compose installed: $composeVersion" -ForegroundColor Green
} catch { Write-Host "  ✗ Docker or Compose not installed" -ForegroundColor Red }

# Test 4: Check Frontend Build
Write-Host "`nTest 4: Frontend Build Check" -ForegroundColor Yellow
if (Test-Path "frontend/build") { Write-Host "  ✓ Build folder exists" -ForegroundColor Green }
else { 
    Write-Host "  ✗ Build folder missing. Run 'npm run build' in frontend/" -ForegroundColor Red
    Write-Host "    Suggestion: Update package.json 'build' to 'react-scripts build'" -ForegroundColor Magenta
}

# Test 5: Start Docker and Test API
Write-Host "`nTest 5: Docker and API Test" -ForegroundColor Yellow
try {
    Write-Host "  Starting Docker Compose..." -ForegroundColor Cyan
    docker compose up --build -d  # Run in detached mode
    Start-Sleep -Seconds 10  # Wait for startup
    Write-Host "  Testing /health endpoint..." -ForegroundColor Cyan
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "  ✓ Health: $health.status" -ForegroundColor Green

    Write-Host "  Testing /api/v1/chat (Hebrew)..." -ForegroundColor Cyan
    $heBody = @{message="שלום";language="he"} | ConvertTo-Json -Compress
    $heResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Body $heBody -ContentType "application/json"
    Write-Host "  ✓ Hebrew Response: $($heResponse.response)" -ForegroundColor Green

    Write-Host "  Testing /api/v1/chat (English)..." -ForegroundColor Cyan
    $enBody = @{message="Hello";language="en"} | ConvertTo-Json -Compress
    $enResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Body $enBody -ContentType "application/json"
    Write-Host "  ✓ English Response: $($enResponse.response)" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error: $_" -ForegroundColor Red
    if ($_.Exception.Message -match "405") { Write-Host "    Check: Is /api/v1/chat a POST endpoint in main.py?" -ForegroundColor Magenta }
    if ($_.Exception.Message -match "connection") { Write-Host "    Check: Is Docker running?" -ForegroundColor Magenta }
} finally {
    Write-Host "  Stopping Docker Compose..." -ForegroundColor Cyan
    docker compose down
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan