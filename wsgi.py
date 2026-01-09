"""
WSGI entry point for production deployment
"""
from main import app, init_db

# Initialize database on first run
init_db()

if __name__ == "__main__":
    app.run()
