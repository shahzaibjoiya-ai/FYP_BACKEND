# Deepfake Detection Backend - Next.js Frontend Integration Guide

## Overview
This is a Python Flask backend for detecting deepfakes in images and videos. It's designed to work seamlessly with a Next.js frontend.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` file to customize settings:
```env
FLASK_ENV=development
DEBUG=True
MAX_FILE_SIZE=52428800
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=jpg,jpeg,png,mp4,avi,mov,mkv
CONFIDENCE_THRESHOLD=0.5
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 3. Run the Server
```bash
python main.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### 1. Detect Image Deepfake
**Endpoint:** `POST /api/detect-image`

**Request:**
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/detect-image
```

**Response:**
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

### 2. Detect Video Deepfake
**Endpoint:** `POST /api/detect-video?sample_rate=5`

**Request:**
```bash
curl -X POST -F "file=@video.mp4" http://localhost:5000/api/detect-video?sample_rate=5
```

**Response:**
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

### 3. Health Check
**Endpoint:** `GET /api/health`

**Response:**
```json
{
    "status": "healthy",
    "message": "Deepfake detection API is running"
}
```

### 4. Model Information
**Endpoint:** `GET /api/model-info`

**Response:**
```json
{
    "model_type": "efficientnet",
    "status": "loaded",
    "confidence_threshold": 0.5,
    "supported_image_formats": ["jpg", "jpeg", "png"],
    "supported_video_formats": ["mp4", "avi", "mov", "mkv"]
}
```

## Next.js Frontend Integration

### Example: Upload Image for Detection
```javascript
const detectImage = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/api/detect-image', {
        method: 'POST',
        body: formData,
    });

    return await response.json();
};
```

### Example: Upload Video for Detection
```javascript
const detectVideo = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/api/detect-video?sample_rate=5', {
        method: 'POST',
        body: formData,
    });

    return await response.json();
};
```

### Example: Display Results with Chart
```javascript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const ResultsChart = ({ result }) => {
    const chartData = [
        {
            name: 'Score',
            real: (result.real_probability * 100).toFixed(2),
            fake: (result.fake_probability * 100).toFixed(2),
        },
    ];

    return (
        <LineChart width={600} height={300} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="real" stroke="#8884d8" />
            <Line type="monotone" dataKey="fake" stroke="#ff7300" />
        </LineChart>
    );
};
```

## Project Structure
```
BACKEND/
├── app.py              # Flask application factory
├── main.py             # Entry point
├── config.py           # Configuration settings
├── deepfake_detector.py # Main detection model
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── routes/
│   ├── detection.py   # Detection endpoints
│   └── info.py        # Info endpoints
├── utils/
│   ├── logger.py      # Logging utility
│   ├── validators.py  # File validation
│   ├── file_handler.py # File upload handling
│   ├── face_extractor.py # Face extraction
│   └── preprocessor.py # Image preprocessing
├── models/            # Trained model storage
├── uploads/           # Temporary file uploads
└── logs/              # Application logs
```

## Supported File Formats

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)

### Videos
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- Matroska (.mkv)

## Performance Tips

1. **Video Processing:**
   - Use `sample_rate` parameter to reduce processing time
   - Default: every 5th frame is analyzed
   - Increase sample_rate for faster processing (e.g., ?sample_rate=10)
   - Decrease for more accuracy (e.g., ?sample_rate=2)

2. **Batch Processing:**
   - Process multiple files sequentially rather than in parallel
   - Monitor server memory usage

3. **Model Optimization:**
   - Model is cached in memory after first load
   - Subsequent requests are much faster

## Troubleshooting

### Issue: "No module named 'mediapipe'"
**Solution:** Install missing dependencies
```bash
pip install mediapipe
```

### Issue: CORS errors from Next.js
**Solution:** Update CORS_ORIGINS in `.env`
```env
CORS_ORIGINS=http://localhost:3000
```

### Issue: File size too large
**Solution:** Increase MAX_FILE_SIZE in `.env`
```env
MAX_FILE_SIZE=104857600  # 100MB
```

### Issue: No faces detected
**Solution:** 
- Ensure image/video has clear faces
- Try with sample_rate=2 or 3 for videos
- Check image brightness and contrast

## Model Details

The backend uses **EfficientNetB0** with custom layers:
- Pre-trained on ImageNet
- Fine-tuned for deepfake detection
- Binary classification: Real (0) vs Fake (1)
- Sigmoid activation for probability output
- Confidence threshold: 0.5

## Future Enhancements

1. **Multi-Model Ensemble:** Combine multiple models for better accuracy
2. **Training Interface:** Fine-tune model with custom datasets
3. **Real-time Processing:** Stream video for live detection
4. **Advanced Analytics:** Temporal analysis for video consistency
5. **Model Versions:** Switch between different model architectures

## License
MIT

## Support
For issues or questions, contact: your-email@example.com
