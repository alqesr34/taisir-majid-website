@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo       GitHub Setup & Upload Assistant
echo ========================================================
echo.

:: Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b
)

:: Initialize Git if not already
if not exist .git (
    echo [INFO] Initializing new Git repository...
    git init
    git branch -M main
) else (
    echo [INFO] Git repository already exists.
)

:: Add all files
echo [INFO] Adding files...
git add .

:: Commit
echo [INFO] Committing changes...
git commit -m "Auto update for hosting"

:: Check for remote 'origin'
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ACTION REQUIRED]
    echo Please create a new repository on GitHub: https://github.com/new
    echo copy the HTTPS URL (e.g., https://github.com/username/repo.git)
    echo.
    set /p REPO_URL="Paste Repository URL here: "
    git remote add origin !REPO_URL!
) else (
    echo [INFO] Remote 'origin' already exists.
)

:: Push
echo [INFO] Pushing to GitHub...
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Push failed.
    echo Possible reasons:
    echo 1. You need to sign in (a browser window might have opened).
    echo 2. The repository URL is incorrect.
    echo 3. There are conflicts (force push might be needed).
    echo.
    set /p FORCE="Do you want to FORCE push (overwrite remote)? (y/n): "
    if /i "!FORCE!"=="y" (
        git push -f origin main
    )
)

echo.
echo ========================================================
echo       Done! Your code is on GitHub.
echo ========================================================
pause
