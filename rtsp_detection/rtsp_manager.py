"""
RTSP Manager Module
Handles RTSP stream connections with robust error handling and reconnection logic.

This module provides:
- RTSP connection management
- Automatic reconnection on connection loss
- Stream property detection
- Connection health monitoring
- Configurable retry logic

Author: Academic Research Team
"""

import cv2
import time
import logging
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RTSPConfig:
    """Configuration for RTSP connection."""
    url: str
    max_retries: int = 3
    retry_delay: int = 5
    connection_timeout: int = 10
    buffer_size: int = 1024 * 1024  # 1MB buffer

@dataclass
class StreamProperties:
    """Properties of the RTSP stream."""
    width: int
    height: int
    fps: float
    frame_count: int
    is_live: bool

class RTSPManager:
    """
    Manages RTSP stream connections with robust error handling.
    
    Features:
    - Automatic connection management
    - Reconnection on connection loss
    - Stream property detection
    - Health monitoring
    - Configurable retry logic
    """
    
    def __init__(self, config: RTSPConfig):
        """
        Initialize RTSP manager with configuration.
        
        Args:
            config: RTSP configuration object
        """
        self.config = config
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_connected = False
        self.connection_attempts = 0
        self.last_frame_time = 0
        self.stream_properties: Optional[StreamProperties] = None
        
        # Set OpenCV buffer size for RTSP
        cv2.setUseOptimized(True)
        
    def connect(self) -> bool:
        """
        Establish connection to RTSP stream.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        logger.info(f"Connecting to RTSP stream: {self.config.url}")
        
        try:
            # Create VideoCapture object
            self.cap = cv2.VideoCapture(self.config.url)
            
            # Set buffer size
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.config.buffer_size)
            
            if not self.cap.isOpened():
                logger.error("Failed to open RTSP stream")
                return False
            
            # Test connection by reading a frame
            ret, frame = self.cap.read()
            if not ret or frame is None:
                logger.error("Failed to read frame from RTSP stream")
                self.cap.release()
                return False
            
            # Get stream properties
            self.stream_properties = self._get_stream_properties()
            self.is_connected = True
            self.connection_attempts = 0
            
            logger.info(f"Successfully connected to RTSP stream")
            logger.info(f"Stream properties: {self.stream_properties}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to RTSP stream: {e}")
            if self.cap:
                self.cap.release()
            return False
    
    def connect_with_retry(self) -> bool:
        """
        Attempt to connect with retry logic.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        for attempt in range(self.config.max_retries):
            logger.info(f"Connection attempt {attempt + 1}/{self.config.max_retries}")
            
            if self.connect():
                return True
            
            self.connection_attempts += 1
            
            if attempt < self.config.max_retries - 1:
                logger.info(f"Retrying in {self.config.retry_delay} seconds...")
                time.sleep(self.config.retry_delay)
        
        logger.error("Failed to connect after all retry attempts")
        return False
    
    def _get_stream_properties(self) -> StreamProperties:
        """
        Get properties of the RTSP stream.
        
        Returns:
            StreamProperties: Stream properties object
        """
        if not self.cap:
            raise RuntimeError("No active connection")
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Determine if stream is live (frame_count is 0 for live streams)
        is_live = frame_count == 0
        
        return StreamProperties(
            width=width,
            height=height,
            fps=fps,
            frame_count=frame_count,
            is_live=is_live
        )
    
    def read_frame(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """
        Read a frame from the RTSP stream.
        
        Returns:
            Tuple[bool, Optional[cv2.Mat]]: (success, frame)
        """
        if not self.is_connected or not self.cap:
            return False, None
        
        try:
            ret, frame = self.cap.read()
            
            if not ret or frame is None:
                logger.warning("Failed to read frame, attempting reconnection...")
                self._handle_connection_loss()
                return False, None
            
            self.last_frame_time = time.time()
            return True, frame
            
        except Exception as e:
            logger.error(f"Error reading frame: {e}")
            self._handle_connection_loss()
            return False, None
    
    def _handle_connection_loss(self):
        """Handle connection loss and attempt reconnection."""
        logger.info("Handling connection loss...")
        self.is_connected = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Attempt reconnection
        if self.connect_with_retry():
            logger.info("Successfully reconnected to RTSP stream")
        else:
            logger.error("Failed to reconnect to RTSP stream")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get current connection status and statistics.
        
        Returns:
            Dict[str, Any]: Connection status information
        """
        current_time = time.time()
        
        return {
            "is_connected": self.is_connected,
            "connection_attempts": self.connection_attempts,
            "last_frame_time": self.last_frame_time,
            "time_since_last_frame": current_time - self.last_frame_time if self.last_frame_time > 0 else None,
            "stream_properties": self.stream_properties.__dict__ if self.stream_properties else None
        }
    
    def release(self):
        """Release the RTSP connection and cleanup resources."""
        logger.info("Releasing RTSP connection...")
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.is_connected = False
        logger.info("RTSP connection released")
    
    def __enter__(self):
        """Context manager entry."""
        if not self.connect_with_retry():
            raise RuntimeError("Failed to connect to RTSP stream")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release() 