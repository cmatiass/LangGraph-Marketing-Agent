# Start LangGraph Marketing Agent Full Stack
Write-Host "Starting LangGraph Marketing Agent Full Stack Application" -ForegroundColor Green
Write-Host ""

Write-Host "Starting Backend API Server..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\charly\Desktop\Project Langgraph\backend'; python main.py"

Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Starting Frontend React App..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\charly\Desktop\Project Langgraph\frontend'; npm start"

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host " LangGraph Marketing Agent Started!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host " Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host " API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host " Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host " WebSocket: ws://localhost:8000/ws/[client_id]" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Both services are starting in separate windows." -ForegroundColor White
Write-Host "The React app will automatically open in your browser." -ForegroundColor White
