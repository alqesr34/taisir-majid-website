"""
This script runs the Flask app with optional ngrok tunnel for external access.

Usage:
    python run_server.py                    # Run local server only
    python run_server.py --tunnel TOKEN     # Run with ngrok tunnel (requires TOKEN)
"""

import os
import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from web import app

def run_local():
    """Run Flask development server locally"""
    print("\n" + "="*60)
    print("Running Flask Server Locally")
    print("="*60)
    
    port = int(os.environ.get('PORT', 8000))
    
    print(f"\nServer running at:")
    print(f"  http://localhost:{port}/")
    print(f"\nAdmin panel:")
    print(f"  http://localhost:{port}/login")
    print(f"\nCredentials:")
    print(f"  Username: muk")
    print(f"  Password: 12395")
    print(f"\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)


def run_with_tunnel(auth_token):
    """Run Flask with ngrok tunnel for external access"""
    try:
        from pyngrok import ngrok
        
        print("\n" + "="*60)
        print("Starting Flask + Ngrok Tunnel")
        print("="*60 + "\n")
        
        # Set auth token
        ngrok.set_auth_token(auth_token)
        
        # Create tunnel
        public_url = ngrok.connect(8000)
        print(f"\n✓ External URL: {public_url}")
        print(f"\nAccess your site from anywhere at:")
        print(f"  {public_url}")
        print(f"\nAdmin panel:")
        print(f"  {public_url}/login")
        print(f"\nCredentials:")
        print(f"  Username: muk")
        print(f"  Password: 12395")
        print(f"\nPress CTRL+C to stop\n")
        print("="*60 + "\n")
        
        # Run app
        app.run(host='0.0.0.0', port=8000, debug=False)
        
    except ImportError:
        print("\nERROR: pyngrok not installed")
        print("Install it with: pip install pyngrok")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nMake sure you have a valid ngrok auth token")
        print("Get one from: https://dashboard.ngrok.com/get-started/your-authtoken")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask app locally or with ngrok tunnel')
    parser.add_argument('--tunnel', type=str, help='Ngrok auth token for external tunnel')
    
    args = parser.parse_args()
    
    if args.tunnel:
        run_with_tunnel(args.tunnel)
    else:
        run_local()
