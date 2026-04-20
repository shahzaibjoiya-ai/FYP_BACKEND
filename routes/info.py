from flask import Blueprint, jsonify, request
from utils.logger import get_logger

logger = get_logger(__name__)
info_bp = Blueprint('info', __name__, url_prefix='/api/info')

@info_bp.route('/about', methods=['GET'])
def about():
    """Get information about the API"""
    return jsonify({
        'name': 'Deepfake Detection API',
        'version': '1.0.0',
        'description': 'Detects deepfake videos and photos using deep learning',
        'author': 'Your Name',
        'endpoints': {
            'POST /api/detect-image': 'Detect deepfake in image',
            'POST /api/detect-video': 'Detect deepfake in video',
            'GET /api/health': 'Health check',
            'GET /api/model-info': 'Get model information'
        }
    }), 200


@info_bp.route('/stats', methods=['GET'])
def stats():
    """Get API statistics"""
    return jsonify({
        'status': 'active',
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'message': 'API is operational'
    }), 200
