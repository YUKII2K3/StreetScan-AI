#!/usr/bin/env python3
"""
Simple RTSP Vehicle Detection Script
Basic vehicle detection using RTSP streams without TensorFlow dependencies.

Usage:
    python3 run_simple_detection.py

Features:
    - Real-time vehicle detection and tracking
    - Speed and direction calculation
    - Live visualization
    - Result logging and saving
    - No TensorFlow dependency

Author: Academic Research Team
Crafted by Yukthesh - Building intelligent solutions for the future
"""

import sys
import os
import argparse

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rtsp_detection.simple_detection_pipeline import SimpleDetectionPipeline, SimpleDetectionConfig
from rtsp_detection.rtsp_manager import RTSPConfig

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Simple RTSP Vehicle Detection System")
    
    # RTSP configuration
    parser.add_argument("--rtsp-url", 
                       default="rtsp://admin:CamPassword_0718@192.168.0.104:554/cam/realmonitor?channel=1&subtype=0",
                       help="RTSP stream URL")
    parser.add_argument("--max-retries", type=int, default=3,
                       help="Maximum connection retry attempts")
    parser.add_argument("--retry-delay", type=int, default=5,
                       help="Delay between retry attempts (seconds)")
    
    # Detection configuration
    parser.add_argument("--no-window", action="store_true",
                       help="Disable live window display")
    parser.add_argument("--save-detections", action="store_true",
                       help="Save detection results to files")
    parser.add_argument("--save-frames", action="store_true",
                       help="Save frames with detections")
    parser.add_argument("--output-dir", default="detection_output",
                       help="Output directory for saved files")
    parser.add_argument("--max-fps", type=int, default=None,
                       help="Maximum FPS (for performance control)")
    parser.add_argument("--no-logging", action="store_true",
                       help="Disable console logging")
    parser.add_argument("--confidence", type=float, default=0.5,
                       help="Detection confidence threshold (0.0-1.0)")
    
    return parser.parse_args()

def main():
    """Main function for simple vehicle detection pipeline."""
    args = parse_arguments()
    
    print("🚗 Simple RTSP Vehicle Detection System")
    print("=" * 50)
    print(f"RTSP URL: {args.rtsp_url}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Live Window: {'Disabled' if args.no_window else 'Enabled'}")
    print(f"Save Detections: {'Yes' if args.save_detections else 'No'}")
    print(f"Save Frames: {'Yes' if args.save_frames else 'No'}")
    print(f"Max FPS: {args.max_fps if args.max_fps else 'Unlimited'}")
    print(f"Confidence Threshold: {args.confidence}")
    print("=" * 50)
    
    # RTSP configuration
    rtsp_config = RTSPConfig(
        url=args.rtsp_url,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay
    )
    
    # Detection configuration
    detection_config = SimpleDetectionConfig(
        show_live_window=not args.no_window,
        save_detections=args.save_detections,
        save_frames=args.save_frames,
        log_results=not args.no_logging,
        output_dir=args.output_dir,
        max_fps=args.max_fps,
        confidence_threshold=args.confidence
    )
    
    # Create pipeline
    pipeline = SimpleDetectionPipeline(rtsp_config, detection_config)
    
    # Custom callback function for additional processing
    def detection_callback(detection_result):
        """Custom callback for detection results."""
        vehicle_count = detection_result.detection_results.get('number_of_vehicles_detected', 0)
        
        if vehicle_count > 0:
            # You can add custom processing here:
            # - Send alerts
            # - Save to database
            # - Trigger other systems
            # - etc.
            
            # Example: Log detailed vehicle information
            for vehicle in detection_result.detection_results.get('detected_vehicles', []):
                vehicle_id = vehicle.get('vehicle_id', 'Unknown')
                vehicle_type = vehicle.get('vehicle_type', 'Unknown')
                confidence = vehicle.get('detection_confidence', 0)
                
                # Speed information
                speed_info = vehicle.get('speed_info', {})
                speed_text = ""
                if speed_info.get('kph') is not None:
                    speed_text = f" | Speed: {speed_info['kph']:.1f} km/h"
                
                # Direction information
                direction_text = ""
                if speed_info.get('direction_label'):
                    direction_text = f" | Direction: {speed_info['direction_label']}"
                
                print(f"🚗 Vehicle {vehicle_id}: {vehicle_type} | Conf: {confidence:.3f}{speed_text}{direction_text}")
    
    # Start detection
    try:
        print("\n🚀 Starting simple vehicle detection pipeline...")
        print("Press 'q' to quit")
        print("-" * 50)
        
        pipeline.start_detection(detection_callback)
        
    except KeyboardInterrupt:
        print("\n🛑 Detection pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Error in detection pipeline: {e}")
        print("Please check your RTSP connection and try again.")
        return 1
    
    print("\n✅ Detection pipeline completed successfully!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 