@echo off
REM Script to auto push to GitHub
REM اضغط على هذا الملف لرفع المشروع تلقائياً

setlocal enabledelayedexpansion

cd /d i:\web

echo.
echo ============================================================
echo          🚀 رفع المشروع إلى GitHub تلقائياً
echo ============================================================
echo.

REM تشغيل PowerShell Script
powershell -ExecutionPolicy Bypass -File "auto_push.ps1"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ حدث خطأ!
    echo اضغط أي زر للخروج...
    pause
    exit /b 1
)

pause
