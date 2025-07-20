from VehicleDetectionTracker.VehicleDetectionTracker import VehicleDetectionTracker

# Choose your video source:
# Option 1: Local video file
# video_path = "path/to/your/video.mp4"

# Option 2: RTSP stream (IP camera)
video_path = "rtsp://admin:CamPassword_0718@192.168.0.101:554"

# Option 3: Webcam (usually device 0)
# video_path = 0

vehicle_detection = VehicleDetectionTracker()
result_callback = lambda result: print({
    "number_of_vehicles_detected": result["number_of_vehicles_detected"],
    "detected_vehicles": [
        {
            "vehicle_id": vehicle["vehicle_id"],
            "vehicle_type": vehicle["vehicle_type"],
            "detection_confidence": vehicle["detection_confidence"],
            "color_info": vehicle["color_info"],
            "model_info": vehicle["model_info"],
            "speed_info": vehicle["speed_info"]
        }
        for vehicle in result['detected_vehicles']
    ]
})
vehicle_detection.process_video(video_path, result_callback = result_callback)
