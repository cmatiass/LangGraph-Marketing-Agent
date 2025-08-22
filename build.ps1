# Build script para compilar el frontend React y copiarlo al backend (Windows)

Write-Host "🏗️  Building React Frontend for Production..." -ForegroundColor Green

# Navigate to frontend directory
Set-Location frontend

# Install dependencies if needed
if (!(Test-Path "node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
}

# Build React app
Write-Host "⚛️  Building React app..." -ForegroundColor Blue
npm run build

# Check if build succeeded
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend build successful!" -ForegroundColor Green
    
    # Create backend static directory if it doesn't exist
    New-Item -ItemType Directory -Force -Path "..\backend\static" | Out-Null
    
    # Copy build files to backend static directory
    Write-Host "📁 Copying build files to backend..." -ForegroundColor Yellow
    Copy-Item -Path "build\*" -Destination "..\backend\static" -Recurse -Force
    
    Write-Host "🎉 Frontend successfully built and copied to backend!" -ForegroundColor Green
    Write-Host "📂 Files copied to: backend\static\" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Now you can run the backend with:" -ForegroundColor White
    Write-Host "cd backend && python main.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The app will be available at: http://localhost:8000" -ForegroundColor Magenta
} else {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    exit 1
}

# Return to original directory
Set-Location ..
