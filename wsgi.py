"""WSGI entry point for production deployment (gunicorn)"""

from web import app

if __name__ == '__main__':
    app.run()
