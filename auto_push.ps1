#!/usr/bin/env powershell
# Script to automatically push project to GitHub
# المتطلبات: Git يجب أن يكون مثبت

param(
    [string]$GitHubUsername = "alqesr34",
    [string]$RepoName = "taisir-majid-website",
    [string]$CommitMessage = "Initial commit: Add website project"
)

# الألوان
$colors = @{
    Success = "Green"
    Error = "Red"
    Info = "Cyan"
    Warning = "Yellow"
}

function Write-Pretty {
    param([string]$Message, [string]$Type = "Info")
    Write-Host $Message -ForegroundColor $colors[$Type]
}

# البداية
Clear-Host
Write-Pretty "╔════════════════════════════════════════════════════╗" "Info"
Write-Pretty "║         🚀 رفع المشروع إلى GitHub تلقائياً           ║" "Info"
Write-Pretty "╚════════════════════════════════════════════════════╝" "Info"
Write-Host ""

# 1. التحقق من Git
Write-Pretty "1️⃣  التحقق من Git..." "Info"
try {
    $gitVersion = git --version 2>&1
    Write-Pretty "   ✓ $gitVersion" "Success"
} catch {
    Write-Pretty "   ❌ Git غير مثبت!" "Error"
    Write-Pretty "   حمّل من: https://git-scm.com/download/win" "Warning"
    exit 1
}

Write-Host ""

# 2. الانتقال إلى مجلد المشروع
Write-Pretty "2️⃣  الانتقال إلى مجلد المشروع..." "Info"
$projectPath = "i:\web"
Set-Location $projectPath
Write-Pretty "   ✓ المجلد: $projectPath" "Success"

Write-Host ""

# 3. إعداد Git
Write-Pretty "3️⃣  إعداد بيانات Git..." "Info"
git config --global user.name "WebAdmin"
git config --global user.email "admin@taisirmajid.com"
Write-Pretty "   ✓ تم تعيين المستخدم" "Success"

Write-Host ""

# 4. التحقق من المستودع المحلي
Write-Pretty "4️⃣  التحقق من المستودع المحلي..." "Info"
if (-not (Test-Path ".git")) {
    git init
    Write-Pretty "   ✓ تم إنشاء مستودع جديد" "Success"
} else {
    Write-Pretty "   ✓ المستودع موجود بالفعل" "Success"
}

Write-Host ""

# 5. إضافة الملفات
Write-Pretty "5️⃣  جاري إضافة جميع الملفات..." "Info"
git add -A
$filesCount = (git diff --cached --name-only | Measure-Object).Count
Write-Pretty "   ✓ تمت إضافة $filesCount ملف" "Success"

Write-Host ""

# 6. الالتزام
Write-Pretty "6️⃣  جاري إنشاء التزام (Commit)..." "Info"
$commitOutput = git commit -m $CommitMessage 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Pretty "   ✓ تم الالتزام بنجاح" "Success"
} else {
    Write-Pretty "   ⓘ لا توجد تغييرات للالتزام" "Warning"
}

Write-Host ""

# 7. إضافة Remote
Write-Pretty "7️⃣  إضافة المستودع البعيد..." "Info"
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"

$existingRemote = git remote get-url origin 2>&1
if ($existingRemote -like "*$RepoName*") {
    Write-Pretty "   ✓ Remote موجود بالفعل" "Success"
} else {
    try {
        git remote remove origin 2>&1 | Out-Null
        git remote add origin $remoteUrl
        Write-Pretty "   ✓ Remote: $remoteUrl" "Success"
    } catch {
        Write-Pretty "   ❌ فشل إضافة Remote" "Error"
        exit 1
    }
}

Write-Host ""

# 8. إعادة تسمية الفرع
Write-Pretty "8️⃣  إعادة تسمية الفرع إلى main..." "Info"
try {
    git branch -M main 2>&1 | Out-Null
    Write-Pretty "   ✓ تم إعادة التسمية" "Success"
} catch {
    Write-Pretty "   ⓘ الفرع main موجود" "Warning"
}

Write-Host ""

# 9. الرفع
Write-Pretty "9️⃣  جاري رفع المشروع إلى GitHub..." "Info"
Write-Pretty "   ⚠️  قد تُطلب منك تسجيل دخول GitHub في المتصفح..." "Warning"
Write-Host ""

try {
    $pushOutput = git push -u origin main 2>&1
    $pushSuccess = $LASTEXITCODE -eq 0
    
    if ($pushSuccess) {
        Write-Pretty "   ✓ تم الرفع بنجاح!" "Success"
    } else {
        if ($pushOutput -like "*not found*") {
            Write-Pretty "   ❌ المستودع غير موجود على GitHub" "Error"
            Write-Pretty "" "Error"
            Write-Pretty "   💡 الحل:" "Warning"
            Write-Pretty "   1. اذهب إلى: https://github.com/new" "Warning"
            Write-Pretty "   2. اسم المستودع: $RepoName" "Warning"
            Write-Pretty "   3. اختر Public" "Warning"
            Write-Pretty "   4. لا تختر 'Initialize with README'" "Warning"
            Write-Pretty "   5. اضغط 'Create repository'" "Warning"
            Write-Pretty "   6. ثم أعد تشغيل هذا السكريبت" "Warning"
            exit 1
        } else {
            Write-Host $pushOutput
            Write-Pretty "   ⚠️  حدث خطأ في الرفع" "Error"
            exit 1
        }
    }
} catch {
    Write-Pretty "   ❌ خطأ: $_" "Error"
    exit 1
}

Write-Host ""

# النتيجة النهائية
Write-Pretty "═════════════════════════════════════════════════════" "Success"
Write-Pretty "✅ تم بنجاح!" "Success"
Write-Pretty "═════════════════════════════════════════════════════" "Success"

Write-Host ""
Write-Pretty "📍 معلومات المستودع:" "Info"
Write-Pretty "   👤 المستخدم: $GitHubUsername" "Success"
Write-Pretty "   📦 المستودع: $RepoName" "Success"
Write-Pretty "   🔗 الرابط: https://github.com/$GitHubUsername/$RepoName" "Success"

Write-Host ""
Write-Pretty "🚀 الخطوة التالية:" "Info"
Write-Pretty "   1. اذهب إلى: https://railway.app" "Success"
Write-Pretty "   2. اختر 'Deploy'" "Success"
Write-Pretty "   3. اختر 'Deploy from GitHub'" "Success"
Write-Pretty "   4. اختر المستودع: $GitHubUsername/$RepoName" "Success"
Write-Pretty "   5. سيتم النشر تلقائياً في 3-5 دقائق" "Success"

Write-Host ""
Write-Pretty "╔════════════════════════════════════════════════════╗" "Info"
Write-Pretty "║    الرابط النهائي سيكون مثل:                        ║" "Info"
Write-Pretty "║    https://$RepoName.up.railway.app" "Info"
Write-Pretty "╚════════════════════════════════════════════════════╝" "Info"

Write-Host ""
Write-Pretty "✨ شكراً لاستخدام هذا السكريبت!" "Success"
Write-Host ""

# فتح GitHub تلقائياً
Start-Sleep -Seconds 2
Write-Pretty "جاري فتح صفحة GitHub..." "Info"
Start-Process -FilePath "https://github.com/$GitHubUsername/$RepoName"
