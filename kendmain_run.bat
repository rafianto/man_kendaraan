@echo off

title Manajemen Kendaraan Django Server
color 0A

:: Switch to project drive
I:
if errorlevel 1 (
    echo [ERROR] Drive I: not found.
    pause
    exit /b 1
)

:: Navigate to project root
cd /d "I:\Projects\appmaintenancekend"
if errorlevel 1 (
    echo [ERROR] Directory not found.
    pause
    exit /b 1
)

:: Activate virtual environment
if not exist "kndyenv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at sapi_env\Scripts\activate.bat
    pause
    exit /b 1
)
call "kndyenv\Scripts\activate.bat"

:: Navigate to Django project folder
cd /d "I:\Projects\appmantoko\appmaintenancekend"

:: Run Django development server
echo =====================================================
echo   Starting Manajemen Kendaraan Server on 0.0.0.0:8000
echo   Press CTRL+C to stop
echo =====================================================
echo.

call python manage.py runserver 0.0.0.0:8000

:: If server crashes, keep window open
echo.
echo [SERVER STOPPED]
pause
