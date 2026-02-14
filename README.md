# موقع تجريبي لعضو مجلس محافظة بغداد — تيسير ماجد القيسي

محتوى المشروع: صفحة رئيسية عربية بسيطة مع نموذج اتصال ومكان لتحديث السيرة الذاتية والمبادرات.

تشغيل محلياً:

1. إنشاء بيئة افتراضية (اختياري):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. تثبيت المتطلبات:

```powershell
pip install -r requirements.txt
```

3. تشغيل التطبيق:

```powershell
python web.py
```

ثم افتح المتصفح على `http://localhost:8000`.

ملاحظات:
- استبدل النصوص النموذجية في `templates/index.html` بالمحتوى الصحيح.
- ضع الصور الحقيقية في `static/img/` بدلاً من `placeholder.jpg`.
- ملف الرسائل المستلمة يخزن في `messages.json` في مجلد المشروع.
