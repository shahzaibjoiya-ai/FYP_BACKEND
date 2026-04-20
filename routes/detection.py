from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from deepfake_detector import get_detector
from utils.logger import get_logger
from utils.validators import allowed_file, secure_upload_filename, validate_file_size
from utils.file_handler import FileHandler
from config import Config

logger = get_logger(__name__)
detection_bp = Blueprint('detection', __name__, url_prefix='/api')

@detection_bp.route('/detect-image', methods=['POST'])
def detect_image():
    """
    Detect deepfake in image
    
    Expected: multipart/form-data with 'file' key
    Returns: JSON with detection results
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        filename = secure_upload_filename(file.filename)
        
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            return jsonify({'error': 'Only JPG, JPEG, and PNG images are supported'}), 400
        
        # Validate size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        try:
            validate_file_size(file_size)
        except ValueError as e:
            return jsonify({'error': str(e)}), 413
        
        # Save file
        filepath = FileHandler.save_upload(file)
        logger.info(f"File uploaded: {filepath}")
        
        # Detect
        detector = get_detector()
        
        if not hasattr(detector, 'available') or not detector.available:
            return jsonify({
                'error': 'Detection model is not available. Please install all required ML dependencies (tensorflow, torch, mediapipe, dlib).',
                'status': 'unavailable',
                'code': 'ML_DEPENDENCIES_MISSING'
            }), 503
        
        result = detector.predict_image(filepath)
        
        # Add file info
        result['filename'] = filename
        
        # Cleanup (optional - keep for analysis)
        # FileHandler.cleanup_file(filepath)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in detect_image: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500


@detection_bp.route('/detect-video', methods=['POST'])
def detect_video():
    """
    Detect deepfake in video
    
    Expected: multipart/form-data with 'file' key
    Returns: JSON with detection results
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        filename = secure_upload_filename(file.filename)
        
        if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            return jsonify({'error': 'Only MP4, AVI, MOV, and MKV videos are supported'}), 400
        
        # Validate size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        try:
            validate_file_size(file_size)
        except ValueError as e:
            return jsonify({'error': str(e)}), 413
        
        # Save file
        filepath = FileHandler.save_upload(file)
        logger.info(f"File uploaded: {filepath}")
        
        # Get sample rate parameter
        sample_rate = request.args.get('sample_rate', 5, type=int)
        
        # Detect
        detector = get_detector()
        
        if not hasattr(detector, 'available') or not detector.available:
            return jsonify({
                'error': 'Detection model is not available. Please install all required ML dependencies (tensorflow, torch, mediapipe, dlib).',
                'status': 'unavailable',
                'code': 'ML_DEPENDENCIES_MISSING'
            }), 503
        
        result = detector.predict_video(filepath, sample_rate=sample_rate)
        
        # Add file info
        result['filename'] = filename
        
        # Cleanup (optional)
        # FileHandler.cleanup_file(filepath)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in detect_video: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500


@detection_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Deepfake detection API is running'
    }), 200


@detection_bp.route('/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        detector = get_detector()
        return jsonify({
            'model_type': detector.model_type,
            'status': 'loaded' if detector.model else 'not_loaded',
            'confidence_threshold': Config.CONFIDENCE_THRESHOLD,
            'supported_image_formats': ['jpg', 'jpeg', 'png'],
            'supported_video_formats': ['mp4', 'avi', 'mov', 'mkv']
        }), 200
    except Exception as e:
        logger.error(f"Error in model_info: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500
