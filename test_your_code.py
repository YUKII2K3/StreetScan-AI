#!/usr/bin/env python3
"""
Test script using your exact YOLO detection code
"""

from ultralytics import YOLO
import cv2

# RTSP stream URL
rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.104:554/cam/realmonitor?channel=1&subtype=0"

print(f"🔍 Testing your RTSP stream: {rtsp_url}")
print("=" * 60)

# Load YOLOv8 pretrained model
print("📦 Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')  # Lightweight and fast

# Open RTSP stream
print("🔗 Opening RTSP stream...")
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("❌ Failed to open RTSP stream!")
    print("Please check:")
    print("1. Camera IP address (192.168.0.104)")
    print("2. Network connectivity")
    print("3. RTSP URL format")
    exit(1)

print("✅ RTSP stream opened successfully!")

# Get stream properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"📐 Frame size: {width}x{height}")
print(f"🎬 FPS: {fps}")
print(f"\n🚗 Starting vehicle detection...")
print("Press 'q' to quit")

frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("❌ Failed to read frame from stream")
        break

    frame_count += 1
    
    # Run detection
    results = model(frame)

    # Draw boxes and labels
    annotated_frame = results[0].plot()

    # Add frame counter
    cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Live Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"\n📊 Processed {frame_count} frames")

cap.release()
cv2.destroyAllWindows() 