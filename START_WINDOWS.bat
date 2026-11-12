@echo off
cd /d "%~dp0"
if not exist backend\.venv\Scripts\python.exe (
 echo Run SETUP_WINDOWS.bat first.
 pause
 exit /b 1
)
echo Portfolio: http://127.0.0.1:8000/
echo Admin:     http://127.0.0.1:8000/admin/
echo Keep this window open. Press Ctrl+C to stop.
backend\.venv\Scripts\python.exe backend\manage.py runserver 127.0.0.1:8000
pause
