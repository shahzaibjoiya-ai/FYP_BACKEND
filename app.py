from flask import Flask
from flask_cors import CORS
from config import Config
from routes.detection import detection_bp
from routes.info import info_bp
from utils.logger import get_logger

logger = get_logger(__name__)

def create_app(config_class=Config):
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize configuration
    config_class.init_app(app)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config_class.CORS_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(detection_bp)
    app.register_blueprint(info_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return {'error': 'Internal server error'}, 500
    
    logger.info("Flask application created successfully")
    return app


if __name__ == '__main__':
    app = create_app()
    logger.info("Starting Deepfake Detection API...")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
