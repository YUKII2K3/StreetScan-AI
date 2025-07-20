# 🚗 RTSP Vehicle Detection System

**Academic Research Project** - Real-time vehicle detection using RTSP streams with YOLOv8, ByteTrack, and MobileNet for make, model, and color recognition.

## 📋 Overview

This system provides real-time vehicle detection and analysis using IP camera RTSP streams. It combines multiple AI models for comprehensive vehicle analysis:

- **YOLOv8** - Vehicle detection and tracking
- **ByteTrack** - Persistent vehicle tracking across frames
- **MobileNet** - Vehicle make, model, and color recognition
- **RTSP Manager** - Robust stream handling with automatic reconnection

## 🏗️ Architecture

```
rtsp_detection/
├── __init__.py              # Package initialization
├── rtsp_manager.py          # RTSP connection management
├── connection_tester.py     # Connection testing and diagnostics
└── detection_pipeline.py    # Main detection pipeline

Scripts:
├── test_rtsp.py            # Test RTSP connection
└── run_detection.py        # Run complete detection system
```

## 🚀 Quick Start

### 1. Test RTSP Connection
First, verify your RTSP stream is accessible:

```bash
python3 test_rtsp.py
```

This will:
- Test connection to your IP camera
- Display stream properties (resolution, FPS)
- Run performance benchmarks
- Provide optimization recommendations
- Save detailed test report

### 2. Run Vehicle Detection
Start the complete detection pipeline:

```bash
python3 run_detection.py
```

**Advanced usage with options:**
```bash
# Save detection results and frames
python3 run_detection.py --save-detections --save-frames

# Limit FPS for performance
python3 run_detection.py --max-fps 15

# Disable live window (headless mode)
python3 run_detection.py --no-window

# Custom RTSP URL
python3 run_detection.py --rtsp-url "rtsp://user:pass@192.168.1.100:554"
```

## ⚙️ Configuration

### RTSP URL Format
```
rtsp://username:password@ip_address:port
```

**Your default configuration:**
```
rtsp://admin:CamPassword_0718@192.168.0.101:554
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--rtsp-url` | RTSP stream URL | Your camera URL |
| `--max-retries` | Connection retry attempts | 3 |
| `--retry-delay` | Delay between retries (seconds) | 5 |
| `--no-window` | Disable live window display | False |
| `--save-detections` | Save detection results to files | False |
| `--save-frames` | Save frames with detections | False |
| `--output-dir` | Output directory for saved files | `detection_output` |
| `--max-fps` | Maximum FPS (performance control) | Unlimited |
| `--no-logging` | Disable console logging | False |

## 🔍 What the System Detects

For each vehicle, you get comprehensive information:

- **Vehicle Type**: car, truck, bus, motorcycle, etc.
- **Color**: Black, White, Red, Blue, Silver, etc.
- **Make/Model**: Toyota Camry, Ford Mustang, Honda Civic, etc.
- **Speed**: Calculated in km/h with reliability score
- **Direction**: Movement direction (8 cardinal directions)
- **Confidence**: Detection accuracy score
- **Tracking ID**: Persistent vehicle ID across frames

## 📊 Sample Output

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
  ]
}
```

## 🎮 Controls

When running the detection system:

- **'q'**: Quit the application
- **Ctrl+C**: Interrupt and cleanup

## 🛠️ Troubleshooting

### Connection Issues

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
- Use `--max-fps` to limit processing

### RTSP URL Variations

Different cameras may use different RTSP URL formats:

```bash
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

## 📁 Output Files

When saving is enabled, the system creates:

```
detection_output/
├── detection_results_20241201_143022.json  # Detection results
├── frame_20241201_143022.jpg               # Saved frames
└── rtsp_test_report.json                   # Connection test report
```

## 🔧 Pre-trained Models

The system uses these pre-trained models:

- **YOLOv8n.pt** - Vehicle detection (loaded from Ultralytics)
- **Car Make/Model Classifier** - `VehicleDetectionTracker/data/model-weights-spectrico-mmr-mobilenet-128x128-344FF72B.pb`
- **Car Color Classifier** - `VehicleDetectionTracker/data/model-weights-spectrico-car-colors-mobilenet-224x224-052EAC82.pb`

## 💡 Performance Tips

1. **Network**: Use wired connection for better stability
2. **Camera Settings**: Lower resolution for higher FPS
3. **Hardware**: GPU acceleration improves performance significantly
4. **Stream Quality**: Balance between quality and performance
5. **FPS Limiting**: Use `--max-fps` to control processing load

## 🔍 Advanced Usage

### Custom Callback Functions

You can create custom callback functions for additional processing:

```python
from rtsp_detection.detection_pipeline import DetectionPipeline, DetectionConfig
from rtsp_detection.rtsp_manager import RTSPConfig

def my_callback(detection_result):
    """Custom callback for detection results."""
    vehicle_count = detection_result.detection_results.get('number_of_vehicles_detected', 0)
    if vehicle_count > 0:
        # Save to database
        # Send alerts
        # Trigger other systems
        print(f"Detected {vehicle_count} vehicles!")

# Create pipeline
rtsp_config = RTSPConfig(url="rtsp://admin:pass@192.168.0.101:554")
detection_config = DetectionConfig(save_detections=True)
pipeline = DetectionPipeline(rtsp_config, detection_config)

# Start with custom callback
pipeline.start_detection(my_callback)
```

### Programmatic Usage

```python
from rtsp_detection import RTSPManager, DetectionPipeline, RTSPConnectionTester
from rtsp_detection.rtsp_manager import RTSPConfig
from rtsp_detection.detection_pipeline import DetectionConfig

# Test connection first
tester = RTSPConnectionTester("rtsp://admin:pass@192.168.0.101:554")
result = tester.test_connection()

if result.success:
    # Run detection
    rtsp_config = RTSPConfig(url="rtsp://admin:pass@192.168.0.101:554")
    detection_config = DetectionConfig(save_detections=True)
    pipeline = DetectionPipeline(rtsp_config, detection_config)
    pipeline.start_detection()
```

## 📈 Monitoring and Logging

The system provides comprehensive monitoring:

- **Real-time FPS**: Displayed on video window
- **Processing time**: Per-frame processing statistics
- **Connection status**: Automatic reconnection handling
- **Performance metrics**: Detailed performance analysis
- **Error logging**: Comprehensive error reporting

## 🔒 Security Notes

- RTSP credentials are passed in the URL (consider using environment variables)
- Ensure your camera network is properly secured
- Use HTTPS/secure connections when possible
- Regularly update camera firmware

## 📝 Academic Use

This system is designed for academic research purposes. It provides:

- **Modular architecture** for easy modification
- **Comprehensive logging** for research analysis
- **Configurable parameters** for experimentation
- **Performance metrics** for system evaluation
- **Extensible design** for additional features

## 🚀 Getting Started Checklist

- [ ] Install dependencies: `pip3 install opencv-python ultralytics numpy tensorflow`
- [ ] Configure your RTSP URL in the scripts
- [ ] Test connection: `python3 test_rtsp.py`
- [ ] Run detection: `python3 run_detection.py`
- [ ] Check output files in `detection_output/` directory

## 📞 Support

For academic research support:
- Check the troubleshooting section above
- Review the test reports for performance insights
- Examine the detailed logs for debugging
- Consider network and hardware requirements

---

**Author**: Academic Research Team  
**License**: MIT  
**Version**: 1.0.0 