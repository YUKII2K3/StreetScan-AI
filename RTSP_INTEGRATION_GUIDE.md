# RTSP Integration Guide for VehicleDetectionTracker

This guide explains how to integrate your IP camera's RTSP stream with the VehicleDetectionTracker system.

## 🎯 Quick Start

### 1. Test Your RTSP Connection
First, verify that your RTSP stream is accessible:

```bash
python test_rtsp_connection.py
```

This will test the connection and show you the stream properties (resolution, FPS, etc.).

### 2. Run Vehicle Detection on RTSP Stream

**Simple version:**
```bash
python examples/RTSPTrackerTest.py
```

**Advanced version (with error handling):**
```bash
python examples/AdvancedRTSPTracker.py
```

## 🔧 Configuration

### RTSP URL Format
The RTSP URL follows this format:
```
rtsp://username:password@ip_address:port
```

**Your configuration:**
```
rtsp://admin:CamPassword_0718@192.168.0.101:554
```

### Supported Video Sources
The system supports multiple video input types:

1. **RTSP Streams** (IP cameras)
   ```python
   video_path = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
   ```

2. **Local Video Files**
   ```python
   video_path = "path/to/your/video.mp4"
   ```

3. **Webcams**
   ```python
   video_path = 0  # Default webcam
   ```

## 🚗 How Vehicle Detection Works

### Detection Pipeline
1. **Frame Capture**: OpenCV reads frames from your RTSP stream
2. **YOLO Detection**: YOLOv8 detects vehicles in each frame
3. **ByteTrack Tracking**: Maintains vehicle IDs across frames
4. **Vehicle Analysis**: 
   - Color classification (MobileNet)
   - Make/Model classification (MobileNet)
   - Speed calculation from tracking history
5. **Output**: JSON results with vehicle details and annotated frames

### Pre-trained Models Used
- **YOLOv8n.pt**: Main vehicle detection (loaded from Ultralytics)
- **Car Make/Model Classifier**: `data/model-weights-spectrico-mmr-mobilenet-128x128-344FF72B.pb`
- **Car Color Classifier**: `data/model-weights-spectrico-car-colors-mobilenet-224x224-052EAC82.pb`

## 📊 Output Format

The system returns detailed JSON results for each frame:

```json
{
  "number_of_vehicles_detected": 2,
  "detected_vehicles": [
    {
      "vehicle_id": 5,
      "vehicle_type": "car",
      "detection_confidence": 0.85,
      "color_info": '[{"color": "Black", "prob": "0.75"}]',
      "model_info": '[{"make": "Toyota", "model": "Camry", "prob": "0.45"}]',
      "speed_info": {
        "kph": 45.2,
        "reliability": 0.9,
        "direction_label": "Right",
        "direction": 0.15
      },
      "vehicle_coordinates": {
        "x": 320.5,
        "y": 240.2,
        "width": 80.0,
        "height": 60.0
      }
    }
  ],
  "annotated_frame_base64": "data:image/jpeg;base64,...",
  "original_frame_base64": "data:image/jpeg;base64,..."
}
```

## 🛠️ Troubleshooting

### Common RTSP Issues

**1. Connection Failed**
```
❌ Failed to open RTSP stream!
```
**Solutions:**
- Verify camera IP address
- Check username/password
- Ensure camera is on the same network
- Test camera web interface first

**2. No Frames Received**
```
❌ Failed to read frame from RTSP stream
```
**Solutions:**
- Check if RTSP is enabled on camera
- Verify port 554 is open
- Try different RTSP URL formats
- Check camera's RTSP settings

**3. Low FPS or Lag**
```
📊 FPS: 5.2
```
**Solutions:**
- Reduce stream resolution on camera
- Use wired network connection
- Check network bandwidth
- Adjust camera's encoding settings

### RTSP URL Variations
Different cameras may use different RTSP URL formats:

```python
# Standard format
rtsp://admin:password@192.168.0.101:554

# With specific stream path
rtsp://admin:password@192.168.0.101:554/stream1
rtsp://admin:password@192.168.0.101:554/h264Preview_01_main

# With different ports
rtsp://admin:password@192.168.0.101:8554
rtsp://admin:password@192.168.0.101:8080

# Without authentication (if camera allows)
rtsp://192.168.0.101:554
```

## 🔍 Advanced Features

### Custom Callback Functions
You can create custom callback functions to handle detection results:

```python
def my_callback(result):
    if result['number_of_vehicles_detected'] > 0:
        # Save to database
        # Send alerts
        # Log to file
        # etc.
        print(f"Detected {result['number_of_vehicles_detected']} vehicles")

# Use with tracker
tracker.process_stream(my_callback)
```

### Error Handling and Reconnection
The `AdvancedRTSPTracker` class includes:
- Automatic reconnection on connection loss
- Retry logic with configurable attempts
- FPS monitoring
- Frame capture and saving

### Performance Optimization
- **GPU Acceleration**: The system automatically uses GPU if available
- **Frame Skipping**: Can be implemented for higher FPS
- **Resolution Scaling**: Process lower resolution for speed

## 📝 Example Usage

### Basic RTSP Integration
```python
from VehicleDetectionTracker.VehicleDetectionTracker import VehicleDetectionTracker

# Initialize tracker
tracker = VehicleDetectionTracker()

# RTSP URL
rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"

# Process stream
tracker.process_video(rtsp_url, lambda result: print(result))
```

### Advanced RTSP Integration
```python
from examples.AdvancedRTSPTracker import AdvancedRTSPTracker

# Create advanced tracker
tracker = AdvancedRTSPTracker(
    rtsp_url="rtsp://admin:CamPassword_0718@192.168.0.101:554",
    max_retries=3,
    retry_delay=5
)

# Custom callback
def custom_callback(result):
    if result['number_of_vehicles_detected'] > 0:
        print(f"🎯 {result['number_of_vehicles_detected']} vehicle(s) detected!")

# Start processing
tracker.process_stream(custom_callback)
```

## 🎮 Controls

When running the vehicle detection system:

- **'q'**: Quit the application
- **'s'**: Save current frame as image (AdvancedRTSPTracker only)

## 📈 Performance Tips

1. **Network**: Use wired connection for better stability
2. **Camera Settings**: Lower resolution for higher FPS
3. **Hardware**: GPU acceleration improves performance significantly
4. **Stream Quality**: Balance between quality and performance

## 🔗 Related Files

- `test_rtsp_connection.py` - Test RTSP connectivity
- `examples/RTSPTrackerTest.py` - Simple RTSP integration
- `examples/AdvancedRTSPTracker.py` - Advanced RTSP with error handling
- `VehicleDetectionTracker/VehicleDetectionTracker.py` - Core detection system 