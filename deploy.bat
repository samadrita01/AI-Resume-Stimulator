@echo off
REM ────────────────────────────────────────────────────────────
REM AI Resume Analyzer - Docker Deployment Script
REM Platform: Windows
REM ────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  AI Resume Analyzer - Docker Deployment Script         ║
echo ║  Platform: Windows                                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check Docker installation
echo [1/4] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found. Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✓ Docker is installed
echo.

REM Check Docker Compose
echo [2/4] Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose not found. It should come with Docker Desktop.
    pause
    exit /b 1
)
echo ✓ Docker Compose is installed
echo.

REM Build Docker image
echo [3/4] Building Docker image...
docker-compose build
if errorlevel 1 (
    echo ✗ Failed to build Docker image
    pause
    exit /b 1
)
echo ✓ Docker image built successfully
echo.

REM Start containers
echo [4/4] Starting containers...
docker-compose up -d
if errorlevel 1 (
    echo ✗ Failed to start containers
    pause
    exit /b 1
)
echo ✓ Containers started successfully
echo.

echo ╔════════════════════════════════════════════════════════╗
echo ║  ✓ Deployment Complete!                               ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Access your application:
echo   http://localhost:8501
echo.
echo Useful commands:
echo   View logs:      docker-compose logs -f
echo   Stop:           docker-compose down
echo   Restart:        docker-compose restart
echo.
pause
