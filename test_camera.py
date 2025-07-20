#!/usr/bin/env python3
"""
Simple Camera Test Script
Test RTSP connection and display video stream.

Usage:
    python3 test_camera.py [rtsp_url]

Author: Academic Research Team
"""

import cv2
import sys
import time

def test_rtsp_stream(rtsp_url):
    """Test RTSP stream and display video."""
    print(f"🔍 Testing RTSP stream: {rtsp_url}")
    print("=" * 60)
    
    # Try to open the stream
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print("❌ Failed to open RTSP stream!")
        print("\nPossible issues:")
        print("1. Camera IP address is incorrect")
        print("2. Username or password is wrong")
        print("3. Camera is not accessible on the network")
        print("4. RTSP port (554) is blocked")
        print("5. Camera requires different authentication")
        return False
    
    print("✅ RTSP stream opened successfully!")
    
    # Get stream properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"📐 Frame size: {width}x{height}")
    print(f"🎬 FPS: {fps}")
    print(f"\n📹 Displaying video stream...")
    print("Press 'q' to quit")
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret or frame is None:
                print("❌ Failed to read frame from stream")
                break
            
            frame_count += 1
            
            # Calculate FPS
            elapsed_time = time.time() - start_time
            current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            # Add FPS text to frame
            cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Frames: {frame_count}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Size: {width}x{height}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow("RTSP Stream Test", frame)
            
            # Check for 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Calculate final statistics
    total_time = time.time() - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    print(f"\n📊 Test Results:")
    print(f"   Frames received: {frame_count}")
    print(f"   Time elapsed: {total_time:.1f} seconds")
    print(f"   Average FPS: {avg_fps:.1f}")
    
    if frame_count > 0:
        print("✅ RTSP stream is working correctly!")
        return True
    else:
        print("❌ No frames were received from the stream.")
        return False

def main():
    """Main function."""
    # Updated RTSP URL with correct camera path
    default_url = "rtsp://admin:CamPassword_0718@192.168.0.104:554/cam/realmonitor?channel=1&subtype=0"
    
    # Use command line argument if provided
    rtsp_url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    print("🚗 RTSP Camera Test")
    print("=" * 50)
    
    success = test_rtsp_stream(rtsp_url)
    
    if success:
        print("\n🎉 Camera test successful!")
        print("You can now run the vehicle detection system.")
    else:
        print("\n💡 Troubleshooting tips:")
        print("1. Check if the camera IP is correct")
        print("2. Verify username and password")
        print("3. Ensure the camera is on the same network")
        print("4. Try accessing the camera's web interface first")
        print("5. Check if RTSP is enabled on the camera")
        print("6. Try different RTSP URL formats:")
        print("   - rtsp://admin:pass@192.168.0.104:554/cam/realmonitor?channel=1&subtype=0")
        print("   - rtsp://admin:pass@192.168.0.104:554/stream1")
        print("   - rtsp://admin:pass@192.168.0.104:8554")

if __name__ == "__main__":
    main() 