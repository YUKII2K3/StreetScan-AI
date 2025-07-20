# 🚀 Quick Start: RTSP Integration for VehicleDetectionTracker

## 📋 Summary

This project uses **YOLOv8 + ByteTrack** for vehicle detection and tracking, with **MobileNet** models for vehicle classification and color recognition. The system can process RTSP streams from IP cameras.

## 🎯 Your RTSP Configuration

```
rtsp://admin:CamPassword_0718@192.168.0.101:554
```

## ⚡ Quick Setup (3 Steps)

### Step 1: Run Setup Script
```bash
python3 setup_rtsp.py
```
This will:
- Check dependencies
- Configure your RTSP URL
- Update example files
- Test the connection

### Step 2: Test Connection
```bash
python3 test_rtsp_connection.py
```
This shows your stream properties and verifies connectivity.

### Step 3: Run Vehicle Detection
```bash
# Simple version
python3 examples/RTSPTrackerTest.py

# Advanced version (recommended)
python3 examples/AdvancedRTSPTracker.py
```

## 🔍 What the System Detects

For each vehicle, you get:
- **Vehicle Type**: car, truck, bus, etc.
- **Color**: Black, White, Red, Blue, etc.
- **Make/Model**: Toyota Camry, Ford Mustang, etc.
- **Speed**: Calculated in km/h
- **Direction**: Movement direction
- **Confidence**: Detection accuracy

## 📊 Sample Output

```json
{
  "number_of_vehicles_detected": 1,
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
        "direction_label": "Right"
      }
    }
  ]
}
```

## 🎮 Controls

- **'q'**: Quit the application
- **'s'**: Save current frame (AdvancedRTSPTracker only)

## 🛠️ Troubleshooting

### Connection Issues
1. **Check camera IP**: Verify `192.168.0.101` is correct
2. **Test credentials**: Try accessing camera web interface
3. **Network access**: Ensure camera is on same network
4. **RTSP enabled**: Check camera settings

### Performance Issues
1. **Lower resolution**: Reduce camera stream quality
2. **Wired connection**: Use Ethernet instead of WiFi
3. **GPU acceleration**: System uses GPU if available

## 📁 Key Files

- `setup_rtsp.py` - Interactive setup script
- `test_rtsp_connection.py` - Connection tester
- `examples/RTSPTrackerTest.py` - Simple integration
- `examples/AdvancedRTSPTracker.py` - Advanced with error handling
- `RTSP_INTEGRATION_GUIDE.md` - Detailed guide

## 🔧 Pre-trained Models

- **YOLOv8n.pt**: Vehicle detection (Ultralytics)
- **Car Make/Model**: `data/model-weights-spectrico-mmr-mobilenet-128x128-344FF72B.pb`
- **Car Color**: `data/model-weights-spectrico-car-colors-mobilenet-224x224-052EAC82.pb`

## 💡 Pro Tips

1. **Start with connection test** before running full detection
2. **Use AdvancedRTSPTracker** for production (has error handling)
3. **Monitor FPS** - aim for 15+ FPS for real-time performance
4. **Save frames** when you see interesting detections
5. **Custom callbacks** let you integrate with databases/alerts

## 🚀 Ready to Go!

Your RTSP stream is configured and ready. Run the setup script to get started:

```bash
python3 setup_rtsp.py
```

The system will automatically detect vehicles, track their movement, and provide detailed analysis including speed, color, and make/model information. 