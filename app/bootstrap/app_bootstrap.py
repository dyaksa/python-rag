from flask import Flask

from app.controller import ingest_bp

def create_app():
    app = Flask(__name__)

    app.config.update({'MAX_CONTENT_LENGTH': 16 * 1024 * 1024})  # 16 MB limit

    # Correct parameter name is url_prefix
    app.register_blueprint(ingest_bp, url_prefix='/api/ingest')

    return app

