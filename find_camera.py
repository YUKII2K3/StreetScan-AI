#!/usr/bin/env python3
"""
Camera IP Finder
Scan network to find camera IP addresses.

Usage:
    python3 find_camera.py

Author: Academic Research Team
"""

import subprocess
import socket
import threading
import time

def ping_host(ip):
    """Ping a host and return True if reachable."""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def test_rtsp_port(ip, port=554):
    """Test if RTSP port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_network():
    """Scan the network for potential cameras."""
    print("🔍 Scanning network for cameras...")
    print("=" * 50)
    
    # Your network range
    base_ip = "192.168.0"
    reachable_hosts = []
    
    print("Scanning IP addresses...")
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        
        # Skip your own IP
        if ip == "192.168.0.103":
            continue
            
        if ping_host(ip):
            rtsp_open = test_rtsp_port(ip, 554)
            rtsp_alt_open = test_rtsp_port(ip, 8554)
            
            status = []
            if rtsp_open:
                status.append("RTSP:554")
            if rtsp_alt_open:
                status.append("RTSP:8554")
            
            reachable_hosts.append((ip, status))
            print(f"✅ {ip} - {' '.join(status) if status else 'No RTSP'}")
    
    return reachable_hosts

def test_rtsp_urls(hosts):
    """Test RTSP URLs for reachable hosts."""
    print("\n🔍 Testing RTSP connections...")
    print("=" * 50)
    
    test_urls = [
        "rtsp://admin:CamPassword_0718@{ip}:554",
        "rtsp://admin:CamPassword_0718@{ip}:8554",
        "rtsp://admin:CamPassword_0718@{ip}:554/stream1",
        "rtsp://admin:CamPassword_0718@{ip}:554/h264Preview_01_main",
        "rtsp://admin:admin@{ip}:554",
        "rtsp://admin:password@{ip}:554",
    ]
    
    working_urls = []
    
    for ip, ports in hosts:
        for url_template in test_urls:
            url = url_template.format(ip=ip)
            
            try:
                import cv2
                cap = cv2.VideoCapture(url)
                if cap.isOpened():
                    # Try to read a frame
                    ret, frame = cap.read()
                    cap.release()
                    
                    if ret and frame is not None:
                        working_urls.append(url)
                        print(f"✅ WORKING: {url}")
                        print(f"   Frame size: {frame.shape[1]}x{frame.shape[0]}")
                    else:
                        print(f"⚠️  Connected but no frames: {url}")
                else:
                    print(f"❌ Failed: {url}")
                    
            except Exception as e:
                print(f"❌ Error: {url} - {str(e)[:50]}")
    
    return working_urls

def main():
    """Main function."""
    print("🚗 Camera IP Finder")
    print("=" * 50)
    
    # Scan network
    hosts = scan_network()
    
    if not hosts:
        print("❌ No reachable hosts found on the network!")
        print("\n💡 Check:")
        print("1. Camera is powered on")
        print("2. Camera is connected to the network")
        print("3. Camera is on the same network as your computer")
        return
    
    print(f"\n📊 Found {len(hosts)} reachable hosts")
    
    # Test RTSP URLs
    working_urls = test_rtsp_urls(hosts)
    
    if working_urls:
        print(f"\n🎉 Found {len(working_urls)} working RTSP streams!")
        print("\n📋 Working URLs:")
        for url in working_urls:
            print(f"   {url}")
        
        print(f"\n🚀 To test a working stream:")
        print(f"   python3 test_camera.py '{working_urls[0]}'")
        
        print(f"\n🚗 To run vehicle detection:")
        print(f"   python3 run_simple_detection.py --rtsp-url '{working_urls[0]}'")
    else:
        print("\n❌ No working RTSP streams found!")
        print("\n💡 Possible issues:")
        print("1. Camera RTSP is disabled")
        print("2. Wrong username/password")
        print("3. Different RTSP URL format")
        print("4. Camera requires different authentication")

if __name__ == "__main__":
    main() 