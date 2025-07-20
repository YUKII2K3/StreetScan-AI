# 🚗 Complete RTSP Vehicle Detection System

**Academic Research Project** - Real-time vehicle detection using RTSP streams with YOLOv8, ByteTrack, and optional MobileNet for make, model, and color recognition.

## 📋 Overview

This system provides real-time vehicle detection and analysis using IP camera RTSP streams. It offers two detection modes:

### 🎯 **Simple Detection Mode** (Recommended)
- **YOLOv8** - Vehicle detection and tracking
- **ByteTrack** - Persistent vehicle tracking across frames
- **Speed & Direction** - Real-time calculation
- **No TensorFlow dependency** - Works on all systems

### 🔍 **Full Detection Mode** (Advanced)
- All features from Simple Mode
- **MobileNet** - Vehicle make, model, and color recognition
- **TensorFlow dependency** - Requires TensorFlow installation

## 🏗️ Architecture

```
rtsp_detection/
├── __init__.py                    # Package initialization
├── rtsp_manager.py               # RTSP connection management
├── connection_tester.py          # Connection testing and diagnostics
├── simple_detection_pipeline.py  # Simple detection (no TensorFlow)
└── detection_pipeline.py         # Full detection (with TensorFlow)

Scripts:
├── test_rtsp.py                  # Test RTSP connection
├── run_simple_detection.py       # Run simple detection
└── run_detection.py              # Run full detection (if TensorFlow available)
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test RTSP Connection
```bash
python3 test_rtsp.py
```

### 3. Run Vehicle Detection

**Simple Mode (Recommended):**
```bash
python3 run_simple_detection.py
```

**Full Mode (if TensorFlow available):**
```bash
python3 run_detection.py
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
| `--confidence` | Detection confidence threshold | 0.5 |

## 🔍 What Each Mode Detects

### Simple Detection Mode
- **Vehicle Type**: car, truck, bus, motorcycle
- **Speed**: Calculated in km/h with reliability score
- **Direction**: Movement direction (8 cardinal directions)
- **Confidence**: Detection accuracy score
- **Tracking ID**: Persistent vehicle ID across frames

### Full Detection Mode
- All features from Simple Mode
- **Color**: Black, White, Red, Blue, Silver, etc.
- **Make/Model**: Toyota Camry, Ford Mustang, Honda Civic, etc.

## 📊 Sample Output

### Simple Mode Output
```json
{
  "number_of_vehicles_detected": 2,
  "detected_vehicles": [
    {
      "vehicle_id": 5,
      "vehicle_type": "car",
      "detection_confidence": 0.85,
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

### Full Mode Output
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

### TensorFlow Issues

If you encounter TensorFlow installation problems:

1. **Use Simple Mode**: `python3 run_simple_detection.py`
2. **Install TensorFlow separately**: Follow TensorFlow installation guide
3. **Use Docker**: Containerized environment with all dependencies

## 📁 Output Files

When saving is enabled, the system creates:

```
detection_output/
├── simple_detection_results_20241201_143022.json  # Simple mode results
├── detection_results_20241201_143022.json         # Full mode results
├── simple_frame_20241201_143022.jpg               # Saved frames
└── rtsp_test_report.json                          # Connection test report
```

## 🔧 Pre-trained Models

### Simple Mode
- **YOLOv8n.pt** - Vehicle detection (loaded from Ultralytics)

### Full Mode
- **YOLOv8n.pt** - Vehicle detection (loaded from Ultralytics)
- **Car Make/Model Classifier** - `VehicleDetectionTracker/data/model-weights-spectrico-mmr-mobilenet-128x128-344FF72B.pb`
- **Car Color Classifier** - `VehicleDetectionTracker/data/model-weights-spectrico-car-colors-mobilenet-224x224-052EAC82.pb`

## 💡 Performance Tips

1. **Network**: Use wired connection for better stability
2. **Camera Settings**: Lower resolution for higher FPS
3. **Hardware**: GPU acceleration improves performance significantly
4. **Stream Quality**: Balance between quality and performance
5. **FPS Limiting**: Use `--max-fps` to control processing load
6. **Confidence Threshold**: Adjust `--confidence` for detection sensitivity

## 🔍 Advanced Usage

### Custom Callback Functions

```python
from rtsp_detection.simple_detection_pipeline import SimpleDetectionPipeline, SimpleDetectionConfig
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
detection_config = SimpleDetectionConfig(save_detections=True)
pipeline = SimpleDetectionPipeline(rtsp_config, detection_config)

# Start with custom callback
pipeline.start_detection(my_callback)
```

### Programmatic Usage

```python
from rtsp_detection import RTSPManager, RTSPConnectionTester, SIMPLE_DETECTION_AVAILABLE
from rtsp_detection.rtsp_manager import RTSPConfig

# Test connection first
tester = RTSPConnectionTester("rtsp://admin:pass@192.168.0.101:554")
result = tester.test_connection()

if result.success and SIMPLE_DETECTION_AVAILABLE:
    from rtsp_detection.simple_detection_pipeline import SimpleDetectionPipeline, SimpleDetectionConfig
    
    # Run detection
    rtsp_config = RTSPConfig(url="rtsp://admin:pass@192.168.0.101:554")
    detection_config = SimpleDetectionConfig(save_detections=True)
    pipeline = SimpleDetectionPipeline(rtsp_config, detection_config)
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
- **Two detection modes** for different research needs

## 🚀 Getting Started Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Configure your RTSP URL in the scripts
- [ ] Test connection: `python3 test_rtsp.py`
- [ ] Run simple detection: `python3 run_simple_detection.py`
- [ ] (Optional) Install TensorFlow for full detection
- [ ] (Optional) Run full detection: `python3 run_detection.py`
- [ ] Check output files in `detection_output/` directory

## 📞 Support

For academic research support:
- Check the troubleshooting section above
- Review the test reports for performance insights
- Examine the detailed logs for debugging
- Consider network and hardware requirements
- Use Simple Mode if TensorFlow is not available

## 🔄 Migration Guide

### From Old System
If you were using the previous examples:

1. **Old**: `python3 examples/RTSPTrackerTest.py`
   **New**: `python3 run_simple_detection.py`

2. **Old**: `python3 examples/AdvancedRTSPTracker.py`
   **New**: `python3 run_detection.py` (if TensorFlow available)

3. **Old**: `python3 test_rtsp_connection.py`
   **New**: `python3 test_rtsp.py`

### Benefits of New System
- **Modular design** - Easy to extend and modify
- **Better error handling** - Robust connection management
- **Performance monitoring** - Detailed statistics
- **Flexible configuration** - Command line options
- **Academic focus** - Research-friendly architecture

---

**Author**: Academic Research Team  
**License**: MIT  
**Version**: 1.0.0  
**Compatibility**: Python 3.7+, macOS, Linux, Windows 