import os
import sys
from pyngrok import ngrok
from web import app

def run_with_public_url():
    port = 8000
    
    print("="*60)
    print("جاري إنشاء رابط خارجي للموقع...")
    
    try:
        # إنشاء النفق
        public_url = ngrok.connect(port).public_url
        print(f"\n🌍 رابط موقعك العام (انسخ هذا وأرسله للهاتف):")
        print(f"   {public_url}")
        print("\n" + "="*60)
    except Exception as e:
        print(f"\n❌ حدث خطأ أثناء إنشاء الرابط: {e}")
        print("تأكد من الاتصال بالإنترنت.")
        print("ملاحظة: قد تحتاج لتسجيل حساب مجاني في ngrok.com إذا طلب منك التوثيق.")
        print("="*60)

    # تشغيل التطبيق
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    run_with_public_url()