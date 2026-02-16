import os
import sys
import importlib.util
from pyngrok import ngrok

def install_package(package):
    """Install package if not present"""
    print(f"Installing {package}...")
    try:
        os.system(f"{sys.executable} -m pip install {package}")
    except Exception as e:
        print(f"Error installing {package}: {e}")

def get_app():
    """Load the Flask app from 9555555.py dynamically"""
    try:
        # Since the filename starts with a number, we must use importlib
        spec = importlib.util.spec_from_file_location("web_app", "9555555.py")
        if spec is None:
            print("Error: Could not find 9555555.py")
            return None
        web_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(web_app)
        return web_app.app
    except Exception as e:
        print(f"Error loading application: {e}")
        return None

def run_sharing():
    # Install pyngrok if not present
    try:
        import pyngrok
    except ImportError:
        install_package("pyngrok")
        import pyngrok

    app = get_app()
    if not app:
        return

    port = 8000
    
    print("\n" + "="*60)
    print("🚀 جاري إعداد الرابط الخارجي... يرجى الانتظار")
    
    try:
        # Create tunnel to port 8000
        # Check if port 8000 is open (app running) or closed (need to run app)
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        is_port_open = (result == 0)
        sock.close()

        public_url = ngrok.connect(port).public_url
        
        print("\n✅ تم إنشاء الرابط بنجاح!")
        print(f"\n🔗 رابط موقعك (يعمل على جميع الشبكات والهواتف):")
        print(f"   {public_url}")
        print("\n💡 ملاحظة: هذا الرابط مؤقت وسيعمل طالما هذه النافذة مفتوحة.")
        print("="*60 + "\n")
        
        if not is_port_open:
            print("جاري تشغيل الموقع...")
            app.run(port=port)
        else:
            print("الموقع يعمل بالفعل في الخلفية. الرابط جاهز!")
            # Keep script running to keep tunnel open
            import time
            while True:
                time.sleep(1)
        
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        print("تأكد من إنشاء حساب مجاني في ngrok.com وتشغيل الأمر:")
        print("ngrok config add-authtoken <your-token>")
        print("="*60)

if __name__ == '__main__':
    run_sharing()
