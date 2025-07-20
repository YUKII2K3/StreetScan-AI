"""
RTSP Vehicle Detection Module
Academic Research Project - Vehicle Detection using YOLOv8, ByteTrack, and MobileNet

This module provides RTSP-based vehicle detection capabilities with:
- Real-time RTSP stream processing
- Vehicle detection and tracking
- Make, model, and color recognition
- Speed and direction calculation
- Modular architecture for academic research

Author: Academic Research Team
License: MIT
"""

from .rtsp_manager import RTSPManager
from .connection_tester import RTSPConnectionTester

# Import simple detection pipeline (no TensorFlow dependency)
try:
    from .simple_detection_pipeline import SimpleDetectionPipeline, SimpleDetectionConfig
    SIMPLE_DETECTION_AVAILABLE = True
except ImportError:
    SIMPLE_DETECTION_AVAILABLE = False

# Import full detection pipeline (requires TensorFlow)
try:
    from .detection_pipeline import DetectionPipeline, DetectionConfig
    FULL_DETECTION_AVAILABLE = True
except ImportError:
    FULL_DETECTION_AVAILABLE = False

__version__ = "1.0.0"
__author__ = "Academic Research Team"

__all__ = [
    'RTSPManager',
    'RTSPConnectionTester',
    'SIMPLE_DETECTION_AVAILABLE',
    'FULL_DETECTION_AVAILABLE'
]

# Add conditional imports
if SIMPLE_DETECTION_AVAILABLE:
    __all__.extend(['SimpleDetectionPipeline', 'SimpleDetectionConfig'])

if FULL_DETECTION_AVAILABLE:
    __all__.extend(['DetectionPipeline', 'DetectionConfig']) 