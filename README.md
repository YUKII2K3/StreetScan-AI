# 🚗 RTSP Vehicle Detection System

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

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd StreetScan-AI
```

### 2. Setup Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Your RTSP Camera
Update the RTSP URL in the scripts with your camera details:

```python
# Example RTSP URL format
rtsp_url = "rtsp://username:password@camera_ip:port/stream_path"
```

### 4. Test RTSP Connection
```bash
python3 test_rtsp.py
```

### 5. Run Vehicle Detection

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
rtsp://username:password@ip_address:port/stream_path
```

**Common RTSP URL formats:**
- `rtsp://admin:password@192.168.0.100:554`
- `rtsp://admin:password@192.168.0.100:554/cam/realmonitor?channel=1&subtype=0`
- `rtsp://admin:password@192.168.0.100:554/stream1`
- `rtsp://admin:password@192.168.0.100:8554`

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

## 📁 Project Structure

```
StreetScan-AI/
├── rtsp_detection/              # Main detection package
│   ├── __init__.py
│   ├── rtsp_manager.py         # RTSP connection management
│   ├── connection_tester.py    # Connection testing
│   ├── simple_detection_pipeline.py  # Simple detection
│   └── detection_pipeline.py   # Full detection
├── scripts/                    # Main execution scripts
│   ├── test_rtsp.py           # Test RTSP connection
│   ├── run_simple_detection.py # Run simple detection
│   └── run_detection.py       # Run full detection
├── examples/                   # Example implementations
├── requirements.txt           # Python dependencies
├── setup.py                  # Setup script
└── README.md                 # This file
```

## 🔧 Dependencies

### Core Dependencies
- `opencv-python>=4.5.0` - Video processing and RTSP handling
- `ultralytics>=8.0.0` - YOLOv8 object detection
- `numpy>=1.19.0` - Numerical computing

### Optional Dependencies
- `tensorflow>=2.0.0` - For full detection mode (make/model/color)

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
rtsp_config = RTSPConfig(url="rtsp://admin:pass@192.168.0.100:554")
detection_config = SimpleDetectionConfig(save_detections=True)
pipeline = SimpleDetectionPipeline(rtsp_config, detection_config)

# Start with custom callback
pipeline.start_detection(my_callback)
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

- [ ] Clone the repository
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is an academic research project. For contributions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Author**: Academic Research Team  
**License**: MIT  
**Version**: 1.0.0  
**Compatibility**: Python 3.7+, macOS, Linux, Windows

---

<div align="center">

### 🎨 **Crafted by Yukthesh** 🎨

*Building intelligent solutions for the future*

[![GitHub](https://img.shields.io/badge/GitHub-Yukthesh-blue?style=for-the-badge&logo=github)](https://github.com/Yukthesh)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yukthesh-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/yukthesh)

---

**Made with ❤️ for academic research and innovation**

</div>
