@echo off
echo Starting LangGraph Marketing Agent Full Stack Application
echo.

echo Starting Backend API Server...
start "Backend API" cmd /k "cd backend && python main.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend React App...
start "Frontend React" cmd /k "cd frontend && npm start"

echo.
echo =====================================================
echo  LangGraph Marketing Agent Started!
echo =====================================================
echo  Backend API: http://localhost:8000
echo  API Docs: http://localhost:8000/docs  
echo  Frontend: http://localhost:3000
echo  WebSocket: ws://localhost:8000/ws/[client_id]
echo =====================================================
echo.
echo Press any key to close all windows...
pause > nul

echo Stopping all services...
taskkill /f /im python.exe /t > nul 2>&1
taskkill /f /im node.exe /t > nul 2>&1
echo Services stopped.
