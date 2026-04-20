import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # File upload settings
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MODEL_PATH = os.getenv('MODEL_PATH', 'models')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,mp4,avi,mov,mkv').split(','))
    
    # Detection settings
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Model settings
    FACE_DETECTION_MODEL = 'mediapipe'
    DEEPFAKE_MODEL_TYPE = 'efficientnet'  # Can be changed to 'xception', 'meso4', etc.
    
    # Logging
    LOG_DIR = 'logs'
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        os.makedirs(Config.LOG_DIR, exist_ok=True)
