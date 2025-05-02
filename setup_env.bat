@echo off
SETLOCAL

echo Checking for Chocolatey...

where choco >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
     "Set-ExecutionPolicy Bypass -Scope Process -Force; ^
      [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; ^
      iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
) ELSE (
    echo Chocolatey already installed.
)

echo Installing MinGW and Make...
choco install -y mingw make

echo Setup complete. You may need to restart your terminal or run `refreshenv`.
ENDLOCAL
pause
