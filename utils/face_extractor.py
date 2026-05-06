import cv2
import numpy as np
import os
from utils.logger import get_logger

logger = get_logger(__name__)

mp = None
MEDIAPIPE_AVAILABLE = False

class FaceExtractor:
    """Extract faces from images and video frames with multiple detection methods"""
    
    def __init__(self):
        global mp, MEDIAPIPE_AVAILABLE
        self.mp_face_detection = None
        self.face_detection = None
        self.haar_cascade = None
        self.detection_method = "none"
        
        # Try MediaPipe first
        try:
            if mp is None:
                import mediapipe
                mp = mediapipe
                MEDIAPIPE_AVAILABLE = True
            
            if MEDIAPIPE_AVAILABLE:
                self.mp_face_detection = mp.solutions.face_detection
                self.face_detection = self.mp_face_detection.FaceDetection(
                    model_selection=1,
                    min_detection_confidence=0.5
                )
                self.detection_method = "mediapipe"
                logger.info("✓ MediaPipe face detection initialized successfully")
        
        except ImportError as e:
            logger.warning(f"⚠️  MediaPipe not available: {str(e)}")
            logger.warning("   Install with: pip install mediapipe")
            self.face_detection = None
        except Exception as e:
            logger.error(f"✗ Error initializing MediaPipe: {str(e)}")
            self.face_detection = None
        
        # Fallback: Load OpenCV Haar Cascade
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self.haar_cascade = cv2.CascadeClassifier(cascade_path)
                if not self.haar_cascade.empty():
                    if self.face_detection is None:
                        self.detection_method = "haar_cascade"
                        logger.info("✓ Fallback: OpenCV Haar Cascade loaded successfully")
                    else:
                        logger.info("ℹ️  Haar Cascade available as fallback")
                else:
                    logger.warning("⚠️  Haar Cascade loaded but empty")
            else:
                logger.warning(f"⚠️  Haar Cascade file not found at: {cascade_path}")
        except Exception as e:
            logger.error(f"✗ Error loading Haar Cascade: {str(e)}")
        
        # Check final status
        if self.face_detection is None and (self.haar_cascade is None or self.haar_cascade.empty()):
            logger.critical("✗ CRITICAL: No face detection method available!")
            logger.critical("   Please install MediaPipe: pip install mediapipe")
            self.detection_method = "none"
        
        logger.info(f"Face detection initialized with method: {self.detection_method}")

    def extract_faces_from_image(self, image_path):
        """Extract faces from image using available detection method"""
        
        if self.detection_method == "none":
            logger.error("✗ Face detection not initialized - no detection method available")
            logger.error("   Solution: Install MediaPipe with: pip install mediapipe")
            return []

        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"✗ Failed to load image: {image_path}")
                return []
            
            faces = []
            
            # Try MediaPipe first
            if self.face_detection is not None:
                try:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = self.face_detection.process(image_rgb)
                    
                    if results.detections:
                        h, w, _ = image.shape
                        for detection in results.detections:
                            bbox = detection.location_data.relative_bounding_box
                            x, y, w_face, h_face = (
                                int(bbox.xmin * w),
                                int(bbox.ymin * h),
                                int(bbox.width * w),
                                int(bbox.height * h)
                            )
                            
                            padding = 20
                            x = max(0, x - padding)
                            y = max(0, y - padding)
                            x_end = min(w, x + w_face + padding)
                            y_end = min(h, y + h_face + padding)
                            
                            face = image[y:y_end, x:x_end]
                            if face.size > 0:
                                faces.append(face)
                    
                    if faces:
                        logger.info(f"✓ Extracted {len(faces)} faces from image using MediaPipe")
                        return faces
                except Exception as e:
                    logger.warning(f"⚠️  MediaPipe detection failed: {str(e)}, trying Haar Cascade...")
            
            # Fallback to Haar Cascade
            if self.haar_cascade is not None and not self.haar_cascade.empty():
                try:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    detected_faces = self.haar_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30)
                    )
                    
                    for (x, y, w, h) in detected_faces:
                        padding = 20
                        x = max(0, x - padding)
                        y = max(0, y - padding)
                        x_end = min(image.shape[1], x + w + 2*padding)
                        y_end = min(image.shape[0], y + h + 2*padding)
                        
                        face = image[y:y_end, x:x_end]
                        if face.size > 0:
                            faces.append(face)
                    
                    if faces:
                        logger.info(f"✓ Extracted {len(faces)} faces from image using Haar Cascade")
                        return faces
                    else:
                        logger.warning("⚠️  No faces detected in image")
                        return []
                except Exception as e:
                    logger.error(f"✗ Haar Cascade detection failed: {str(e)}")
                    return []
            
            logger.warning("⚠️  No faces detected and no fallback available")
            return []
        
        except Exception as e:
            logger.error(f"✗ Error extracting faces from image: {str(e)}")
            return []

    def extract_faces_from_video(self, video_path, frame_sample_rate=5):
        """Extract faces from video frames using available detection method"""
        
        if self.detection_method == "none":
            logger.error("✗ Face detection not initialized - no detection method available")
            logger.error("   Solution: Install MediaPipe with: pip install mediapipe")
            return []

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logger.error(f"✗ Failed to open video: {video_path}")
                return []
            
            faces = []
            frame_count = 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            logger.info(f"Processing video: {total_frames} frames, sampling every {frame_sample_rate} frames")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_sample_rate == 0:
                    # Try MediaPipe first
                    if self.face_detection is not None:
                        try:
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = self.face_detection.process(frame_rgb)
                            
                            if results.detections:
                                h, w, _ = frame.shape
                                for detection in results.detections:
                                    bbox = detection.location_data.relative_bounding_box
                                    x, y, w_face, h_face = (
                                        int(bbox.xmin * w),
                                        int(bbox.ymin * h),
                                        int(bbox.width * w),
                                        int(bbox.height * h)
                                    )
                                    
                                    padding = 20
                                    x = max(0, x - padding)
                                    y = max(0, y - padding)
                                    x_end = min(w, x + w_face + padding)
                                    y_end = min(h, y + h_face + padding)
                                    
                                    face = frame[y:y_end, x:x_end]
                                    if face.size > 0:
                                        faces.append(face)
                        except Exception as e:
                            logger.warning(f"⚠️  MediaPipe detection failed for frame {frame_count}: {str(e)}")
                            # Try Haar Cascade for this frame
                            if self.haar_cascade is not None and not self.haar_cascade.empty():
                                try:
                                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                    detected_faces = self.haar_cascade.detectMultiScale(
                                        gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(30, 30)
                                    )
                                    
                                    for (x, y, w, h) in detected_faces:
                                        padding = 20
                                        x = max(0, x - padding)
                                        y = max(0, y - padding)
                                        x_end = min(frame.shape[1], x + w + 2*padding)
                                        y_end = min(frame.shape[0], y + h + 2*padding)
                                        
                                        face = frame[y:y_end, x:x_end]
                                        if face.size > 0:
                                            faces.append(face)
                                except Exception as e2:
                                    logger.debug(f"Haar Cascade also failed for frame {frame_count}")
                    
                    # Use Haar Cascade if MediaPipe is not available
                    elif self.haar_cascade is not None and not self.haar_cascade.empty():
                        try:
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            detected_faces = self.haar_cascade.detectMultiScale(
                                gray,
                                scaleFactor=1.1,
                                minNeighbors=5,
                                minSize=(30, 30)
                            )
                            
                            for (x, y, w, h) in detected_faces:
                                padding = 20
                                x = max(0, x - padding)
                                y = max(0, y - padding)
                                x_end = min(frame.shape[1], x + w + 2*padding)
                                y_end = min(frame.shape[0], y + h + 2*padding)
                                
                                face = frame[y:y_end, x:x_end]
                                if face.size > 0:
                                    faces.append(face)
                        except Exception as e:
                            logger.debug(f"Haar Cascade detection failed for frame {frame_count}: {str(e)}")
                
                frame_count += 1
            
            cap.release()
            logger.info(f"✓ Extracted {len(faces)} faces from video ({frame_count} frames processed)")
            return faces
        
        except Exception as e:
            logger.error(f"✗ Error extracting faces from video: {str(e)}")
            return []

    def is_available(self):
        """Check if face detection is available"""
        return self.detection_method != "none"
    
    def get_detection_method(self):
        """Get the current face detection method"""
        return self.detection_method
    
    def get_status(self):
        """Get detailed status information"""
        return {
            'detection_method': self.detection_method,
            'available': self.is_available(),
            'mediapipe_available': self.face_detection is not None,
            'haar_cascade_available': self.haar_cascade is not None and not self.haar_cascade.empty()
        }

    def __del__(self):
        """Cleanup resources"""
        try:
            if hasattr(self, "face_detection") and self.face_detection:
                self.face_detection.close()
                logger.debug("✓ MediaPipe resources cleaned up")
        except Exception as e:
            logger.debug(f"Note during cleanup: {str(e)}")