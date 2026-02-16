# Fast Tunnel - Open Website Publicly
# No signup required!

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host " 🚀 فتح الموقع على الإنترنت (بدون تسجيل)" -ForegroundColor Green
Write-Host "======================================================================`n" -ForegroundColor Cyan

# Refresh PATH first
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Check local server
Write-Host "⏳ فحص السيرفر المحلي..." -ForegroundColor Yellow
try {
    $null = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ السيرفر شغال`n" -ForegroundColor Green
}
catch {
    Write-Host "❌ السيرفر مو شغال!" -ForegroundColor Red
    Write-Host "شغّل السيرفر أولاً: python web.py`n" -ForegroundColor Yellow
    Read-Host "اضغط Enter للخروج"
    exit
}

# Check Node
Write-Host "⏳ فحص Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Node.js $nodeVersion مثبت`n" -ForegroundColor Green
}
else {
    Write-Host "❌ Node.js غير مثبت`n" -ForegroundColor Red
    Read-Host "اضغط Enter للخروج"
    exit
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " ⏳ جاري إنشاء الرابط العام... انتظر 10-15 ثانية" -ForegroundColor Yellow
Write-Host "======================================================================`n" -ForegroundColor Cyan

# Start localtunnel
Write-Host "📡 تشغيل localtunnel...`n" -ForegroundColor Cyan

npx -y localtunnel --port 8000

Write-Host "`n`nانتهى." -ForegroundColor Cyan
