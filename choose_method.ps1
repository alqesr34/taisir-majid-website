# ========================================================================
#  🚀 فتح الموقع على الإنترنت - الطريقة الأسهل
# ========================================================================

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host " 🌐 خيارات فتح الموقع على الإنترنت" -ForegroundColor Green
Write-Host "========================================================================`n" -ForegroundColor Cyan

# Check server
$result = $false
try {
    $null = Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    $result = $true
}
catch {
    Write-Host "❌ السيرفر المحلي مو شغال!" -ForegroundColor Red
    Write-Host "`nشغّل السيرفر أولاً: python web.py`n" -ForegroundColor Yellow
    Read-Host "اضغط Enter للخروج"
    exit
}

Write-Host "✅ السيرفر المحلي شغال`n" -ForegroundColor Green

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " اختر الطريقة:" -ForegroundColor Yellow
Write-Host "========================================================================`n" -ForegroundColor Cyan

Write-Host "1️⃣  ngrok (الأفضل - يحتاج تسجيل بسيط لمرة واحدة)" -ForegroundColor White
Write-Host "   ✓ سريع وموثوق" -ForegroundColor Gray
Write-Host "   ✓ رابط واضح" -ForegroundColor Gray
Write-Host "   ✗ يحتاج تسجيل مجاني (دقيقتين)" -ForegroundColor Gray
Write-Host ""

Write-Host "2️⃣  Ngrok بدون تسجيل (تجريبي - قد لا يعمل)" -ForegroundColor White
Write-Host "   ✓ بدون تسجيل" -ForegroundColor Gray
Write-Host "   ✗ قد يفشل أحياناً" -ForegroundColor Gray
Write-Host ""

Write-Host "3️⃣  نشر دائم على Railway/Render (موصى به للاستخدام الحقيقي)" -ForegroundColor White
Write-Host "   ✓ يبقى شغال 24/7" -ForegroundColor Gray
Write-Host "   ✓ رابط ثابت لا يتغير" -ForegroundColor Gray
Write-Host "   ✓ مجاني" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================================================`n" -ForegroundColor Cyan

$choice = Read-Host "اختر رقم (1، 2، أو 3)"

Write-Host ""

switch ($choice) {
    "1" {
        Write-Host "========================================================================" -ForegroundColor Cyan
        Write-Host " خطوات استخدام ngrok:" -ForegroundColor Yellow
        Write-Host "========================================================================`n" -ForegroundColor Cyan
        
        Write-Host "1️⃣  سجّل حساب مجاني:" -ForegroundColor White
        Write-Host "   https://dashboard.ngrok.com/signup`n" -ForegroundColor Cyan
        
        Write-Host "2️⃣  بعد التسجيل، انسخ التوكن من:" -ForegroundColor White
        Write-Host "   https://dashboard.ngrok.com/get-started/your-authtoken`n" -ForegroundColor Cyan
        
        Write-Host "3️⃣  شغّل هذا الأمر (استبدل YOUR_TOKEN بالتوكن):" -ForegroundColor White
        Write-Host "   ngrok config add-authtoken YOUR_TOKEN`n" -ForegroundColor Yellow
        
        Write-Host "4️⃣  بعدها شغّل:" -ForegroundColor White
        Write-Host "   python I:/web/start_external.py`n" -ForegroundColor Yellow
        
        Write-Host "========================================================================`n" -ForegroundColor Cyan
    }
    "2" {
        Write-Host "⚠️  هذه الطريقة تجريبية وقد لا تعمل دائماً`n" -ForegroundColor Yellow
        
        # Try to run ngrok without auth (will fail but show the error)
        Write-Host "جاري المحاولة...`n" -ForegroundColor Cyan
        
        python I:/web/start_external.py
    }
    "3" {
        Write-Host "========================================================================" -ForegroundColor Cyan
        Write-Host " نشر دائم - أفضل حل للاستخدام الحقيقي" -ForegroundColor Yellow
        Write-Host "========================================================================`n" -ForegroundColor Cyan
        
        Write-Host "المميزات:" -ForegroundColor White
        Write-Host "  ✅ الموقع يبقى شغال 24/7" -ForegroundColor Green
        Write-Host "  ✅ رابط ثابت لا يتغير" -ForegroundColor Green
        Write-Host "  ✅ مجاني تماماً" -ForegroundColor Green
        Write-Host "  ✅ سريع جداً`n" -ForegroundColor Green
        
        Write-Host "أخبرني إذا تريد المساعدة في النشر (سأرشدك خطوة بخطوة)`n" -ForegroundColor Cyan
        
        Write-Host "========================================================================`n" -ForegroundColor Cyan
    }
    default {
        Write-Host "❌ خيار غير صحيح`n" -ForegroundColor Red
    }
}

Read-Host "`nاضغط Enter للخروج"
