"""
Simple RTSP Detection Pipeline Module
Simplified vehicle detection using RTSP streams without TensorFlow dependencies.

This module provides:
- Real-time vehicle detection and tracking
- Speed and direction calculation
- Live visualization
- Result logging and saving
- No TensorFlow dependency

Author: Academic Research Team
Crafted by Yukthesh - Building intelligent solutions for the future
"""

import cv2
import time
import json
import logging
from datetime import datetime
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
import os

from .rtsp_manager import RTSPManager, RTSPConfig
from ultralytics import YOLO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SimpleDetectionConfig:
    """Configuration for simple detection pipeline."""
    show_live_window: bool = True
    save_detections: bool = False
    save_frames: bool = False
    log_results: bool = True
    output_dir: str = "detection_output"
    max_fps: Optional[int] = None  # Limit FPS for performance
    confidence_threshold: float = 0.5  # Detection confidence threshold

@dataclass
class SimpleDetectionResult:
    """Results from a single frame detection."""
    timestamp: datetime
    frame_number: int
    processing_time: float
    detection_results: Dict[str, Any]
    frame_saved: bool = False

class SimpleDetectionPipeline:
    """
    Simplified pipeline for real-time vehicle detection using RTSP streams.
    
    Features:
    - Real-time vehicle detection and tracking
    - Speed and direction calculation
    - Live visualization
    - Result logging and saving
    - Performance monitoring
    - No TensorFlow dependency
    """
    
    def __init__(self, rtsp_config: RTSPConfig, detection_config: SimpleDetectionConfig):
        """
        Initialize simple detection pipeline.
        
        Args:
            rtsp_config: RTSP connection configuration
            detection_config: Detection pipeline configuration
        """
        self.rtsp_config = rtsp_config
        self.detection_config = detection_config
        self.yolo_model = YOLO("yolov8n.pt")  # Load YOLOv8 nano model
        self.rtsp_manager: Optional[RTSPManager] = None
        
        # Performance tracking
        self.frame_count = 0
        self.start_time = None
        self.processing_times = []
        
        # Vehicle tracking
        self.track_history = {}
        self.vehicle_timestamps = {}
        
        # Create output directory if needed
        if self.detection_config.save_detections or self.detection_config.save_frames:
            os.makedirs(self.detection_config.output_dir, exist_ok=True)
        
        logger.info("Simple detection pipeline initialized")
    
    def start_detection(self, result_callback: Optional[Callable] = None):
        """
        Start the real-time detection pipeline.
        
        Args:
            result_callback: Optional callback function for detection results
        """
        logger.info("Starting simple real-time vehicle detection pipeline...")
        
        try:
            with RTSPManager(self.rtsp_config) as rtsp_manager:
                self.rtsp_manager = rtsp_manager
                self.start_time = time.time()
                
                print("🚗 Starting simple vehicle detection...")
                print("Press 'q' to quit")
                print("=" * 60)
                
                self._run_detection_loop(result_callback)
                
        except Exception as e:
            logger.error(f"Error in detection pipeline: {e}")
            raise
        finally:
            self._cleanup()
    
    def _run_detection_loop(self, result_callback: Optional[Callable]):
        """Main detection loop."""
        last_fps_time = time.time()
        
        while True:
            loop_start = time.time()
            
            # Read frame from RTSP stream
            success, frame = self.rtsp_manager.read_frame()
            if not success or frame is None:
                logger.warning("Failed to read frame, continuing...")
                continue
            
            # Process frame
            detection_result = self._process_frame(frame)
            
            # Call callback if provided
            if result_callback:
                result_callback(detection_result)
            
            # Display results
            if self.detection_config.show_live_window:
                self._display_results(frame, detection_result)
            
            # Save results if configured
            if self.detection_config.save_detections:
                self._save_detection_results(detection_result)
            
            # Save frame if configured
            if self.detection_config.save_frames:
                self._save_frame(frame, detection_result)
            
            # Log results if configured
            if self.detection_config.log_results:
                self._log_results(detection_result)
            
            # FPS limiting
            if self.detection_config.max_fps:
                self._limit_fps(loop_start)
            
            # FPS display
            current_time = time.time()
            if current_time - last_fps_time >= 5.0:  # Update every 5 seconds
                self._display_fps_stats()
                last_fps_time = current_time
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Quitting detection pipeline...")
                break
    
    def _process_frame(self, frame) -> SimpleDetectionResult:
        """
        Process a single frame for vehicle detection.
        
        Args:
            frame: Input frame from RTSP stream
            
        Returns:
            SimpleDetectionResult: Detection results for the frame
        """
        processing_start = time.time()
        
        # Run YOLO detection with tracking
        results = self.yolo_model.track(frame, persist=True, tracker="bytetrack.yaml", conf=self.detection_config.confidence_threshold)
        
        # Process results
        detection_results = self._process_yolo_results(results, frame)
        
        processing_time = time.time() - processing_start
        
        # Update statistics
        self.frame_count += 1
        self.processing_times.append(processing_time)
        
        return SimpleDetectionResult(
            timestamp=datetime.now(),
            frame_number=self.frame_count,
            processing_time=processing_time,
            detection_results=detection_results
        )
    
    def _process_yolo_results(self, results, frame) -> Dict[str, Any]:
        """Process YOLO detection results."""
        detection_data = {
            "number_of_vehicles_detected": 0,
            "detected_vehicles": [],
            "annotated_frame_base64": None,
            "original_frame_base64": None
        }
        
        if results and len(results) > 0 and results[0].boxes is not None:
            result = results[0]
            
            # Get detection data
            boxes = result.boxes.xywh.cpu() if result.boxes.xywh is not None else []
            conf_list = result.boxes.conf.cpu() if result.boxes.conf is not None else []
            track_ids = result.boxes.id.int().cpu().tolist() if result.boxes.id is not None else []
            clss = result.boxes.cls.cpu().tolist() if result.boxes.cls is not None else []
            names = result.names
            
            # Filter for vehicles (car, truck, bus, motorcycle)
            vehicle_classes = ['car', 'truck', 'bus', 'motorcycle']
            
            for i, (box, conf, track_id, cls) in enumerate(zip(boxes, conf_list, track_ids, clss)):
                class_name = names[int(cls)]
                
                # Only process vehicles
                if class_name.lower() in vehicle_classes:
                    x, y, w, h = box
                    
                    # Update tracking history
                    if track_id not in self.track_history:
                        self.track_history[track_id] = []
                    
                    track = self.track_history[track_id]
                    track.append((float(x), float(y)))
                    
                    # Limit history length
                    if len(track) > 30:
                        track.pop(0)
                    
                    # Calculate speed and direction
                    speed_info = self._calculate_speed_and_direction(track_id, x, y)
                    
                    # Create vehicle data
                    vehicle_data = {
                        "vehicle_id": int(track_id),
                        "vehicle_type": class_name,
                        "detection_confidence": float(conf),
                        "vehicle_coordinates": {
                            "x": float(x),
                            "y": float(y),
                            "width": float(w),
                            "height": float(h)
                        },
                        "speed_info": speed_info,
                        "color_info": "[]",  # Placeholder - no color detection
                        "model_info": "[]"   # Placeholder - no model detection
                    }
                    
                    detection_data["detected_vehicles"].append(vehicle_data)
                    detection_data["number_of_vehicles_detected"] += 1
            
            # Get annotated frame
            annotated_frame = result.plot()
            detection_data["annotated_frame_base64"] = self._encode_frame_base64(annotated_frame)
        
        # Encode original frame
        detection_data["original_frame_base64"] = self._encode_frame_base64(frame)
        
        return detection_data
    
    def _calculate_speed_and_direction(self, track_id, x, y) -> Dict[str, Any]:
        """Calculate speed and direction for a tracked vehicle."""
        import math
        
        current_time = time.time()
        
        if track_id not in self.vehicle_timestamps:
            self.vehicle_timestamps[track_id] = {"timestamps": [], "positions": []}
        
        # Store current position and timestamp
        self.vehicle_timestamps[track_id]["timestamps"].append(current_time)
        self.vehicle_timestamps[track_id]["positions"].append((x, y))
        
        # Keep only recent data
        if len(self.vehicle_timestamps[track_id]["timestamps"]) > 10:
            self.vehicle_timestamps[track_id]["timestamps"].pop(0)
            self.vehicle_timestamps[track_id]["positions"].pop(0)
        
        timestamps = self.vehicle_timestamps[track_id]["timestamps"]
        positions = self.vehicle_timestamps[track_id]["positions"]
        
        speed_kph = None
        reliability = 0.0
        direction_label = "Unknown"
        direction = None
        
        if len(timestamps) >= 2:
            # Calculate speed
            total_distance = 0
            total_time = 0
            
            for i in range(1, len(positions)):
                x1, y1 = positions[i-1]
                x2, y2 = positions[i]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                time_diff = timestamps[i] - timestamps[i-1]
                
                total_distance += distance
                total_time += time_diff
            
            if total_time > 0:
                avg_speed_mps = total_distance / total_time
                speed_kph = avg_speed_mps * 3.6  # Convert to km/h
            
            # Calculate direction
            if len(positions) >= 2:
                initial_x, initial_y = positions[0]
                final_x, final_y = positions[-1]
                direction = math.atan2(final_y - initial_y, final_x - initial_x)
                direction_label = self._map_direction_to_label(direction)
            
            # Calculate reliability
            if len(timestamps) < 5:
                reliability = 0.5
            elif len(timestamps) < 10:
                reliability = 0.7
            else:
                reliability = 1.0
        
        return {
            "kph": speed_kph,
            "reliability": reliability,
            "direction_label": direction_label,
            "direction": direction
        }
    
    def _map_direction_to_label(self, direction):
        """Map direction angle to label."""
        import math
        
        direction_ranges = {
            (-math.pi / 8, math.pi / 8): "Right",
            (math.pi / 8, 3 * math.pi / 8): "Bottom Right",
            (3 * math.pi / 8, 5 * math.pi / 8): "Bottom",
            (5 * math.pi / 8, 7 * math.pi / 8): "Bottom Left",
            (7 * math.pi / 8, -7 * math.pi / 8): "Left",
            (-7 * math.pi / 8, -5 * math.pi / 8): "Top Left",
            (-5 * math.pi / 8, -3 * math.pi / 8): "Top",
            (-3 * math.pi / 8, -math.pi / 8): "Top Right"
        }
        
        for angle_range, label in direction_ranges.items():
            if angle_range[0] <= direction <= angle_range[1]:
                return label
        
        return "Unknown"
    
    def _encode_frame_base64(self, frame):
        """Encode frame to base64."""
        import base64
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode()
    
    def _display_results(self, frame, detection_result: SimpleDetectionResult):
        """Display detection results in live window."""
        # Get annotated frame if available
        if 'annotated_frame_base64' in detection_result.detection_results:
            annotated_frame = self._decode_frame_base64(
                detection_result.detection_results['annotated_frame_base64']
            )
            if annotated_frame is not None:
                # Add performance overlay
                self._add_performance_overlay(annotated_frame, detection_result)
                cv2.imshow("Simple Vehicle Detection - RTSP Stream", annotated_frame)
        else:
            # Fallback to original frame
            self._add_performance_overlay(frame, detection_result)
            cv2.imshow("Simple Vehicle Detection - RTSP Stream", frame)
    
    def _decode_frame_base64(self, frame_base64):
        """Decode base64 frame."""
        import base64
        import numpy as np
        try:
            image_data = base64.b64decode(frame_base64)
            image_np = np.frombuffer(image_data, dtype=np.uint8)
            return cv2.imdecode(image_np, flags=cv2.IMREAD_COLOR)
        except:
            return None
    
    def _add_performance_overlay(self, frame, detection_result: SimpleDetectionResult):
        """Add performance information overlay to frame."""
        # Add FPS and processing time
        fps = 1.0 / detection_result.processing_time if detection_result.processing_time > 0 else 0
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame: {detection_result.frame_number}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Processing: {detection_result.processing_time*1000:.1f}ms", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add vehicle count
        vehicle_count = detection_result.detection_results.get('number_of_vehicles_detected', 0)
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    def _save_detection_results(self, detection_result: SimpleDetectionResult):
        """Save detection results to file."""
        timestamp_str = detection_result.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            self.detection_config.output_dir, 
            f"simple_detection_results_{timestamp_str}.json"
        )
        
        # Prepare data for saving
        save_data = {
            "timestamp": detection_result.timestamp.isoformat(),
            "frame_number": detection_result.frame_number,
            "processing_time": detection_result.processing_time,
            "detection_results": detection_result.detection_results
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        logger.info(f"Detection results saved to: {filename}")
    
    def _save_frame(self, frame, detection_result: SimpleDetectionResult):
        """Save current frame to file."""
        timestamp_str = detection_result.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            self.detection_config.output_dir, 
            f"simple_frame_{timestamp_str}.jpg"
        )
        
        cv2.imwrite(filename, frame)
        detection_result.frame_saved = True
        
        logger.info(f"Frame saved to: {filename}")
    
    def _log_results(self, detection_result: SimpleDetectionResult):
        """Log detection results to console."""
        vehicle_count = detection_result.detection_results.get('number_of_vehicles_detected', 0)
        
        if vehicle_count > 0:
            print(f"🎯 Frame {detection_result.frame_number}: {vehicle_count} vehicle(s) detected")
            
            # Log details for each vehicle
            for vehicle in detection_result.detection_results.get('detected_vehicles', []):
                vehicle_id = vehicle.get('vehicle_id', 'Unknown')
                vehicle_type = vehicle.get('vehicle_type', 'Unknown')
                confidence = vehicle.get('detection_confidence', 0)
                
                # Speed information
                speed_info = vehicle.get('speed_info', {})
                speed_text = ""
                if speed_info.get('kph') is not None:
                    speed_text = f" | Speed: {speed_info['kph']:.1f} km/h"
                
                print(f"   ID: {vehicle_id} | Type: {vehicle_type} | Conf: {confidence:.3f}{speed_text}")
    
    def _limit_fps(self, loop_start: float):
        """Limit FPS if configured."""
        if self.detection_config.max_fps:
            target_frame_time = 1.0 / self.detection_config.max_fps
            elapsed = time.time() - loop_start
            if elapsed < target_frame_time:
                time.sleep(target_frame_time - elapsed)
    
    def _display_fps_stats(self):
        """Display FPS statistics."""
        if self.start_time and self.frame_count > 0:
            elapsed_time = time.time() - self.start_time
            avg_fps = self.frame_count / elapsed_time
            avg_processing_time = sum(self.processing_times) / len(self.processing_times)
            
            print(f"📊 Stats - FPS: {avg_fps:.1f}, Avg Processing: {avg_processing_time*1000:.1f}ms")
    
    def _cleanup(self):
        """Cleanup resources."""
        if self.rtsp_manager:
            self.rtsp_manager.release()
        
        cv2.destroyAllWindows()
        
        # Display final statistics
        if self.start_time and self.frame_count > 0:
            total_time = time.time() - self.start_time
            avg_fps = self.frame_count / total_time
            avg_processing_time = sum(self.processing_times) / len(self.processing_times)
            
            print(f"\n📊 Final Statistics:")
            print(f"   Total frames processed: {self.frame_count}")
            print(f"   Total time: {total_time:.1f} seconds")
            print(f"   Average FPS: {avg_fps:.1f}")
            print(f"   Average processing time: {avg_processing_time*1000:.1f}ms")
        
        logger.info("Simple detection pipeline cleanup completed")

def main():
    """Main function for simple detection pipeline."""
    # RTSP configuration
    rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
    rtsp_config = RTSPConfig(url=rtsp_url)
    
    # Detection configuration
    detection_config = SimpleDetectionConfig(
        show_live_window=True,
        save_detections=True,
        save_frames=False,
        log_results=True,
        output_dir="detection_output"
    )
    
    # Create pipeline
    pipeline = SimpleDetectionPipeline(rtsp_config, detection_config)
    
    # Custom callback function (optional)
    def custom_callback(detection_result: SimpleDetectionResult):
        """Custom callback for detection results."""
        vehicle_count = detection_result.detection_results.get('number_of_vehicles_detected', 0)
        if vehicle_count > 0:
            print(f"🎯 {vehicle_count} vehicle(s) detected in frame {detection_result.frame_number}")
    
    # Start detection
    try:
        pipeline.start_detection(custom_callback)
    except KeyboardInterrupt:
        print("\n🛑 Detection pipeline interrupted by user")
    except Exception as e:
        print(f"❌ Error in detection pipeline: {e}")

if __name__ == "__main__":
    main() 