# Project Structure & Architecture

## 📁 Complete Project Layout

```
BACKEND/
│
├── 📄 app.py                      # Flask application factory
├── 📄 main.py                     # Entry point - run this to start server
├── 📄 deepfake_detector.py        # Core deepfake detection model
├── 📄 config.py                   # Configuration & settings management
│
├── 📁 routes/                     # API endpoint blueprints
│   ├── __init__.py
│   ├── detection.py               # Main detection endpoints
│   └── info.py                    # Information endpoints
│
├── 📁 utils/                      # Utility modules
│   ├── __init__.py
│   ├── logger.py                  # Custom logging utility
│   ├── validators.py              # File validation functions
│   ├── file_handler.py            # File upload & cleanup
│   ├── face_extractor.py          # Face detection & extraction
│   ├── preprocessor.py            # Image preprocessing
│   └── advanced_models.py         # Alternative model architectures
│
├── 📁 models/                     # Trained model storage
│   └── (models download here on first run)
│
├── 📁 uploads/                    # Temporary file storage
│   └── (uploaded files stored here temporarily)
│
├── 📁 logs/                       # Application logs
│   └── YYYY-MM-DD.log
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env                        # Environment variables
├── 📄 .gitignore                  # Git ignore rules
│
├── 📄 setup.py                    # Setup script (cross-platform)
├── 📄 setup.bat                   # Setup script (Windows)
├── 📄 setup.sh                    # Setup script (Linux/macOS)
│
├── 📄 test_api.py                 # API testing script
│
├── 📚 README.md                   # API documentation
├── 📚 QUICKSTART.md               # 5-minute setup guide
├── 📚 INSTALLATION_GUIDE.md       # Detailed setup instructions
├── 📚 PERFORMANCE_GUIDE.md        # Optimization strategies
├── 📚 NEXTJS_INTEGRATION.md       # Frontend integration examples
└── 📚 PROJECT_STRUCTURE.md        # This file
```

## 🔧 Core Components

### 1. **app.py** - Flask Application Factory
Creates and configures the Flask application with:
- CORS setup for Next.js frontend
- Blueprint registration (routes)
- Error handlers
- Configuration initialization

### 2. **config.py** - Configuration Management
Manages all settings:
- Environment variables from `.env`
- File upload limits
- Model configuration
- CORS origins for frontend
- Logging settings

### 3. **deepfake_detector.py** - Core Detection Logic
Main detection engine:
- Model initialization (EfficientNet by default)
- Image detection: `predict_image()`
- Video detection: `predict_video()`
- Face extraction pipeline
- Prediction aggregation

### 4. **routes/detection.py** - API Endpoints
REST API endpoints:
- `POST /api/detect-image` - Image deepfake detection
- `POST /api/detect-video` - Video deepfake detection
- `GET /api/health` - Health check
- `GET /api/model-info` - Model information

### 5. **routes/info.py** - Info Endpoints
Information endpoints:
- `GET /api/info/about` - API information
- `GET /api/info/stats` - API statistics

## 🛠️ Utility Modules

### logger.py
Custom logging system:
- File logging (daily rotation)
- Console output
- Formatted timestamps
- Debug/Info/Error levels

### validators.py
File validation functions:
- File type checking
- File size validation
- Extension verification
- Image/video detection

### file_handler.py
File management:
- Upload file saving with timestamps
- Cleanup of old uploads
- File organization

### face_extractor.py
Face detection & extraction:
- MediaPipe face detection
- Bounding box extraction
- Face cropping with padding
- Batch face extraction from videos

### preprocessor.py
Image preprocessing:
- Resizing to model input size
- Normalization (0-1 range)
- Image augmentation
- Batch processing

### advanced_models.py
Alternative model architectures:
- Xception
- InceptionV3
- ResNet50
- MesoNet-4
- ModelFactory pattern

## 📊 Data Flow

### Image Detection Flow
```
┌─────────────────────┐
│ Upload Image (POST) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ File Validation     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Save Temporarily    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extract Faces       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Preprocess Faces    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Run Model           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Aggregate Results   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Return JSON         │
└─────────────────────┘
```

### Video Detection Flow
```
┌─────────────────────┐
│ Upload Video (POST) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ File Validation     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Save Temporarily    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extract Frames      │
│ (sample_rate)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extract Faces       │
│ from Frames         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Preprocess All      │
│ Extracted Faces     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Run Model on All    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Calculate Stats     │
│ (mean, std, max)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Return JSON         │
└─────────────────────┘
```

## 📤 Response Format

