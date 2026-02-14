# Script to initialize and push project to GitHub
# Make sure Git is installed before running this
# Run with: powershell -ExecutionPolicy Bypass -File setup_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   GitHub Repository Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# قراءة البيانات من المستخدم
$github_username = Read-Host "اكتب اسم المستخدم GitHub الخاص بك"
$repo_name = Read-Host "اكتب اسم المستودع (مثال: taisir-majid-website)"

# التحقق من Git
Write-Host ""
Write-Host "جاري التحقق من Git..." -ForegroundColor Yellow
git --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git غير مثبت! يرجى تثبيت Git من: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "الخطوة 1: إنشاء مستودع Git محلي" -ForegroundColor Green
git init

Write-Host ""
Write-Host "الخطوة 2: إضافة جميع الملفات" -ForegroundColor Green
git add .

Write-Host ""
Write-Host "الخطوة 3: إنشاء التزام أول" -ForegroundColor Green
git commit -m "Initial commit: Add website project"

Write-Host ""
Write-Host "الخطوة 4: إضافة المستودع البعيد" -ForegroundColor Green
git remote add origin "https://github.com/$github_username/$repo_name.git"

Write-Host ""
Write-Host "الخطوة 5: إعادة تسمية الفرع إلى main" -ForegroundColor Green
git branch -M main

Write-Host ""
Write-Host "الخطوة 6: رفع المشروع إلى GitHub" -ForegroundColor Green
Write-Host "⚠️  قد تُطلب منك إدخال بيانات اعتمادك..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ تم بنجاح! المشروع الآن على GitHub" -ForegroundColor Green
Write-Host "رابط المستودع: https://github.com/$github_username/$repo_name" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "الخطوة التالية:" -ForegroundColor Yellow
Write-Host "1. اذهب إلى: https://railway.app" -ForegroundColor White
Write-Host "2. اختر 'Deploy from GitHub'" -ForegroundColor White
Write-Host "3. اختر هذا المستودع وسيتم النشر تلقائياً" -ForegroundColor White
