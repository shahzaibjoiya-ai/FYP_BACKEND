# Deepfake Detection Backend - Complete Installation Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Server](#running-the-server)
5. [Testing the API](#testing-the-api)
6. [Troubleshooting](#troubleshooting)
7. [Next.js Frontend Integration](#nextjs-frontend-integration)

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 8GB (16GB+ recommended for video processing)
- **Disk Space**: 10GB (for models and uploads)
- **GPU** (Optional but recommended): NVIDIA GPU with CUDA support for faster processing

### Recommended Setup
- Python 3.10+
- 16GB+ RAM
- SSD with at least 20GB free space
- NVIDIA GPU (RTX 2080 or better)
- Internet connection for downloading pre-trained models

## 💻 Installation Steps

### Step 1: Install Python

#### On Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### On macOS
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

#### On Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Verify
python3 --version
```

### Step 2: Clone or Download the Project

```bash
cd Desktop
# Either clone from git or extract the BACKEND folder
cd BACKEND
```

### Step 3: Run Setup Script

#### On Windows (Easiest)
Double-click `setup.bat` or run:
```bash
setup.bat
```

#### On macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

#### Alternative: Manual Setup (All Platforms)

1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create directories:
   ```bash
   mkdir models uploads logs
   ```

### Step 4: Verify Installation

Run the verification script:
```bash
# Activate venv first if not already activated
python setup.py
```

Or test imports manually:
```bash
python -c "import flask, tensorflow, torch, mediapipe, cv2; print('All imports successful!')"
```

## ⚙️ Configuration

### Environment Variables (.env)

Edit the `.env` file to customize settings:

```env
# Flask settings
FLASK_ENV=development          # development or production
DEBUG=True                     # Set to False in production

# File settings
MAX_FILE_SIZE=52428800        # 50MB in bytes
UPLOAD_FOLDER=uploads          # Folder for temporary uploads
MODEL_PATH=models              # Folder for storing models

# Allowed file formats
ALLOWED_EXTENSIONS=jpg,jpeg,png,mp4,avi,mov,mkv

# Detection settings
CONFIDENCE_THRESHOLD=0.5       # 0-1, higher = more confident fake classification

# CORS settings (for frontend access)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Model settings
DEEPFAKE_MODEL_TYPE=efficientnet  # Options: efficientnet, xception, resnet50, etc.
```

### Common Configurations

**For Production:**
```env
FLASK_ENV=production
DEBUG=False
MAX_FILE_SIZE=104857600  # 100MB
CONFIDENCE_THRESHOLD=0.7
```

**For Development:**
```env
FLASK_ENV=development
DEBUG=True
MAX_FILE_SIZE=52428800   # 50MB
CONFIDENCE_THRESHOLD=0.5
```

**For GPU Acceleration:**
Ensure CUDA is installed and TensorFlow/PyTorch can detect your GPU:
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## 🚀 Running the Server

### Basic Startup

1. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. Run the server:
   ```bash
   python main.py
   ```

3. You should see:
   ```
   ==================================================
   Deepfake Detection Backend Starting
   ==================================================
   Environment: development
   Debug: True
   Max file size: 50.0MB
   Model type: efficientnet
   Confidence threshold: 0.5
   Starting server on http://0.0.0.0:5000
   ==================================================
   ```

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 "app:create_app()"
```

### Using Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t deepfake-detector .
docker run -p 5000:5000 deepfake-detector
```

## 🧪 Testing the API

### Using Python Script

```bash
python test_api.py
```

### Using cURL

**Test Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Test Image Detection:**
```bash
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:5000/api/detect-image
```

**Test Video Detection:**
```bash
curl -X POST -F "file=@/path/to/video.mp4" http://localhost:5000/api/detect-video?sample_rate=5
```

### Using Postman

1. Download [Postman](https://www.postman.com/downloads/)
2. Create new request:
   - Method: POST
   - URL: `http://localhost:5000/api/detect-image`
   - Body: form-data → file → select image
   - Send

### Using Python Requests

```python
import requests

# Image detection
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/detect-image', files=files)
    print(response.json())

# Video detection
with open('video.mp4', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/detect-video?sample_rate=5', files=files)
    print(response.json())
```

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Make sure venv is activated
pip install -r requirements.txt
```

### Issue: "No module named 'mediapipe'"

**Solution:**
```bash
pip install mediapipe
```

### Issue: CUDA/GPU not detected by TensorFlow

**Solution:**
```bash
# Check if GPU is available
python -c "import tensorflow as tf; print(len(tf.config.list_physical_devices('GPU')))"

# Install GPU support
pip install tensorflow[and-cuda]
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Change port in app.py or environment, or kill existing process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

### Issue: Very slow processing

**Solutions:**
1. Check if GPU is being used:
   ```bash
   python -c "import tensorflow as tf; print(tf.test.is_built_with_cuda())"
   ```
2. Increase `sample_rate` parameter for videos (e.g., ?sample_rate=10)
3. Reduce input resolution in preprocessor
4. Use lighter model: change `DEEPFAKE_MODEL_TYPE=mesonet` in `.env`

### Issue: "Out of memory" error

**Solutions:**
1. Reduce `MAX_FILE_SIZE` in `.env`
2. Increase `sample_rate` for videos
3. Reduce batch size in deepfake_detector.py
4. Close other applications

### Issue: CORS error from frontend

**Solution:**
Update `CORS_ORIGINS` in `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://yourdomain.com
```

### Issue: No faces detected

**Solutions:**
1. Ensure image/video has clear faces
2. Try with `sample_rate=2` or 3 for videos
3. Check image quality and lighting
4. Ensure faces are not too small or too large in frame

## 🔗 Next.js Frontend Integration

### Backend URL

Update your Next.js environment variables:

**.env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### Example API Call

```javascript
// lib/deepfakeAPI.js
export async function detectImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/detect-image`,
        {
            method: 'POST',
            body: formData,
        }
    );

    if (!response.ok) {
        throw new Error('Detection failed');
    }

    return await response.json();
}

export async function detectVideo(file, sampleRate = 5) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/detect-video?sample_rate=${sampleRate}`,
        {
            method: 'POST',
            body: formData,
        }
    );

    if (!response.ok) {
        throw new Error('Detection failed');
    }

    return await response.json();
}
```

### Example React Component

```javascript
'use client';

import { useState } from 'react';
import { detectImage } from '@/lib/deepfakeAPI';

export default function DeepfakeDetector() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        try {
            const data = await detectImage(file);
            setResult(data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                    accept="image/*"
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Analyzing...' : 'Detect'}
                </button>
            </form>

            {result && (
                <div>
                    <p>Real: {(result.real_probability * 100).toFixed(2)}%</p>
                    <p>Fake: {(result.fake_probability * 100).toFixed(2)}%</p>
                </div>
            )}
        </div>
    );
}
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/docs)
- [MediaPipe Documentation](https://mediapipe.dev/)
- [Next.js Documentation](https://nextjs.org/docs)

## 🆘 Getting Help

1. Check [README.md](README.md) for API documentation
2. Check [NEXTJS_INTEGRATION.md](NEXTJS_INTEGRATION.md) for frontend integration examples
3. Review logs in `logs/` directory
4. Run `python test_api.py` for diagnostic information

---

**Last Updated**: 2024
**Version**: 1.0.0
