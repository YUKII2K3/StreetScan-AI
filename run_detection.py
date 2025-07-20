#!/usr/bin/env python3
"""
RTSP Vehicle Detection Script
Main script to run real-time vehicle detection using RTSP streams.

Usage:
    python3 run_detection.py

Features:
    - Real-time vehicle detection and tracking
    - Make, model, and color recognition
    - Speed and direction calculation
    - Live visualization
    - Result logging and saving

Author: Academic Research Team
"""

import sys
import os
import argparse

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rtsp_detection.detection_pipeline import DetectionPipeline, DetectionConfig
from rtsp_detection.rtsp_manager import RTSPConfig

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="RTSP Vehicle Detection System")
    
    # RTSP configuration
    parser.add_argument("--rtsp-url", 
                       default="rtsp://admin:CamPassword_0718@192.168.0.101:554",
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
    
    return parser.parse_args()

def main():
    """Main function for vehicle detection pipeline."""
    args = parse_arguments()
    
    print("🚗 RTSP Vehicle Detection System")
    print("=" * 50)
    print(f"RTSP URL: {args.rtsp_url}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Live Window: {'Disabled' if args.no_window else 'Enabled'}")
    print(f"Save Detections: {'Yes' if args.save_detections else 'No'}")
    print(f"Save Frames: {'Yes' if args.save_frames else 'No'}")
    print(f"Max FPS: {args.max_fps if args.max_fps else 'Unlimited'}")
    print("=" * 50)
    
    # RTSP configuration
    rtsp_config = RTSPConfig(
        url=args.rtsp_url,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay
    )
    
    # Detection configuration
    detection_config = DetectionConfig(
        show_live_window=not args.no_window,
        save_detections=args.save_detections,
        save_frames=args.save_frames,
        log_results=not args.no_logging,
        output_dir=args.output_dir,
        max_fps=args.max_fps
    )
    
    # Create pipeline
    pipeline = DetectionPipeline(rtsp_config, detection_config)
    
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
                
                # Color information
                import json
                color_info = json.loads(vehicle.get('color_info', '[]'))
                color_text = ""
                if color_info:
                    color_text = f" | Color: {color_info[0]['color']}"
                
                # Model information
                model_info = json.loads(vehicle.get('model_info', '[]'))
                model_text = ""
                if model_info:
                    model_text = f" | Model: {model_info[0]['make']} {model_info[0]['model']}"
                
                print(f"🚗 Vehicle {vehicle_id}: {vehicle_type} | Conf: {confidence:.3f}{speed_text}{color_text}{model_text}")
    
    # Start detection
    try:
        print("\n🚀 Starting vehicle detection pipeline...")
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