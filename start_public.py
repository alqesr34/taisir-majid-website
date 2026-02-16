#!/usr/bin/env python3
"""
Alternative External Access - Using localtunnel (no signup required)
Simple public URL without authentication
"""

import sys
import time
import subprocess
import os

def check_local_server():
    """Check if Flask server is running on localhost:8000"""
    try:
        import requests
        resp = requests.get("http://localhost:8000/", timeout=5)
        return resp.status_code == 200
    except:
        return False

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def check_npx():
    """Check if npx is available"""
    try:
        result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def start_localtunnel():
    """Start localtunnel - no signup required!"""
    print("\n" + "="*70)
    print("🚀 جاري فتح النفق الخارجي (بدون تسجيل)...")
    print("="*70 + "\n")
    
    if not check_node():
        print("❌ Node.js غير مثبت!")
        print("\nحمّل وثبّت Node.js من:")
        print("   https://nodejs.org/")
        print("\nثم شغّل هذا السكريبت مرة ثانية.")
        return False
    
    if not check_npx():
        print("❌ npx غير متوفر!")
        return False
    
    print("⏳ إنشاء الرابط العام (قد يستغرق بضع ثواني)...\n")
    
    try:
        # Run localtunnel using npx (automatically downloads if needed)
        # This doesn't require signup!
        process = subprocess.Popen(
            ['npx', '-y', 'localtunnel', '--port', '8000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        url_found = False
        for line in process.stdout:
            print(line.strip())
            if 'your url is:' in line.lower():
                url = line.split('your url is:')[1].strip()
                url_found = True
                print("\n" + "="*70)
                print("✅ تم إنشاء الرابط بنجاح!")
                print("="*70)
                print(f"\n🔗 الرابط العام (يعمل على جميع الشبكات والموبايلات):")
                print(f"\n   {url}")
                print(f"\n🔗 لوحة التحكم:")
                print(f"   {url}/login")
                print("\n" + "="*70)
                print("\n💡 ملاحظات:")
                print("   - هذا الرابط مؤقت ويعمل طالما هذه النافذة مفتوحة")
                print("   - أول مرة تزور الرابط، قد تظهر صفحة تأكيد - اضغط Continue")
                print("   - اضغط Ctrl+C لإيقاف النفق")
                print("="*70 + "\n")
                break
        
        if not url_found:
            print("\n⚠️ لم يتم العثور على الرابط في النتائج.")
            print("لكن localtunnel قد يكون شغال. تحقق من النتائج أعلاه.")
        
        # Keep running
        try:
            print("النفق شغال... لا تغلق هذه النافذة.\n")
            process.wait()
        except KeyboardInterrupt:
            print("\n\n⏹️ إيقاف النفق...")
            process.terminate()
            process.wait()
            print("انتهى.\n")
            
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")
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
    
    # Start localtunnel
    if not start_localtunnel():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
