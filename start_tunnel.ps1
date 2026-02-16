# تشغيل النفق (Tunnel) لعرض الموقع خارجياً
# External Access via ngrok

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " شغل الموقع على الإنترنت - ngrok Tunnel" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if local server is running
Write-Host "Checking local server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ السيرفر المحلي شغال" -ForegroundColor Green
}
catch {
    Write-Host "✗ السيرفر المحلي مو شغال!" -ForegroundColor Red
    Write-Host "شغّل السيرفر أولاً بتشغيل: python web.py" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "اضغط Enter للخروج"
    exit
}

Write-Host ""
Write-Host "الآن جاري فتح النفق الخارجي..." -ForegroundColor Yellow
Write-Host ""

# Run Python script that uses pyngrok
C:/Users/eng/AppData/Local/Programs/Python/Python312/python.exe I:/web/external_access.py

Write-Host ""
Write-Host "انتهى." -ForegroundColor Cyan
Read-Host "اضغط Enter للخروج"
