@echo off
cd /d "%~dp0"
echo ================================================
echo  Jigsaw Assets Builder
echo ================================================
echo.

echo [1/3] Generating thumbs + manifest...
python tools/build.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: build failed. Check Python is installed.
    pause
    exit /b 1
)

echo.
echo [2/3] Git add + commit...
git add .
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set dt=%%I
set timestamp=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%
git commit -m "assets: update %timestamp%"

echo.
echo [3/3] Git push...
git push

echo.
echo ================================================
echo  Done!
echo ================================================
pause
