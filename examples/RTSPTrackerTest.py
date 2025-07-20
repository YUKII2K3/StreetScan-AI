from VehicleDetectionTracker.VehicleDetectionTracker import VehicleDetectionTracker

# RTSP stream configuration
rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"

# Initialize the vehicle detection tracker
vehicle_detection = VehicleDetectionTracker()

# Define callback function to handle detection results
def result_callback(result):
    """
    Callback function to process detection results for each frame.
    You can modify this function to handle the results as needed.
    """
    print(f"Frame processed - Vehicles detected: {result['number_of_vehicles_detected']}")
    
    # Print detailed information for each detected vehicle
    for vehicle in result['detected_vehicles']:
        print(f"  Vehicle ID: {vehicle['vehicle_id']}")
        print(f"  Type: {vehicle['vehicle_type']}")
        print(f"  Confidence: {vehicle['detection_confidence']:.3f}")
        
        # Speed information
        speed_info = vehicle['speed_info']
        if speed_info['kph'] is not None:
            print(f"  Speed: {speed_info['kph']:.1f} km/h (Reliability: {speed_info['reliability']:.1f})")
            print(f"  Direction: {speed_info['direction_label']}")
        
        # Color information
        import json
        color_info = json.loads(vehicle['color_info'])
        if color_info:
            print(f"  Color: {color_info[0]['color']} ({color_info[0]['prob']})")
        
        # Model information
        model_info = json.loads(vehicle['model_info'])
        if model_info:
            print(f"  Make/Model: {model_info[0]['make']} {model_info[0]['model']} ({model_info[0]['prob']})")
        
        print("  " + "-" * 50)

# Process the RTSP stream
print(f"Starting vehicle detection on RTSP stream: {rtsp_url}")
print("Press 'q' to quit the application")
print("=" * 60)

try:
    vehicle_detection.process_video(rtsp_url, result_callback)
except Exception as e:
    print(f"Error processing RTSP stream: {e}")
    print("Please check:")
    print("1. Camera IP address is correct")
    print("2. Username and password are correct")
    print("3. Camera is accessible on the network")
    print("4. RTSP port (554) is open") 