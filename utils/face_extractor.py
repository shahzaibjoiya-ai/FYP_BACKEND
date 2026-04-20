import cv2
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)

mp = None

class FaceExtractor:
    """Extract faces from images and video frames"""
    
    def __init__(self):
        global mp
        try:
            if mp is None:
                import mediapipe
                mp = mediapipe
            
            self.mp_face_detection = mp.solutions.face_detection
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=1,
                min_detection_confidence=0.5
            )
        
        except Exception as e:
            logger.error(f"Error initializing MediaPipe: {str(e)}")
            self.face_detection = None  # IMPORTANT fallback

    def extract_faces_from_image(self, image_path):
        if self.face_detection is None:
            logger.error("Face detection not initialized")
            return []

        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return []
            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(image_rgb)
            
            faces = []
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
                    face = image[y:y+h_face+padding, x:x+w_face+padding]
                    
                    if face.size > 0:
                        faces.append(face)
            
            logger.info(f"Extracted {len(faces)} faces from image")
            return faces
        
        except Exception as e:
            logger.error(f"Error extracting faces from image: {str(e)}")
            return []

    def extract_faces_from_video(self, video_path, frame_sample_rate=5):
        if self.face_detection is None:
            logger.error("Face detection not initialized")
            return []

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return []
            
            faces = []
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_sample_rate == 0:
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
                            face = frame[y:y+h_face+padding, x:x+w_face+padding]
                            
                            if face.size > 0:
                                faces.append(face)
                
                frame_count += 1
            
            cap.release()
            logger.info(f"Extracted {len(faces)} faces from video")
            return faces
        
        except Exception as e:
            logger.error(f"Error extracting faces from video: {str(e)}")
            return []

    def __del__(self):
        if hasattr(self, "face_detection") and self.face_detection:
            try:
                self.face_detection.close()
            except:
                pass