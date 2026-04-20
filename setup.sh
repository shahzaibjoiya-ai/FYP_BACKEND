#!/bin/bash
# Setup script for Deepfake Detection Backend

echo "======================================================"
echo "Deepfake Detection Backend - Setup"
echo "======================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python version:"
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p models
mkdir -p uploads
mkdir -p logs

echo ""
echo "======================================================"
echo "Setup completed successfully!"
echo "======================================================"
echo ""
echo "To run the backend, activate the virtual environment and execute:"
echo "  python main.py"
echo ""
echo "The API will be available at http://localhost:5000"
echo "======================================================"
