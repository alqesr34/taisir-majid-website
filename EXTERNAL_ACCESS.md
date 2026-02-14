# الحصول على رابط خارجي لموقعك

## الخيار 1: استخدام Ngrok (الأبسط والأسرع)

**الخطوات:**

1. **انتقل إلى:** https://ngrok.com/download
   
2. **سجل حساب مجاني:** https://dashboard.ngrok.com/signup

3. **احصل على Auth Token:** 
   - بعد التسجيل، انسخ auth token من الموقع
   
4. **ثبت ngrok (اختياري - يمكن استخدام Python):**
   ```bash
   # في Terminal
   pip install pyngrok
   ```

5. **استخدم السكريبت التالي (python):**
   ```python
   from pyngrok import ngrok
   
   # ضع auth token هنا
   ngrok.set_auth_token("YOUR_AUTH_TOKEN_HERE")
   
   # أنشئ tunnel
   public_url = ngrok.connect(8000)
   print(f"External URL: {public_url}")
   
   # اترك الـ tunnel فتوح
   ngrok_process = ngrok.get_ngrok_process()
   ngrok_process.proc.wait()
   ```

---

## الخيار 2: استخدام Railway (بدون تكوين محلي)

**الوضع:**
- الموقع لا يزال يعطي 404 على Railway
- بحاجة لتحقيق أعمق من لوحة تحكم Railway

---

## الخيار 3: استخدام PythonAnywhere

**الخطوات:**

1. **انتقل إلى:** https://www.pythonanywhere.com/

2. **سجل حساب مجاني**

3. **رفع الملفات ونسخ البيانات**

4. **تشغيل التطبيق من صفحة الويب**

---

## الموقع المحلي: يعمل تماماً ✅

- **الرابط:** http://localhost:8000
- **عنوان الإدارة:** http://localhost:8000/login
- **بيانات الدخول:** muk / 12395

