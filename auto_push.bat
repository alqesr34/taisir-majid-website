@echo off
REM Script to auto push to GitHub
REM اضغط على هذا الملف لرفع المشروع تلقائياً

setlocal enabledelayedexpansion

cd /d i:\web

echo.
echo ============================================================
echo          🚀 فتح المجلد ورفع المشروع
echo ============================================================
echo.

REM 1. فتح المجلد في ويندوز تلقائياً
echo [INFO] Opening folder...
start .

REM 2. تشغيل سكريبت الرفع (Python)
python init_github.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ حدث خطأ في تشغيل Python!
    echo اضغط أي زر للخروج...
    pause
    exit /b 1
)

pause
