@echo off
title Angelus Sentinel - Launcher
echo =========================================
echo       INICIANDO ANGELUS SENTINEL
echo =========================================
echo.

echo [1/2] Iniciando Backend (FastAPI - Puerto 8000)...
start "Angelus Backend" cmd /c "python -m uvicorn backend.main:app --reload --port 8000"

echo [2/2] Iniciando Frontend (Next.js - Puerto 3000)...
start "Angelus Frontend" cmd /c "cd frontend && npm run dev"

echo.
echo =========================================
echo  Servicios lanzados en ventanas separadas.
echo  - Backend estara en: http://localhost:8000
echo  - Frontend estara en: http://localhost:3000
echo =========================================
echo.
pause
