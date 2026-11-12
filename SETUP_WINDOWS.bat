@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
 echo Install Python 3.12 with the Python launcher, then run this file again.
 pause
 exit /b 1
)
where npm >nul 2>nul
if errorlevel 1 (
 echo Install Node.js 22 LTS, reopen the terminal, then run this file again.
 pause
 exit /b 1
)
if not exist backend\.venv\Scripts\python.exe py -3.12 -m venv backend\.venv
if errorlevel 1 goto fail
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements-lock.txt
if errorlevel 1 goto fail
if not exist backend\.env copy backend\.env.example backend\.env >nul
call npm ci --prefix frontend
if errorlevel 1 goto fail
call npm run build --prefix frontend
if errorlevel 1 goto fail
backend\.venv\Scripts\python.exe backend\manage.py migrate
if errorlevel 1 goto fail
backend\.venv\Scripts\python.exe backend\manage.py seed_projects
if errorlevel 1 goto fail
backend\.venv\Scripts\python.exe backend\manage.py collectstatic --noinput
if errorlevel 1 goto fail
echo.
echo Create your private admin account. If it already exists, press Ctrl+C and skip this step.
backend\.venv\Scripts\python.exe backend\manage.py createsuperuser
echo.
echo Setup complete. Run START_WINDOWS.bat next.
pause
exit /b 0
:fail
echo Setup failed. Read the error above, fix it, and rerun setup.
pause
exit /b 1