### Success Response
```json
{
    "status": "success",
    "faces_detected": 1,
    "real_probability": 0.85,
    "fake_probability": 0.15,
    "is_fake": false,
    "confidence": 0.85,
    "filename": "image.jpg"
}
```

### Video Success Response
```json
{
    "status": "success",
    "frames_analyzed": 150,
    "real_probability": 0.78,
    "fake_probability": 0.22,
    "is_fake": false,
    "confidence": 0.78,
    "frame_predictions": {
        "max_fake_score": 0.45,
        "min_fake_score": 0.10,
        "std_fake_score": 0.12
    },
    "filename": "video.mp4"
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description here"
}
```

## 🔄 Request-Response Cycle

1. **Client** sends file via POST multipart/form-data
2. **routes/detection.py** receives request
3. **validators.py** validates file
4. **file_handler.py** saves file temporarily
5. **deepfake_detector.py** processes file
6. **face_extractor.py** extracts faces
7. **preprocessor.py** prepares images
8. **Model** makes predictions
9. **Results** aggregated and formatted
10. **Response** sent to client
11. **file_handler.py** cleans up temporary file

## 🗄️ Dependencies

### Core Framework
- **Flask** - Web framework
- **Flask-CORS** - Cross-Origin support

### Deep Learning
- **TensorFlow** - Neural network framework
- **PyTorch** - Alternative ML framework
- **Keras** - Neural network API

### Computer Vision
- **OpenCV** - Image/video processing
- **MediaPipe** - Face detection
- **scikit-image** - Image processing

### Utilities
- **NumPy** - Numerical operations
- **Pillow** - Image manipulation
- **Matplotlib** - Visualization
- **SciPy** - Scientific computing

## ⚙️ Configuration Files

### .env
Environment variables:
- Flask settings
- File upload limits
- CORS origins
- Model type
- Confidence threshold

### requirements.txt
Python package dependencies:
- Versions specified for reproducibility
- Can be installed with: `pip install -r requirements.txt`

### config.py
Python configuration:
- Reads from .env
- Validates settings
- Initializes directories
- Provides defaults

## 🚀 Startup Sequence

When you run `python main.py`:

1. **config.py** loads and validates settings
2. **logger.py** initializes logging system
3. **app.py** creates Flask application
4. **routes** blueprints are registered
5. **deepfake_detector.py** loads/creates model
6. **Server** starts on http://0.0.0.0:5000
7. **Ready** for requests

## 🔌 Integration Points

### Frontend (Next.js)
- Sends HTTP POST requests to `/api/detect-image` or `/api/detect-video`
- Receives JSON responses with probabilities
- Displays results in UI/charts

### Database (Optional)
- Can be added to store detection history
- User management
- Result archiving

### Notification Service (Optional)
- Email alerts for detection results
- Webhook callbacks

## 📝 Key Functions

### deepfake_detector.py
```python
get_detector()              # Get detector instance
predict_image(path)         # Detect in image
predict_video(path, rate)   # Detect in video
predict_batch(paths)        # Detect multiple files
save_model()               # Save model to disk
```

### face_extractor.py
```python
extract_faces_from_image()  # Extract faces from image
extract_faces_from_video()  # Extract faces from video
```

### preprocessor.py
```python
preprocess_image()          # Preprocess single image
preprocess_batch()          # Preprocess multiple
augment_image()            # Data augmentation
normalize_tensor()         # Normalization
```

### validators.py
```python
allowed_file()             # Check file type
is_image()                # Check if image
is_video()                # Check if video
validate_file_size()       # Check size limit
secure_upload_filename()   # Secure filename
```

## 🧪 Testing

### Unit Tests
Test individual functions in isolation

### Integration Tests
Test complete workflows (upload → detect → response)

### Load Tests
Test system under multiple concurrent requests

### Performance Tests
Benchmark detection speed and accuracy

Use `test_api.py` to verify all endpoints work correctly.

## 🔐 Security Considerations

1. **File Upload**
   - Size limits in `MAX_FILE_SIZE`
   - Extension validation
   - Secure filename handling
   - Temporary storage cleanup

2. **CORS**
   - Restricted to frontend URL
   - Configurable in `.env`

3. **Input Validation**
   - All file inputs validated
   - Proper error handling

4. **Logging**
   - Request logging in `logs/`
   - No sensitive data logged

## 📈 Scalability

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer
- Separate API and model servers

### Vertical Scaling
- Use GPU acceleration
- Increase RAM
- Use faster storage (SSD)

### Optimization
- Model quantization
- Batch processing
- Caching results
- Async processing with Celery

---

**This architecture is production-ready and can be extended with additional features as needed!**
