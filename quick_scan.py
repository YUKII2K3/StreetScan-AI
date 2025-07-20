#!/usr/bin/env python3
"""
Quick Network Scanner
Fast scan to find camera IP addresses.

Author: Academic Research Team
"""

import subprocess
import socket
import threading
import time

def quick_ping(ip):
    """Quick ping test."""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                              capture_output=True, text=True, timeout=3)
        return result.returncode == 0
    except:
        return False

def test_rtsp_connection(ip, credentials):
    """Test RTSP connection with different credentials."""
    import cv2
    
    test_urls = [
        f"rtsp://{credentials}@{ip}:554",
        f"rtsp://{credentials}@{ip}:8554",
        f"rtsp://{credentials}@{ip}:554/stream1",
        f"rtsp://{credentials}@{ip}:554/h264Preview_01_main",
        f"rtsp://{credentials}@{ip}:554/live",
        f"rtsp://{credentials}@{ip}:554/av0_0",
    ]
    
    for url in test_urls:
        try:
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    return url, frame.shape
        except:
            continue
    
    return None, None

def main():
    """Main function."""
    print("🔍 Quick Network Scan for Camera")
    print("=" * 50)
    
    # Common camera IP ranges
    ip_ranges = [
        "192.168.0",
        "192.168.1", 
        "10.0.0",
        "10.0.1"
    ]
    
    # Common credentials
    credentials_list = [
        "admin:CamPassword_0718",
        "admin:admin",
        "admin:password",
        "admin:123456",
        "admin:admin123",
        "root:root",
        "user:user"
    ]
    
    found_cameras = []
    
    for base_ip in ip_ranges:
        print(f"\n🔍 Scanning {base_ip}.x network...")
        
        # Quick scan of common camera IPs
        common_ips = [1, 10, 11, 12, 20, 21, 22, 50, 51, 52, 100, 101, 102, 200, 201, 202]
        
        for i in common_ips:
            ip = f"{base_ip}.{i}"
            
            # Skip your own IP
            if ip == "192.168.0.103":
                continue
                
            if quick_ping(ip):
                print(f"✅ Found device at {ip}")
                
                # Test RTSP with different credentials
                for creds in credentials_list:
                    url, frame_shape = test_rtsp_connection(ip, creds)
                    if url:
                        found_cameras.append((ip, url, frame_shape))
                        print(f"🎉 CAMERA FOUND: {url}")
                        print(f"   Frame size: {frame_shape[1]}x{frame_shape[0]}")
                        break
    
    if found_cameras:
        print(f"\n🎉 Found {len(found_cameras)} camera(s)!")
        print("\n📋 Working RTSP URLs:")
        for ip, url, shape in found_cameras:
            print(f"   {url}")
        
        print(f"\n🚀 To test the first camera:")
        print(f"   python3 test_camera.py '{found_cameras[0][1]}'")
        
        print(f"\n🚗 To run vehicle detection:")
        print(f"   python3 run_simple_detection.py --rtsp-url '{found_cameras[0][1]}'")
    else:
        print("\n❌ No cameras found!")
        print("\n💡 Troubleshooting:")
        print("1. Camera is powered off")
        print("2. Camera is not on the network")
        print("3. Camera uses different IP range")
        print("4. Camera requires different credentials")
        print("5. RTSP is disabled on camera")

if __name__ == "__main__":
    main() 