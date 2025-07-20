#!/usr/bin/env python3
"""
Setup script for RTSP Vehicle Detection System
Academic Research Project

This script helps install dependencies and configure the system.
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    
    dependencies = [
        "opencv-python>=4.5.0",
        "ultralytics>=8.0.0",
        "numpy>=1.19.0",
        "tensorflow>=2.0.0",
        "dataclasses;python_version<'3.7'"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
            return False
    
    return True

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    modules = [
        ("cv2", "OpenCV"),
        ("ultralytics", "Ultralytics YOLO"),
        ("numpy", "NumPy"),
        ("tensorflow", "TensorFlow")
    ]
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {display_name}: {e}")
            return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = [
        "detection_output",
        "logs"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True

def test_rtsp_support():
    """Test if OpenCV supports RTSP."""
    print("🔍 Testing RTSP support...")
    
    try:
        import cv2
        # Try to create a VideoCapture object (this tests RTSP support)
        cap = cv2.VideoCapture()
        cap.release()
        print("✅ OpenCV RTSP support available")
        return True
    except Exception as e:
        print(f"❌ RTSP support test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚗 RTSP Vehicle Detection System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed")
        return False
    
    # Test RTSP support
    if not test_rtsp_support():
        print("❌ RTSP support test failed")
        return False
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure your RTSP URL in the scripts")
    print("2. Test connection: python3 test_rtsp.py")
    print("3. Run detection: python3 run_detection.py")
    print("\n📖 For more information, see README_RTSP.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)