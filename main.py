# """
# Deepfake Detection Backend API

# This module provides a Flask-based REST API for detecting deepfakes in images and videos.
# It uses EfficientNetB0 with custom layers for binary classification (Real/Fake).

# Key Features:
# - Image deepfake detection
# - Video deepfake detection
# - Face extraction and preprocessing
# - Probability scores with confidence levels
# - CORS-enabled for Next.js frontend integration

# Installation:
#     pip install -r requirements.txt

# Running:
#     python app.py

# API Endpoints:
#     POST /api/detect-image - Upload image for deepfake detection
#     POST /api/detect-video - Upload video for deepfake detection
#     GET /api/health - Health check
#     GET /api/model-info - Get model information
#     GET /api/info/about - Get API information
#     GET /api/info/stats - Get API statistics

# Response Format:
#     {
#         "status": "success",
#         "faces_detected": 1,
#         "real_probability": 0.85,
#         "fake_probability": 0.15,
#         "is_fake": false,
#         "confidence": 0.85
#     }
# """

from app import create_app
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == '__main__':
    app = create_app()
    logger.info("=" * 50)
    logger.info("Deepfake Detection Backend Starting")
    logger.info("=" * 50)
    logger.info(f"Environment: {Config.FLASK_ENV}")
    logger.info(f"Debug: {Config.DEBUG}")
    logger.info(f"Max file size: {Config.MAX_FILE_SIZE / 1024 / 1024}MB")
    logger.info(f"Model type: {Config.DEEPFAKE_MODEL_TYPE}")
    logger.info(f"Confidence threshold: {Config.CONFIDENCE_THRESHOLD}")
    logger.info("Starting server on http://0.0.0.0:5000")
    logger.info("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG,
        use_reloader=False
    )
