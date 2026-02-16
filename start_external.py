#!/usr/bin/env python3
"""
External Tunnel - Simple ngrok launcher for Taisir Majid website
Creates a public URL that works on all networks and mobile devices
"""

import sys
import time
import subprocess

def check_local_server():
    """Check if Flask server is running on localhost:8000"""
    try:
        import requests
        resp = requests.get("http://localhost:8000/", timeout=5)
        return resp.status_code == 200
    except:
        return False

def start_ngrok():
    """Start ngrok tunnel pointing to localhost:8000"""
    print("\n" + "="*70)
    print("🚀 جاري فتح النفق الخارجي (ngrok)...")
    print("="*70 + "\n")
    
    try:
        from pyngrok import ngrok, conf
        
        # Kill any existing tunnels
        ngrok.kill()
        
        # Start a new tunnel
        print("⏳ إنشاء الرابط العام...")
        public_url = ngrok.connect(8000, bind_tls=True)
        
        print("\n" + "="*70)
        print("✅ تم إنشاء الرابط بنجاح!")
        print("="*70)
        print(f"\n🔗 الرابط العام (يعمل على جميع الشبكات والموبايلات):")
        print(f"\n   {public_url}")
        print(f"\n🔗 لوحة التحكم:")
        print(f"   {public_url}/login")
        print("\n" + "="*70)
        print("\n💡 ملاحظة:")
        print("   - هذا الرابط مؤقت ويعمل طالما هذه النافذة مفتوحة")
        print("   - اضغط Ctrl+C لإيقاف النفق")
        print("="*70 + "\n")
        
        # Keep running
        try:
            print("النفق شغال... لا تغلق هذه النافذة.\n")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️ إيقاف النفق...")
            ngrok.kill()
            print("انتهى.\n")
            
    except ImportError:
        print("\n❌ خطأ: pyngrok غير مثبت!")
        print("\nحل المشكلة:")
        print("   pip install pyngrok\n")
        return False
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ خطأ: {error_msg}\n")
        
        if "authtoken" in error_msg.lower() or "authenticate" in error_msg.lower():
            print("="*70)
            print("⚠️  تحتاج إلى تسجيل في ngrok (مجاني)")
            print("="*70)
            print("\nالخطوات:")
            print("1. اذهب إلى: https://dashboard.ngrok.com/signup")
            print("2. سجل حساب مجاني")
            print("3. انسخ الـ authtoken من: https://dashboard.ngrok.com/get-started/your-authtoken")
            print("4. شغّل الأمر التالي في Terminal:")
            print("\n   ngrok config add-authtoken YOUR_TOKEN_HERE\n")
            print("="*70 + "\n")
        
        return False
    
    return True

def main():
    """Main function"""
    
    # Check local server first
    if not check_local_server():
        print("\n" + "="*70)
        print("⚠️  السيرفر المحلي مو شغال!")
        print("="*70)
        print("\nشغّل السيرفر أولاً:")
        print("   python web.py")
        print("\nثم شغّل هذا السكريبت مرة ثانية.")
        print("="*70 + "\n")
        return 1
    
    print("\n✅ السيرفر المحلي شغال على localhost:8000")
    
    # Start ngrok
    if not start_ngrok():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
