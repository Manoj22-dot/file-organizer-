"""
File Organizer Pro - Main Application Entry Point
"""

from flask import Flask
from modules.database import init_db
from modules.routes import register_routes
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'file-organizer-secret-2024'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads_demo')
    app.config['ORGANIZED_FOLDER'] = os.path.join(os.path.dirname(__file__), 'organized')
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'database', 'organizer.db')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['ORGANIZED_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    # Initialize database
    with app.app_context():
        init_db(app)

    # Register all routes
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    print("🗂️  File Organizer Pro running at http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
