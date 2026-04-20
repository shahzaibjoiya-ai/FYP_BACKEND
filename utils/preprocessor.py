import cv2
import numpy as np
from PIL import Image

class ImagePreprocessor:
    """Preprocess images for deepfake detection models"""
    
    @staticmethod
    def preprocess_image(image, target_size=(224, 224)):
        """
        Preprocess image for model input
        
        Args:
            image: Input image (numpy array or file path)
            target_size: Target size for the image
        
        Returns:
            Preprocessed image normalized to [0, 1]
        """
        # Load image if path is provided
        if isinstance(image, str):
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize
        if image.shape[:2] != target_size:
            image = cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
        
        # Convert to float
        image = image.astype('float32')
        
        # Normalize
        image = image / 255.0
        
        return image
    
    @staticmethod
    def preprocess_batch(images, target_size=(224, 224)):
        """
        Preprocess batch of images
        
        Args:
            images: List of images
            target_size: Target size for images
        
        Returns:
            Batch of preprocessed images
        """
        batch = np.array([ImagePreprocessor.preprocess_image(img, target_size) for img in images])
        return batch
    
    @staticmethod
    def augment_image(image, target_size=(224, 224)):
        """
        Augment image for better model robustness
        
        Args:
            image: Input image
            target_size: Target size
        
        Returns:
            List of augmented images
        """
        augmented = []
        
        # Original
        augmented.append(ImagePreprocessor.preprocess_image(image, target_size))
        
        # Horizontal flip
        if isinstance(image, str):
            img = cv2.imread(image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img = image.copy()
        
        img_flipped = cv2.flip(img, 1)
        augmented.append(ImagePreprocessor.preprocess_image(img_flipped, target_size))
        
        # Brightness adjustment
        img_bright = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
        augmented.append(ImagePreprocessor.preprocess_image(img_bright, target_size))
        
        return np.array(augmented)
    
    @staticmethod
    def normalize_tensor(tensor, mean=None, std=None):
        """
        Normalize tensor using ImageNet statistics
        
        Args:
            tensor: Input tensor
            mean: Mean values (default: ImageNet mean)
            std: Standard deviation values (default: ImageNet std)
        
        Returns:
            Normalized tensor
        """
        if mean is None:
            mean = np.array([0.485, 0.456, 0.406])
        if std is None:
            std = np.array([0.229, 0.224, 0.225])
        
        # Normalize
        for i in range(3):
            tensor[:, :, i] = (tensor[:, :, i] - mean[i]) / std[i]
        
        return tensor
