#!/usr/bin/env python3
"""
Fix ngrok connection - Restart server and ngrok properly
"""

import sys
import time
import subprocess
import os
import signal

def kill_port(port):
    """Kill any process using the specified port"""
    print(f"Checking port {port}...")
    try:
        # Get process using port
        result = subprocess.run(
            ['netstat', '-ano', '|', 'findstr', f':{port}'],
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    print(f"Killing process {pid} on port {port}...")
                    subprocess.run(['taskkill', '/F', '/PID', pid], 
                                 capture_output=True)
                    time.sleep(1)
    except Exception as e:
        print(f"Error checking port: {e}")

def check_server():
    """Check if server is running"""
    try:
        import requests
        resp = requests.get("http://localhost:8000/", timeout=5)
        return resp.status_code == 200
    except:
        return False

def start_server():
    """Start Flask server"""
    print("\nStarting Flask server...")
    python_exe = sys.executable
    web_file = os.path.join(os.path.dirname(__file__), 'web.py')
    
    process = subprocess.Popen(
        [python_exe, web_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for server to start
    print("Waiting for server to start...")
    for i in range(10):
        time.sleep(1)
        if check_server():
            print("✅ Server started successfully!\n")
            return process
        print(f"  Checking... ({i+1}/10)")
    
    print("❌ Server failed to start\n")
    return None

def start_ngrok():
    """Start ngrok tunnel"""
    print("Starting ngrok tunnel...")
    print("="*70)
    
    try:
        from pyngrok import ngrok
        
        # Kill any existing tunnels
        ngrok.kill()
        time.sleep(1)
        
        # Start tunnel
        public_url = ngrok.connect(8000, bind_tls=True)
        
        print("\n" + "="*70)
        print("✅ نجح! الموقع متاح الآن على الإنترنت")
        print("="*70)
        print(f"\n🔗 الرابط العام:")
        print(f"   {public_url}")
        print(f"\n🔗 لوحة التحكم:")
        print(f"   {public_url}/login")
        print(f"\n📱 شارك هذا الرابط - يعمل على الموبايل والكمبيوتر")
        print("\n" + "="*70)
        print("\n💡 اضغط Ctrl+C لإيقاف النفق")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ خطأ: {error_msg}\n")
        
        if "authtoken" in error_msg.lower() or "authenticate" in error_msg.lower():
            print("="*70)
            print("⚠️  تحتاج تسجيل في ngrok")
            print("="*70)
            print("\nالخطوات:")
            print("1. https://dashboard.ngrok.com/signup (سجّل)")
            print("2. https://dashboard.ngrok.com/get-started/your-authtoken (انسخ التوكن)")
            print("3. شغّل: ngrok config add-authtoken YOUR_TOKEN")
            print("4. أعد تشغيل هذا السكريبت")
            print("="*70 + "\n")
        
        return False

def main():
    """Main function"""
    
    print("\n" + "="*70)
    print(" 🚀 فتح الموقع على الإنترنت")
    print("="*70 + "\n")
    
    # Check if server is already running
    if check_server():
        print("✅ السيرفر يعمل بالفعل\n")
    else:
        print("⚠️  السيرفر غير شغال")
        
        # Kill any process on port 8000
        kill_port(8000)
        
        # Start server
        server_process = start_server()
        if not server_process:
            print("فشل تشغيل السيرفر. جرب يدوياً: python web.py")
            return 1
    
    # Start ngrok
    if not start_ngrok():
        return 1
    
    # Keep running
    try:
        print("النفق شغال... (لا تغلق هذه النافذة)\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  إيقاف...")
        try:
            from pyngrok import ngrok
            ngrok.kill()
        except:
            pass
        print("تم.\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
