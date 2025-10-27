from flask import Flask, jsonify
from app.config import Config
from app.routes import api_bp
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Cache directory
    os.makedirs('cache', exist_ok=True)

    # Register blueprints
    app.register_blueprint(api_bp)

    # Handling global errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Country not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Validation failed"}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({"error": "External data source unavailable"}), 503

    return app
