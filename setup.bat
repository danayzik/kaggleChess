@echo off

:: Check if Chocolatey is installed
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo Chocolatey not found, installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Unrestricted -Scope Process; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
)

:: Check for make
where make >nul 2>nul
if %errorlevel% neq 0 (
    echo make not found, installing make...
    choco install make -y
) else (
     echo make is already installed.
  )

:: Check for g++
where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo g++ not found, installing mingw...
    choco install mingw -y
) else (
    echo g++ is already installed.
)

:: Check for pip
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo pip not found, installing python (includes pip)...
    choco install python -y
) else (
    echo python and pip are already installed.
)


echo All necessary tools are installed.
pause
