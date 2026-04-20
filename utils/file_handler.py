import os
import shutil
from datetime import datetime
from config import Config

class FileHandler:
    """Handle file upload and cleanup"""
    
    @staticmethod
    def save_upload(file):
        """Save uploaded file to uploads folder"""
        if not file or file.filename == '':
            raise ValueError("No file provided")
        
        # Create timestamped subfolder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        upload_subfolder = os.path.join(Config.UPLOAD_FOLDER, timestamp)
        os.makedirs(upload_subfolder, exist_ok=True)
        
        # Save file
        filepath = os.path.join(upload_subfolder, file.filename)
        file.save(filepath)
        
        return filepath
    
    @staticmethod
    def cleanup_file(filepath):
        """Delete uploaded file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file {filepath}: {str(e)}")
    
    @staticmethod
    def cleanup_old_uploads(days=1):
        """Clean up uploads older than specified days"""
        import time
        
        current_time = time.time()
        age_seconds = days * 24 * 60 * 60
        
        if not os.path.exists(Config.UPLOAD_FOLDER):
            return
        
        for timestamp_folder in os.listdir(Config.UPLOAD_FOLDER):
            folder_path = os.path.join(Config.UPLOAD_FOLDER, timestamp_folder)
            
            if os.path.isdir(folder_path):
                folder_age = current_time - os.path.getmtime(folder_path)
                
                if folder_age > age_seconds:
                    shutil.rmtree(folder_path)
