#!/usr/bin/env python
"""
Test script for Deepfake Detection API

This script tests all endpoints of the API locally.
"""

import requests
import json
import os
from pathlib import Path

API_URL = "http://localhost:5000"

def print_response(response, title):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/health")
        print_response(response, "Health Check")
    except Exception as e:
        print(f"Error: {e}")

def test_model_info():
    """Test model info endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/model-info")
        print_response(response, "Model Information")
    except Exception as e:
        print(f"Error: {e}")

def test_detect_image(image_path):
    """Test image detection endpoint"""
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/api/detect-image", files=files)
            print_response(response, f"Image Detection: {Path(image_path).name}")
    except Exception as e:
        print(f"Error: {e}")

def test_detect_video(video_path, sample_rate=5):
    """Test video detection endpoint"""
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return
    
    try:
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_URL}/api/detect-video?sample_rate={sample_rate}", 
                files=files
            )
            print_response(response, f"Video Detection: {Path(video_path).name}")
    except Exception as e:
        print(f"Error: {e}")

def test_about():
    """Test about endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/info/about")
        print_response(response, "API About")
    except Exception as e:
        print(f"Error: {e}")

def test_stats():
    """Test stats endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/info/stats")
        print_response(response, "API Stats")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("Deepfake Detection API - Test Suite")
    print(f"{'='*60}")
    
    # Test basic endpoints
    test_health_check()
    test_about()
    test_stats()
    test_model_info()
    
    # Test with sample files (if available)
    sample_image = "uploads/sample_image.jpg"
    sample_video = "uploads/sample_video.mp4"
    
    if os.path.exists(sample_image):
        test_detect_image(sample_image)
    else:
        print(f"\nSample image not found: {sample_image}")
        print("To test image detection, provide a test image.")
    
    if os.path.exists(sample_video):
        test_detect_video(sample_video)
    else:
        print(f"\nSample video not found: {sample_video}")
        print("To test video detection, provide a test video.")
    
    print(f"\n{'='*60}")
    print("Test suite completed!")
    print(f"{'='*60}\n")
