@echo off

:: Check if Chocolatey is installed
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo Chocolatey not found, installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Unrestricted -Scope Process; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
)

:: Install make, g++, python, and pip if not installed
for %%i in (make g++ python pip) do (
    where %%i >nul 2>nul
    if %errorlevel% neq 0 (
        echo Installing %%i...
        choco install %%i -y
    ) else (
        echo %%i is already installed.
    )
)

echo All necessary tools are installed.
pause
