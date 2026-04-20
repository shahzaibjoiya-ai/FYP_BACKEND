#!/usr/bin/env python
# """
# Setup and Installation Script for Deepfake Detection Backend

# This script helps set up the complete environment with all dependencies.
# Run this before starting the application.
# """

import os
import sys
import subprocess
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_section("Checking Python Version")
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ is required")
        sys.exit(1)
    
    print("✓ Python version is compatible")

def create_virtual_env():
    """Create virtual environment"""
    print_section("Creating Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print(f"✓ Virtual environment already exists at {venv_path}")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activation_command():
    """Get the activation command for the current OS"""
    if os.name == 'nt':  # Windows
        return r"venv\Scripts\activate"
    else:  # Linux/Mac
        return "source venv/bin/activate"

def install_dependencies():
    """Install required packages"""
    print_section("Installing Dependencies")
    
    try:
        # Determine pip command
        if os.name == 'nt':  # Windows
            pip_cmd = r"venv\Scripts\pip"
        else:  # Linux/Mac
            pip_cmd = "venv/bin/pip"
        
        print("Installing packages from requirements.txt...")
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_folders():
    """Create necessary folders"""
    print_section("Creating Directories")
    
    folders = ['models', 'uploads', 'logs']
    
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✓ {folder}/ directory created")

def verify_installation():
    """Verify that all modules can be imported"""
    print_section("Verifying Installation")
    
    required_modules = [
        'flask',
        'numpy',
        'cv2',
        'tensorflow',
        'torch',
        'mediapipe',
        'PIL',
        'sklearn',
        'scipy'
    ]
    
    failed = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed.append(module)
    
    if failed:
        print(f"\n⚠️  Failed to import: {', '.join(failed)}")
        print("Try installing these manually or check requirements.txt")
        return False
    
    print("\n✓ All modules imported successfully")
    return True

def print_next_steps():
    """Print next steps for user"""
    print_section("Next Steps")
    
    if os.name == 'nt':  # Windows
        activate_cmd = r"venv\Scripts\activate"
        run_cmd = "python main.py"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate"
        run_cmd = "python3 main.py"
    
    print(f"1. Activate virtual environment:")
    print(f"   {activate_cmd}")
    print(f"\n2. Run the application:")
    print(f"   {run_cmd}")
    print(f"\n3. API will be available at:")
    print(f"   http://localhost:5000")
    print(f"\n4. Test the API:")
    print(f"   python test_api.py")
    print(f"\n5. Update .env file with your settings if needed")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print(" Deepfake Detection Backend - Setup Script")
    print("="*60)
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    if not create_virtual_env():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Some dependencies failed to install")
        print("Try installing manually with: pip install -r requirements.txt")
    
    # Create folders
    create_folders()
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Some modules could not be imported")
        print("Try running: pip install -r requirements.txt again")
    
    # Print next steps
    print_next_steps()
    
    print(f"\n{'='*60}")
    print(" Setup Complete!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
