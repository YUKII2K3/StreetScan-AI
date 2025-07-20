#!/usr/bin/env python3
"""
Simple RTSP connection test script.
Use this to verify your IP camera connection before running the full vehicle detection system.
"""

import cv2
import time

def test_rtsp_connection(rtsp_url, timeout=10):
    """
    Test RTSP connection and display basic stream information.
    
    Args:
        rtsp_url (str): RTSP stream URL
        timeout (int): Timeout in seconds for connection test
    """
    print(f"🔍 Testing RTSP connection to: {rtsp_url}")
    print("=" * 60)
    
    # Open the RTSP stream
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
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"📐 Frame size: {width}x{height}")
    print(f"🎬 FPS: {fps}")
    print(f"📊 Total frames: {frame_count if frame_count > 0 else 'Live stream'}")
    
    # Try to read frames for a few seconds
    print(f"\n📹 Testing frame capture for {timeout} seconds...")
    print("Press 'q' to quit early")
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while time.time() - start_time < timeout:
            ret, frame = cap.read()
            
            if not ret or frame is None:
                print("❌ Failed to read frame from stream")
                break
            
            frame_count += 1
            
            # Display the frame
            cv2.imshow("RTSP Stream Test", frame)
            
            # Calculate and display current FPS
            elapsed_time = time.time() - start_time
            current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            # Add FPS text to frame
            cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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
    print(f"   Frames captured: {frame_count}")
    print(f"   Time elapsed: {total_time:.1f} seconds")
    print(f"   Average FPS: {avg_fps:.1f}")
    
    if frame_count > 0:
        print("✅ RTSP stream is working correctly!")
        print("   You can now run the vehicle detection system.")
        return True
    else:
        print("❌ No frames were captured from the stream.")
        return False

if __name__ == "__main__":
    # Your RTSP URL
    rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
    
    # Test the connection
    success = test_rtsp_connection(rtsp_url, timeout=10)
    
    if success:
        print("\n🎉 RTSP connection test passed!")
        print("You can now run:")
        print("   python examples/RTSPTrackerTest.py")
        print("   python examples/AdvancedRTSPTracker.py")
    else:
        print("\n💡 Troubleshooting tips:")
        print("1. Check if the camera IP is correct")
        print("2. Verify username and password")
        print("3. Ensure the camera is on the same network")
        print("4. Try accessing the camera's web interface first")
        print("5. Check if RTSP is enabled on the camera") 