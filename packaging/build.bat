@echo off
echo === PullSplash Windows Build ===
echo.

cd /d "%~dp0\.."

pip install -r requirements.txt > nul 2>&1

echo Building PullSplash.exe ...
pyinstaller ^
    --distpath .\dist ^
    --workpath .\build ^
    --clean ^
    --noconfirm ^
    packaging\pullsplash.spec

echo.
echo Done! Output: dist\PullSplash.exe
echo Double-click dist\PullSplash.exe to launch.
echo.
pause
