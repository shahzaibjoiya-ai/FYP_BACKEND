import os
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def secure_upload_filename(filename):
    """Secure and validate upload filename"""
    filename = secure_filename(filename)
    if not filename:
        raise ValueError("Invalid filename")
    
    if not allowed_file(filename):
        raise ValueError(f"File type not allowed. Allowed types: {Config.ALLOWED_EXTENSIONS}")
    
    return filename

def is_image(filename):
    """Check if file is an image"""
    image_extensions = {'jpg', 'jpeg', 'png'}
    return filename.rsplit('.', 1)[1].lower() in image_extensions

def is_video(filename):
    """Check if file is a video"""
    video_extensions = {'mp4', 'avi', 'mov', 'mkv'}
    return filename.rsplit('.', 1)[1].lower() in video_extensions

def validate_file_size(file_size):
    """Validate file size"""
    if file_size > Config.MAX_FILE_SIZE:
        raise ValueError(f"File size exceeds maximum allowed size of {Config.MAX_FILE_SIZE / 1024 / 1024}MB")

def get_file_info(filepath):
    """Get detailed file information"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    file_size = os.path.getsize(filepath)
    filename = os.path.basename(filepath)
    
    return {
        'filename': filename,
        'size': file_size,
        'is_image': is_image(filename),
        'is_video': is_video(filename),
        'path': filepath
    }
