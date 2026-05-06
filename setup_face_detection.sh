#!/usr/bin/env bash
# QUICK SETUP SCRIPT - Face Detection Fix
# Run this to fix the "Face detection not initialized" error

set -e

echo "=========================================="
echo "Face Detection Initialization Fix"
echo "=========================================="
echo ""

# Check Python
echo "1️⃣  Checking Python installation..."
python --version || {
    echo "❌ Python not found"
    exit 1
}
echo "✓ Python found"
echo ""

# Check if MediaPipe is installed
echo "2️⃣  Checking for MediaPipe..."
if python -c "import mediapipe" 2>/dev/null; then
    echo "✓ MediaPipe already installed"
    METHOD="mediapipe"
else
    echo "⚠️  MediaPipe not installed"
    echo ""
    echo "Choose installation method:"
    echo "  a) Install MediaPipe (recommended)"
    echo "  b) Use built-in Haar Cascade fallback"
    echo "  c) Install all dependencies (full setup)"
    echo ""
    read -p "Enter choice (a/b/c): " choice
    
    case $choice in
        a)
            echo ""
            echo "Installing MediaPipe..."
            pip install mediapipe
            echo "✓ MediaPipe installed"
            METHOD="mediapipe"
            ;;
        b)
            echo ""
            echo "Using built-in Haar Cascade (no installation needed)"
            echo "✓ Face detection will use Haar Cascade fallback"
            METHOD="haar_cascade"
            ;;
        c)
            echo ""
            echo "Installing all dependencies..."
            pip install -r requirements.txt
            echo "✓ All dependencies installed"
            METHOD="mediapipe"
            ;;
        *)
            echo "Invalid choice"
            exit 1
            ;;
    esac
fi
echo ""

# Run diagnostic
echo "3️⃣  Running diagnostic..."
echo ""
python test_face_extractor.py
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Detection method: $METHOD"
echo ""
echo "You can now:"
echo "  • Run the API: python main.py"
echo "  • Test detection: curl -X POST http://localhost:5000/api/detect-image -F \"file=@image.jpg\""
echo ""
