@echo off
REM Script to initialize and push project to GitHub
REM Make sure Git is installed before running this

setlocal enabledelayedexpansion

echo.
echo ========================================
echo GitHub Repository Setup Script
echo ========================================
echo.

REM Replace with your actual values
set "REPO_NAME=taisir-majid-website"
set "GITHUB_USERNAME=YOUR_USERNAME"
set "COMMIT_MSG=Initial commit: Add website project"

echo Step 1: Initialize Git repository
git init

echo.
echo Step 2: Add all files
git add .

echo.
echo Step 3: Create initial commit
git commit -m "%COMMIT_MSG%"

echo.
echo Step 4: Set remote repository
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo.
echo Step 5: Rename branch to main
git branch -M main

echo.
echo Step 6: Push to GitHub
git push -u origin main

echo.
echo ========================================
echo Done! Your project is now on GitHub
echo Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo ========================================
echo.

pause
