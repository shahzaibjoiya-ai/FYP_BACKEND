# Performance Optimization Guide

## 🚀 Optimization Strategies

### 1. Model Selection

Different models offer trade-offs between speed and accuracy:

| Model | Speed | Accuracy | Memory | Best For |
|-------|-------|----------|--------|----------|
| EfficientNet | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Balanced |
| MesoNet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Real-time |
| Xception | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | High accuracy |
| ResNet50 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Balanced |
| InceptionV3 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | Best accuracy |

**Change model in `.env`:**
```env
DEEPFAKE_MODEL_TYPE=mesonet  # for fastest processing
```

### 2. Video Processing Optimization

**Adjust sample rate** - Higher = Faster, Lower = More Accurate:

```bash
# Fast but less accurate (good for screening)
curl -X POST -F "file=@video.mp4" "http://localhost:5000/api/detect-video?sample_rate=10"

# Balanced
curl -X POST -F "file=@video.mp4" "http://localhost:5000/api/detect-video?sample_rate=5"

# Slow but more accurate
curl -X POST -F "file=@video.mp4" "http://localhost:5000/api/detect-video?sample_rate=2"
```

### 3. Image Preprocessing Optimization

Edit [utils/preprocessor.py](utils/preprocessor.py):

```python
# Current (good quality)
def preprocess_image(image, target_size=(224, 224)):
    ...

# Fast (lower resolution)
def preprocess_image(image, target_size=(128, 128)):
    ...

# High quality (slower)
def preprocess_image(image, target_size=(512, 512)):
    ...
```

### 4. GPU Acceleration

#### Enable CUDA (NVIDIA GPU)

```bash
# Check if TensorFlow detects GPU
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Install GPU support
pip install tensorflow[and-cuda]
```

#### Use MPS (Apple Silicon)

```python
# Add to app.py
import tensorflow as tf

# Enable Metal Performance Shaders
with tf.device('/GPU:0'):
    # Your model will run on GPU
    pass
```

### 5. Batch Processing

For multiple files, use a queue system:

```python
from concurrent.futures import ThreadPoolExecutor

def process_files_batch(file_list, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_file, file_list))
    return results
```

### 6. Caching Results

Store results for identical files:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# Check cache before processing
cached_results = {}

def detect_with_cache(filepath):
    file_hash = get_file_hash(filepath)
    if file_hash in cached_results:
        return cached_results[file_hash]
    
    result = detect(filepath)
    cached_results[file_hash] = result
    return result
```

### 7. Memory Management

Add to [config.py](config.py):

```python
import tensorflow as tf

# Limit GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Or allocate specific amount
tf.config.set_logical_device_configuration(
    gpus[0],
    [tf.config.LogicalDeviceConfiguration(memory_limit=2048)]  # 2GB
)
```

### 8. Asynchronous Processing

For long-running detections:

```python
from celery import Celery

app = Celery('deepfake_detector')

@app.task
def detect_video_async(filepath):
    detector = get_detector()
    return detector.predict_video(filepath)

# In Flask route
@app.route('/api/detect-video-async', methods=['POST'])
def detect_video_async_route():
    # Save file
    filepath = FileHandler.save_upload(file)
    
    # Send to Celery task
    task = detect_video_async.delay(filepath)
    
    return jsonify({'task_id': task.id}), 202

# Check task status
@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    from celery.result import AsyncResult
    task = AsyncResult(task_id)
    return jsonify({'status': task.status, 'result': task.result})
```

### 9. Quantization

Reduce model size for faster inference:

```python
import tensorflow as tf

def quantize_model(model):
    # Convert model to TensorFlow Lite (smaller and faster)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    with open('model_quantized.tflite', 'wb') as f:
        f.write(tflite_model)
    
    return tflite_model

# Use quantized model
quantize_model(detector.model)
```

### 10. Lazy Loading

Load models only when needed:

```python
class DeepfakeDetector:
    def __init__(self):
        self.model = None  # Don't load immediately
    
    @property
    def detector(self):
        if self.model is None:
            self.model = self._load_model()
        return self.model
    
    def predict_image(self, image_path):
        # Model loaded only on first use
        return self.detector.predict(...)
```

## 📊 Performance Benchmarks

### Sample Results (EfficientNetB0)

| Input | Model | Sample Rate | Time | GPU | CPU |
|-------|-------|-------------|------|-----|-----|
| Image (1MB) | EfficientNet | N/A | 2-3s | 0.5s | 2-3s |
| Video (50MB) | EfficientNet | 5 | 45-60s | 15-20s | 45-60s |
| Video (50MB) | MesoNet | 5 | 20-30s | 8-12s | 20-30s |
| Batch (10 images) | EfficientNet | N/A | 15-20s | 3-5s | 15-20s |

## 🔧 Configuration Examples

### High-Speed Configuration (Real-time Detection)
```env
DEEPFAKE_MODEL_TYPE=mesonet
# In app routes, default sample_rate=10
CONFIDENCE_THRESHOLD=0.5
MAX_FILE_SIZE=20971520  # 20MB
```

### High-Accuracy Configuration
```env
DEEPFAKE_MODEL_TYPE=inception
# In app routes, default sample_rate=2
CONFIDENCE_THRESHOLD=0.7
MAX_FILE_SIZE=104857600  # 100MB
```

### Balanced Configuration (Recommended)
```env
DEEPFAKE_MODEL_TYPE=efficientnet
# In app routes, default sample_rate=5
CONFIDENCE_THRESHOLD=0.5
MAX_FILE_SIZE=52428800  # 50MB
```

## 💡 Tips & Tricks

1. **Pre-download models**: Models download on first use. Pre-download for faster first request:
   ```bash
   python -c "from deepfake_detector import get_detector; get_detector()"
   ```

2. **Monitor GPU usage**:
   ```bash
   watch -n 1 nvidia-smi  # Linux
   ```

3. **Use smaller image sizes for screening**:
   ```python
   # In preprocessor.py
   target_size=(128, 128)  # instead of (224, 224)
   ```

4. **Cache face detection results**:
   Extract faces once, cache them for batch processing

5. **Implement progressive loading**:
   Send partial results as video is being analyzed

## 🔍 Profiling & Monitoring

### Profile Your Code
```python
from cProfile import Profile
from pstats import Stats

profiler = Profile()
profiler.enable()

# Your code here
result = detector.predict_image(image_path)

profiler.disable()
stats = Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

### Monitor Resource Usage
```python
import psutil
import os

process = psutil.Process(os.getpid())

print(f"Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
print(f"CPU: {process.cpu_percent()}%")
print(f"Threads: {process.num_threads()}")
```

---

**Performance optimization is a balance between speed and accuracy. Choose the configuration that best fits your needs!**
