# 📋 خطوات رفع المشروع على GitHub بالتفصيل

تم إعداد المشروع! الآن تابع الخطوات التالية:

---

## 🔧 المُتطلبات

1. **حساب GitHub**: https://github.com/signup
2. **Git**: https://git-scm.com/download/win

---

## ⚡ الطريقة السريعة (الأسهل)

### إذا كنت على Windows:

**الخطوة 1: فتح PowerShell**
- افتح VS Code Terminal
- تأكد أنك في مجلد `i:\web`

**الخطوة 2: تشغيل السكريبت**
```powershell
powershell -ExecutionPolicy Bypass -File setup_github.ps1
```

ثم أدخل:
- اسم المستخدم GitHub
- اسم المستودع (مثلاً: `taisir-majid-website`)

**ننتظره ينتهي... ✅**

---

## 📝 الطريقة اليدوية (خطوة بخطوة)

إذا لم ينجح السكريبت، اتبع هذا يدويًا:

### 1. تثبيت Git (إذا لم يكن مثبت)
```powershell
winget install Git.Git
```

بعد التثبيت، أعد تشغيل Terminal الجديد.

### 2. إعداد Git
```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@github.com"
```

### 3. إنشاء مستودع على GitHub
1. اذهب إلى: https://github.com/new
2. اسم المستودع: `taisir-majid-website`
3. اختر Public
4. ❌ **لا تختر** "Initialize with README"
5. اضغط "Create repository"

### 4. رفع المشروع
```powershell
cd i:\web

git init

git add .

git commit -m "Initial commit: Add website project"

git remote add origin https://github.com/YOUR_USERNAME/taisir-majid-website.git

git branch -M main

git push -u origin main
```

عند الطلب، أدخل:
- **Username**: اسم مستخدمك GitHub
- **Password**: استخدم GitHub Personal Access Token
  - اذهب إلى: https://github.com/settings/tokens/new
  - اختر scopes: `repo`, `workflow`
  - انسخ الـ Token والصقه

---

## ✅ التحقق

بعد انتهاء رفع المشروع:

1. اذهب إلى: `https://github.com/YOUR_USERNAME/taisir-majid-website`
2. تأكد من وجود جميع الملفات ✅

---

## 🚀 الخطوة التالية: النشر على Railway

### اتبع هذه الخطوات:

1. **اذهب إلى**: https://railway.app
2. **اضغط**: "Deploy"
3. **اختر**: "Deploy from GitHub"
4. **اختر**: المستودع الجديد من القائمة
5. **انتظر**: 3-5 دقائق
6. **احصل على الرابط**: مثل `https://taisir-majid-website.up.railway.app`

---

## 📌 الملفات المهمة

| الملف | الوصف |
|------|-------|
| `web.py` | التطبيق الرئيسي |
| `requirements.txt` | المتطلبات |
| `Procfile` | إعدادات النشر |
| `.gitignore` | الملفات المستثناة من Git |
| `README_AR.md` | شرح المشروع بالعربية |
| `DEPLOYMENT.md` | شرح النشر السحابي |
| `GITHUB_GUIDE_AR.md` | شرح تفصيلي لـ GitHub |

---

## ⚠️ نصائح أمان

قبل الرفع:

1. ✅ تغيير `ADMIN_USER` و `ADMIN_PASS` في `web.py`
2. ✅ إضافة `.env` للمتغيرات الحساسة
3. ✅ استخدام Private الخزن بدل Public (اختياري)
4. ✅ تحديث الـ `SECRET_KEY`

---

## 🆘 حل المشاكل

### المشكلة: "git: command not found"
**الحل**: أعد تشغيل Terminal بعد تثبيت Git

### المشكلة: "remote already exists"
**الحل**:
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/taisir-majid-website.git
```

### المشكلة: "failed to authenticate"
**الحل**: استخدم GitHub Token من: https://github.com/settings/tokens

### المشكلة: الملفات الكبيرة جداً
**الحل**: أضفها إلى `.gitignore`

---

## 📞 التواصل عند الحاجة

- البريد الإلكتروني: taisirmajidnajm@gmail.com
- الهاتف: 07838961231

---

**تم! الآن المشروع متاح للجميع على الإنترنت! 🎉**

---

## 🔗 الروابط المهمة

- GitHub: https://github.com
- Railway: https://railway.app
- Render: https://render.com
- Git Download: https://git-scm.com

