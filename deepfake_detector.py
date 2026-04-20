import os
from utils.logger import get_logger
from config import Config

logger = get_logger(__name__)

# Try to import ML dependencies
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    logger.warning("numpy not available - detection features will be limited")

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    logger.warning("opencv-python not available - detection features will be limited")

try:
    import tensorflow as tf
    from keras.models import load_model
    HAS_TF = True
except ImportError:
    HAS_TF = False
    logger.warning("tensorflow not available - detection features will be limited")

try:
    from utils.preprocessor import ImagePreprocessor
    HAS_PREPROCESSOR = True
except ImportError:
    HAS_PREPROCESSOR = False
    logger.warning("ImagePreprocessor not available")

try:
    from utils.face_extractor import FaceExtractor
    HAS_FACE_EXTRACTOR = True
except ImportError:
    HAS_FACE_EXTRACTOR = False
    logger.warning("FaceExtractor not available")

class DeepfakeDetector:
    """Main deepfake detection model"""
    
    def __init__(self, model_type='efficientnet'):
        self.model_type = model_type
        self.model = None
        self.available = HAS_TF and HAS_CV2 and HAS_NUMPY and HAS_FACE_EXTRACTOR and HAS_PREPROCESSOR
        
        if not self.available:
            logger.warning(f"DeepfakeDetector initialized in stub mode - missing ML dependencies")
            return
        
        try:
            self.face_extractor = FaceExtractor()
            self.preprocessor = ImagePreprocessor()
            self.model_path = os.path.join(Config.MODEL_PATH, f'{model_type}_model.h5')
            
            # Load or create model
            self._initialize_model()
        except Exception as e:
            logger.error(f"Error initializing DeepfakeDetector: {str(e)}")
            self.available = False
    
    def _initialize_model(self):
        """Initialize or load the deepfake detection model"""
        if not self.available:
            return
        
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading existing model from {self.model_path}")
                self.model = load_model(self.model_path)
            else:
                logger.info(f"Creating new {self.model_type} model")
                self._create_model()
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            self._create_model()
    
    def _create_model(self):
        """Create a new EfficientNet-based model for deepfake detection"""
        if not HAS_TF:
            logger.error("Cannot create model - TensorFlow not available")
            return
        
        try:
            if self.model_type == 'efficientnet':
                # Use EfficientNetB0 as backbone
                base_model = tf.keras.applications.EfficientNetB0(
                    input_shape=(224, 224, 3),
                    include_top=False,
                    weights='imagenet'
                )
                base_model.trainable = False
                
                # Add custom top layers
                inputs = tf.keras.Input(shape=(224, 224, 3))
                x = base_model(inputs, training=False)
                x = tf.keras.layers.GlobalAveragePooling2D()(x)
                x = tf.keras.layers.Dense(256, activation='relu')(x)
                x = tf.keras.layers.Dropout(0.5)(x)
                x = tf.keras.layers.Dense(128, activation='relu')(x)
                x = tf.keras.layers.Dropout(0.3)(x)
                outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
                
                self.model = tf.keras.Model(inputs, outputs)
                
                # Compile
                self.model.compile(
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                    loss='binary_crossentropy',
                    metrics=['accuracy']
                )
                
                logger.info("EfficientNetB0 model created successfully")
            else:
                logger.error(f"Unknown model type: {self.model_type}")
        
        except Exception as e:
            logger.error(f"Error creating model: {str(e)}")
    
    def predict_image(self, image_path):
        """
        Predict if an image is deepfake or real
        
        Args:
            image_path: Path to image file
        
        Returns:
            Dictionary with predictions and confidence scores
        """
        try:
            # Extract faces
            faces = self.face_extractor.extract_faces_from_image(image_path)
            
            if not faces:
                logger.warning(f"No faces detected in image: {image_path}")
                return {
                    'status': 'no_faces',
                    'message': 'No faces detected in the image',
                    'real_probability': 0.5,
                    'fake_probability': 0.5,
                    'is_fake': None
                }
            
            # Preprocess faces
            preprocessed_faces = self.preprocessor.preprocess_batch(faces)
            
            # Get predictions
            predictions = self.model.predict(preprocessed_faces, verbose=0)
            
            # Calculate average confidence
            avg_prediction = np.mean(predictions)
            
            result = {
                'status': 'success',
                'faces_detected': len(faces),
                'fake_probability': float(avg_prediction),
                'real_probability': float(1 - avg_prediction),
                'is_fake': bool(avg_prediction > Config.CONFIDENCE_THRESHOLD),
                'confidence': float(max(avg_prediction, 1 - avg_prediction))
            }
            
            logger.info(f"Image prediction: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Error predicting image: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'real_probability': 0.5,
                'fake_probability': 0.5,
                'is_fake': None
            }
    
    def predict_video(self, video_path, sample_rate=5):
        """
        Predict if a video is deepfake or real
        
        Args:
            video_path: Path to video file
            sample_rate: Sample every N frames
        
        Returns:
            Dictionary with predictions across video frames
        """
        try:
            # Extract faces from video
            faces = self.face_extractor.extract_faces_from_video(video_path, sample_rate)
            
            if not faces:
                logger.warning(f"No faces detected in video: {video_path}")
                return {
                    'status': 'no_faces',
                    'message': 'No faces detected in the video',
                    'real_probability': 0.5,
                    'fake_probability': 0.5,
                    'is_fake': None
                }
            
            # Preprocess faces
            preprocessed_faces = self.preprocessor.preprocess_batch(faces)
            
            # Get predictions for all frames
            predictions = self.model.predict(preprocessed_faces, verbose=0)
            
            # Calculate statistics
            avg_prediction = np.mean(predictions)
            max_prediction = np.max(predictions)
            min_prediction = np.min(predictions)
            std_prediction = np.std(predictions)
            
            result = {
                'status': 'success',
                'frames_analyzed': len(faces),
                'fake_probability': float(avg_prediction),
                'real_probability': float(1 - avg_prediction),
                'is_fake': bool(avg_prediction > Config.CONFIDENCE_THRESHOLD),
                'confidence': float(max(avg_prediction, 1 - avg_prediction)),
                'frame_predictions': {
                    'max_fake_score': float(max_prediction),
                    'min_fake_score': float(min_prediction),
                    'std_fake_score': float(std_prediction)
                }
            }
            
            logger.info(f"Video prediction: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Error predicting video: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'real_probability': 0.5,
                'fake_probability': 0.5,
                'is_fake': None
            }
    
    def predict_batch(self, file_paths):
        """
        Predict multiple files at once
        
        Args:
            file_paths: List of file paths
        
        Returns:
            List of predictions
        """
        results = []
        for file_path in file_paths:
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                result = self.predict_video(file_path)
            else:
                result = self.predict_image(file_path)
            results.append(result)
        
        return results
    
    def save_model(self):
        """Save the model"""
        try:
            if self.model:
                os.makedirs(Config.MODEL_PATH, exist_ok=True)
                self.model.save(self.model_path)
                logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")


# Initialize detector
detector = None

def get_detector():
    """Get or create detector instance"""
    global detector
    if detector is None:
        detector = DeepfakeDetector(model_type=Config.DEEPFAKE_MODEL_TYPE)
    return detector
