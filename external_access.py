#!/usr/bin/env python3
"""
External Access Helper for Taisir Majid Website
Supports multiple tunneling methods
"""

import os
import sys
import time
import subprocess
import requests

def test_local_server(port=8000, timeout=5):
    """Test if Flask server is running locally"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=timeout)
        return response.status_code == 200
    except:
        return False

def get_ngrok_url():
    """Get public URL from ngrok if available"""
    try:
        from pyngrok import ngrok
        tunnels = ngrok.get_tunnels()
        if tunnels:
            return tunnels[0].public_url
    except:
        pass
    return None

def print_status():
    """Print current status"""
    print("\n" + "="*60)
    print("TAISIR MAJID WEBSITE - ACCESS INFORMATION")
    print("="*60)
    
    # Local access
    print("\n1. LOCAL ACCESS (on local network):")
    print("   - http://localhost:8000")
    print("   - http://192.168.1.108:8000")
    
    # Check ngrok
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        print(f"\n2. EXTERNAL ACCESS (via ngrok):")
        print(f"   - {ngrok_url}")
    else:
        print("\n2. EXTERNAL ACCESS:")
        print("   - ngrok not configured")
        print("   - SSH tunnel may be active (check terminal)")
    
    # Admin
    print(f"\n3. ADMIN PANEL:")
    print("   - URL: /login")
    print("   - Username: muk")
    print("   - Password: 12395")
    
    print("\n" + "="*60 + "\n")

def start_ngrok(auth_token):
    """Start ngrok tunnel with auth token"""
    if not auth_token:
        print("ERROR: ngrok auth token not provided")
        return False
    
    try:
        from pyngrok import ngrok
        ngrok.set_auth_token(auth_token)
        public_url = ngrok.connect(8000)
        print(f"ngrok tunnel active: {public_url}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to start ngrok - {str(e)[:100]}")
        return False

def main():
    """Main function"""
    
    # Check for Flask server
    print("Checking local server...")
    if test_local_server():
        print("✓ Flask server is running on localhost:8000")
    else:
        print("✗ Flask server is NOT running")
        print("  Start it with: python web.py")
        return 1
    
    # Check for ngrok token in command line or environment
    ngrok_token = None
    if len(sys.argv) > 1:
        ngrok_token = sys.argv[1]
    else:
        ngrok_token = os.environ.get("NGROK_AUTH_TOKEN")
    
    if ngrok_token:
        print("\nStarting ngrok tunnel...")
        start_ngrok(ngrok_token)
    
    # Print status
    print_status()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        return 0

if __name__ == "__main__":
    sys.exit(main())
