# Quick Start Guide - 5 Minutes to Running

## Windows Users

### Step 1: Open Command Prompt or PowerShell
Navigate to your BACKEND folder:
```bash
cd Desktop\BACKEND
```

### Step 2: Run Setup (Auto-installs everything)
```bash
setup.bat
```

### Step 3: Activate & Run
```bash
venv\Scripts\activate
python main.py
```

✅ **Server is running!** Visit http://localhost:5000/api/health

---

## macOS/Linux Users

### Step 1: Open Terminal
Navigate to your BACKEND folder:
```bash
cd ~/Desktop/BACKEND
```

### Step 2: Run Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Activate & Run
```bash
source venv/bin/activate
python main.py
```

✅ **Server is running!** Visit http://localhost:5000/api/health

---

## Testing Immediately

### Option A: Use Python Script
```bash
python test_api.py
```

### Option B: Use cURL
```bash
# Health check
curl http://localhost:5000/api/health

# Get model info
curl http://localhost:5000/api/model-info
```

### Option C: Upload a Test Image
```bash
curl -X POST -F "file=@test_image.jpg" http://localhost:5000/api/detect-image
```

---

## Connect to Next.js Frontend

In your Next.js project, use this API URL:

```javascript
const API_URL = 'http://localhost:5000/api';

// Detect image
const detectImage = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_URL}/detect-image`, {
        method: 'POST',
        body: formData,
    });
    
    return await response.json();
};
```

---

## API Endpoints (Quick Reference)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check if API is running |
| `/api/model-info` | GET | Get model configuration |
| `/api/detect-image` | POST | Detect deepfake in image |
| `/api/detect-video` | POST | Detect deepfake in video |
| `/api/info/about` | GET | API information |

---

## Response Example

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

---

## Troubleshooting Quick Fixes

### Python not found?
- Windows: Install Python from python.org and check "Add to PATH"
- macOS: `brew install python3`
- Linux: `sudo apt install python3`

### Module not found?
```bash
pip install -r requirements.txt
```

### Port 5000 already in use?
Change port in `.env`:
```env
FLASK_PORT=5001
```

### GPU not working?
It's optional! CPU works fine, just slower. Check logs for details.

---

## Next Steps

1. **Read the full docs**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
2. **Frontend integration**: [NEXTJS_INTEGRATION.md](NEXTJS_INTEGRATION.md)
3. **API Reference**: [README.md](README.md)
4. **Configuration**: Edit `.env` file

---

## Keeping Server Running

### In Development
```bash
python main.py
```
(Runs in foreground, Ctrl+C to stop)

### In Production
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 "app:create_app()"
```

### As Background Service (Linux)
```bash
nohup python main.py > server.log 2>&1 &
```

---

**Done!** Your deepfake detection backend is ready! 🎉
