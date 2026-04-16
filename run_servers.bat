@echo off
echo Starting Backend Server...
start "Backend" cmd /k "cd backend && uvicorn main:app --reload --port 8000"

echo Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo Both servers are starting. 
echo - Backend will be available at: http://localhost:8000
echo - Frontend will be available at: http://localhost:5173
echo.
echo ========================================================
echo Test Credentials:
echo Email: admin@shopsphere.com
echo Password: admin123
echo ========================================================
pause
