"""
Face Extractor Diagnostic - Check face detection status
Run this to verify face detection is working properly
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.face_extractor import FaceExtractor
from utils.logger import get_logger

logger = get_logger(__name__)

def diagnose_face_detection():
    """Diagnose face detection initialization"""
    
    print("\n" + "="*70)
    print("FACE EXTRACTOR DIAGNOSTIC")
    print("="*70)
    
    print("\n1️⃣  Initializing FaceExtractor...")
    try:
        face_extractor = FaceExtractor()
        print("   ✓ FaceExtractor initialized")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return False
    
    print("\n2️⃣  Checking detection methods...")
    status = face_extractor.get_status()
    
    print(f"\n   Detection Method: {status['detection_method']}")
    print(f"   Available: {status['available']}")
    print(f"   MediaPipe Available: {status['mediapipe_available']}")
    print(f"   Haar Cascade Available: {status['haar_cascade_available']}")
    
    if not status['available']:
        print("\n   ✗ ERROR: No face detection method available!")
        print("\n   SOLUTION:")
        print("   ├─ Install MediaPipe (RECOMMENDED):")
        print("   │  pip install mediapipe")
        print("   │")
        print("   ├─ OR use Haar Cascade (built-in fallback)")
        print("   │  Already configured as fallback")
        print("   │")
        print("   └─ Full installation:")
        print("      pip install -r requirements.txt")
        return False
    
    print("\n   ✓ Face detection is ready!")
    
    print("\n3️⃣  Testing face detection with a sample image...")
    
    import os
    test_images = [
        "uploads/20260503_005720/image.jpg",
        "uploads/20260503_221825/image.jpg",
        "uploads/20260503_232110/image.jpg",
        "uploads/20260504_030842/image.jpg",
    ]
    
    found_test_image = None
    for img_path in test_images:
        if os.path.exists(img_path):
            found_test_image = img_path
            break
    
    if found_test_image:
        print(f"\n   Testing with: {found_test_image}")
        try:
            faces = face_extractor.extract_faces_from_image(found_test_image)
            print(f"   ✓ Extracted {len(faces)} face(s)")
            if faces:
                print(f"   ✓ Face detection working correctly!")
            else:
                print(f"   ⚠️  No faces detected in this image")
        except Exception as e:
            print(f"   ✗ Error during test: {e}")
            return False
    else:
        print("\n   ⚠️  No test images found in uploads folder")
        print("   Upload some images first, then test again")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Status: ✓ READY")
    print(f"Detection Method: {status['detection_method']}")
    print(f"MediaPipe: {'✓ Available' if status['mediapipe_available'] else '✗ Not available (using Haar Cascade fallback)'}")
    print(f"Haar Cascade: {'✓ Available as fallback' if status['haar_cascade_available'] else '✗ Not available'}")
    print("\n✓ Face detection is properly configured and ready to use!")
    print("\nYou can now:")
    print("  • Run the deepfake detection API")
    print("  • Upload images for detection")
    print("  • Upload videos for detection\n")
    
    return True


def quick_fix_guide():
    """Show quick fix options"""
    print("\n" + "="*70)
    print("QUICK FIX GUIDE")
    print("="*70)
    
    print("\nIf you're still getting 'Face detection not initialized' error:")
    print("\nOption 1: Install MediaPipe (RECOMMENDED)")
    print("  pip install mediapipe")
    print("  python test_face_extractor.py  # Then run this script again")
    
    print("\nOption 2: Full Dependencies")
    print("  pip install -r requirements.txt")
    
    print("\nOption 3: Check Logs")
    print("  Look in logs/ folder for detailed initialization messages")
    
    print("\nOption 4: Verify Installation")
    print("  python -c \"import mediapipe; print('✓ MediaPipe installed')\"")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        success = diagnose_face_detection()
        
        if not success:
            quick_fix_guide()
            sys.exit(1)
        
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Diagnostic failed: {e}")
        import traceback
        traceback.print_exc()
        quick_fix_guide()
        sys.exit(1)
