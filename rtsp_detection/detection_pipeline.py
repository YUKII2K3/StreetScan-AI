"""
RTSP Detection Pipeline Module
Main pipeline for real-time vehicle detection using RTSP streams.

This module provides:
- Real-time vehicle detection and tracking
- Make, model, and color recognition
- Speed and direction calculation
- Live visualization
- Result logging and saving

Author: Academic Research Team
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
from VehicleDetectionTracker.VehicleDetectionTracker import VehicleDetectionTracker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DetectionConfig:
    """Configuration for detection pipeline."""
    show_live_window: bool = True
    save_detections: bool = False
    save_frames: bool = False
    log_results: bool = True
    output_dir: str = "detection_output"
    max_fps: Optional[int] = None  # Limit FPS for performance

@dataclass
class DetectionResult:
    """Results from a single frame detection."""
    timestamp: datetime
    frame_number: int
    processing_time: float
    detection_results: Dict[str, Any]
    frame_saved: bool = False

class DetectionPipeline:
    """
    Main pipeline for real-time vehicle detection using RTSP streams.
    
    Features:
    - Real-time vehicle detection and tracking
    - Make, model, and color recognition
    - Speed and direction calculation
    - Live visualization
    - Result logging and saving
    - Performance monitoring
    """
    
    def __init__(self, rtsp_config: RTSPConfig, detection_config: DetectionConfig):
        """
        Initialize detection pipeline.
        
        Args:
            rtsp_config: RTSP connection configuration
            detection_config: Detection pipeline configuration
        """
        self.rtsp_config = rtsp_config
        self.detection_config = detection_config
        self.vehicle_detector = VehicleDetectionTracker()
        self.rtsp_manager: Optional[RTSPManager] = None
        
        # Performance tracking
        self.frame_count = 0
        self.start_time = None
        self.processing_times = []
        
        # Create output directory if needed
        if self.detection_config.save_detections or self.detection_config.save_frames:
            os.makedirs(self.detection_config.output_dir, exist_ok=True)
        
        logger.info("Detection pipeline initialized")
    
    def start_detection(self, result_callback: Optional[Callable] = None):
        """
        Start the real-time detection pipeline.
        
        Args:
            result_callback: Optional callback function for detection results
        """
        logger.info("Starting real-time vehicle detection pipeline...")
        
        try:
            with RTSPManager(self.rtsp_config) as rtsp_manager:
                self.rtsp_manager = rtsp_manager
                self.start_time = time.time()
                
                print("🚗 Starting real-time vehicle detection...")
                print("Press 'q' to quit, 's' to save current frame")
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
    
    def _process_frame(self, frame) -> DetectionResult:
        """
        Process a single frame for vehicle detection.
        
        Args:
            frame: Input frame from RTSP stream
            
        Returns:
            DetectionResult: Detection results for the frame
        """
        processing_start = time.time()
        
        # Process frame with vehicle detector
        timestamp = datetime.now()
        detection_results = self.vehicle_detector.process_frame(frame, timestamp)
        
        processing_time = time.time() - processing_start
        
        # Update statistics
        self.frame_count += 1
        self.processing_times.append(processing_time)
        
        return DetectionResult(
            timestamp=timestamp,
            frame_number=self.frame_count,
            processing_time=processing_time,
            detection_results=detection_results
        )
    
    def _display_results(self, frame, detection_result: DetectionResult):
        """Display detection results in live window."""
        # Get annotated frame if available
        if 'annotated_frame_base64' in detection_result.detection_results:
            annotated_frame = self.vehicle_detector._decode_image_base64(
                detection_result.detection_results['annotated_frame_base64']
            )
            if annotated_frame is not None:
                # Add performance overlay
                self._add_performance_overlay(annotated_frame, detection_result)
                cv2.imshow("Vehicle Detection - RTSP Stream", annotated_frame)
        else:
            # Fallback to original frame
            self._add_performance_overlay(frame, detection_result)
            cv2.imshow("Vehicle Detection - RTSP Stream", frame)
    
    def _add_performance_overlay(self, frame, detection_result: DetectionResult):
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
    
    def _save_detection_results(self, detection_result: DetectionResult):
        """Save detection results to file."""
        timestamp_str = detection_result.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            self.detection_config.output_dir, 
            f"detection_results_{timestamp_str}.json"
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
    
    def _save_frame(self, frame, detection_result: DetectionResult):
        """Save current frame to file."""
        timestamp_str = detection_result.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            self.detection_config.output_dir, 
            f"frame_{timestamp_str}.jpg"
        )
        
        cv2.imwrite(filename, frame)
        detection_result.frame_saved = True
        
        logger.info(f"Frame saved to: {filename}")
    
    def _log_results(self, detection_result: DetectionResult):
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
        
        logger.info("Detection pipeline cleanup completed")

def main():
    """Main function for standalone detection pipeline."""
    # RTSP configuration
    rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
    rtsp_config = RTSPConfig(url=rtsp_url)
    
    # Detection configuration
    detection_config = DetectionConfig(
        show_live_window=True,
        save_detections=True,
        save_frames=False,
        log_results=True,
        output_dir="detection_output"
    )
    
    # Create pipeline
    pipeline = DetectionPipeline(rtsp_config, detection_config)
    
    # Custom callback function (optional)
    def custom_callback(detection_result: DetectionResult):
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