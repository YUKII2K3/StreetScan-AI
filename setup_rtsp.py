#!/usr/bin/env python3
"""
RTSP Setup Script for VehicleDetectionTracker
This script helps you configure and test your RTSP camera integration.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        ('opencv-python', 'cv2'),
        ('ultralytics', 'ultralytics'),
        ('numpy', 'numpy'),
        ('tensorflow', 'tensorflow')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip3 install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies are installed!")
    return True

def configure_rtsp_url():
    """Configure the RTSP URL interactively."""
    print("\n🔧 RTSP Configuration")
    print("=" * 40)
    
    # Default values
    default_ip = "192.168.0.101"
    default_username = "admin"
    default_password = "CamPassword_0718"
    default_port = "554"
    
    print(f"Current configuration:")
    print(f"  IP: {default_ip}")
    print(f"  Username: {default_username}")
    print(f"  Password: {default_password}")
    print(f"  Port: {default_port}")
    
    # Ask if user wants to change
    change = input("\nDo you want to modify these settings? (y/N): ").strip().lower()
    
    if change == 'y':
        ip = input(f"Enter camera IP address [{default_ip}]: ").strip() or default_ip
        username = input(f"Enter username [{default_username}]: ").strip() or default_username
        password = input(f"Enter password [{default_password}]: ").strip() or default_password
        port = input(f"Enter port [{default_port}]: ").strip() or default_port
    else:
        ip, username, password, port = default_ip, default_username, default_password, default_port
    
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}"
    
    print(f"\n📡 RTSP URL: {rtsp_url}")
    return rtsp_url

def update_example_files(rtsp_url):
    """Update example files with the configured RTSP URL."""
    print("\n📝 Updating example files...")
    
    files_to_update = [
        'examples/RTSPTrackerTest.py',
        'examples/AdvancedRTSPTracker.py',
        'test_rtsp_connection.py'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace the RTSP URL
                old_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
                content = content.replace(old_url, rtsp_url)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                print(f"✅ Updated {file_path}")
            except Exception as e:
                print(f"❌ Failed to update {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")

def run_connection_test(rtsp_url):
    """Run the RTSP connection test."""
    print(f"\n🧪 Testing RTSP connection...")
    print(f"URL: {rtsp_url}")
    
    try:
        result = subprocess.run([
            sys.executable, 'test_rtsp_connection.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Connection test completed successfully!")
            print("You can now run the vehicle detection system.")
            return True
        else:
            print("❌ Connection test failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Connection test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running connection test: {e}")
        return False

def show_next_steps():
    """Show the next steps to run the vehicle detection system."""
    print("\n🎯 Next Steps")
    print("=" * 40)
    print("1. Test RTSP connection:")
    print("   python3 test_rtsp_connection.py")
    print()
    print("2. Run simple vehicle detection:")
    print("   python3 examples/RTSPTrackerTest.py")
    print()
    print("3. Run advanced vehicle detection (recommended):")
    print("   python3 examples/AdvancedRTSPTracker.py")
    print()
    print("4. View the integration guide:")
    print("   cat RTSP_INTEGRATION_GUIDE.md")
    print()
    print("💡 Tips:")
    print("- Press 'q' to quit the vehicle detection system")
    print("- Press 's' to save frames (in advanced mode)")
    print("- Check the logs for detection results")

def main():
    """Main setup function."""
    print("🚗 VehicleDetectionTracker - RTSP Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first.")
        return
    
    # Configure RTSP URL
    rtsp_url = configure_rtsp_url()
    
    # Update example files
    update_example_files(rtsp_url)
    
    # Ask if user wants to test connection
    test_connection = input("\nDo you want to test the RTSP connection now? (Y/n): ").strip().lower()
    
    if test_connection != 'n':
        success = run_connection_test(rtsp_url)
        if not success:
            print("\n💡 Troubleshooting tips:")
            print("1. Check if the camera IP is correct")
            print("2. Verify username and password")
            print("3. Ensure the camera is on the same network")
            print("4. Try accessing the camera's web interface first")
            print("5. Check if RTSP is enabled on the camera")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main() 