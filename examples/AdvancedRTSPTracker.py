import cv2
import time
from VehicleDetectionTracker.VehicleDetectionTracker import VehicleDetectionTracker

class AdvancedRTSPTracker:
    def __init__(self, rtsp_url, max_retries=3, retry_delay=5):
        """
        Initialize the advanced RTSP tracker with connection management.
        
        Args:
            rtsp_url (str): RTSP stream URL
            max_retries (int): Maximum number of connection retry attempts
            retry_delay (int): Delay between retry attempts in seconds
        """
        self.rtsp_url = rtsp_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.vehicle_detection = VehicleDetectionTracker()
        
    def test_rtsp_connection(self):
        """
        Test if the RTSP stream is accessible.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        print(f"Testing RTSP connection to: {self.rtsp_url}")
        
        cap = cv2.VideoCapture(self.rtsp_url)
        if not cap.isOpened():
            print("❌ Failed to open RTSP stream")
            return False
            
        # Try to read a frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            print("❌ Failed to read frame from RTSP stream")
            return False
            
        print("✅ RTSP connection successful!")
        print(f"   Frame size: {frame.shape[1]}x{frame.shape[0]}")
        return True
    
    def connect_with_retry(self):
        """
        Attempt to connect to RTSP stream with retry logic.
        
        Returns:
            cv2.VideoCapture or None: Video capture object if successful
        """
        for attempt in range(self.max_retries):
            print(f"Connection attempt {attempt + 1}/{self.max_retries}")
            
            if self.test_rtsp_connection():
                cap = cv2.VideoCapture(self.rtsp_url)
                if cap.isOpened():
                    return cap
            
            if attempt < self.max_retries - 1:
                print(f"Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
        
        print("❌ Failed to connect after all retry attempts")
        return None
    
    def process_stream(self, result_callback=None):
        """
        Process the RTSP stream with advanced error handling.
        
        Args:
            result_callback (function): Callback function for processing results
        """
        # Default callback if none provided
        if result_callback is None:
            result_callback = self.default_callback
        
        # Attempt to connect
        cap = self.connect_with_retry()
        if cap is None:
            return
        
        print("🚗 Starting vehicle detection on RTSP stream...")
        print("Press 'q' to quit, 's' to save current frame")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    print("⚠️  Failed to read frame, attempting to reconnect...")
                    cap.release()
                    cap = self.connect_with_retry()
                    if cap is None:
                        break
                    continue
                
                frame_count += 1
                current_time = time.time()
                
                # Calculate FPS
                if frame_count % 30 == 0:  # Update FPS every 30 frames
                    elapsed_time = current_time - start_time
                    fps = frame_count / elapsed_time
                    print(f"📊 FPS: {fps:.1f}, Frames processed: {frame_count}")
                
                # Process frame
                from datetime import datetime
                timestamp = datetime.now()
                response = self.vehicle_detection.process_frame(frame, timestamp)
                
                # Call callback function
                result_callback(response)
                
                # Display annotated frame
                if 'annotated_frame_base64' in response:
                    annotated_frame = self.vehicle_detection._decode_image_base64(response['annotated_frame_base64'])
                    if annotated_frame is not None:
                        cv2.imshow("Vehicle Detection Tracker - RTSP Stream", annotated_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("🛑 Quitting...")
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
                    filename = f"captured_frame_{timestamp_str}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"💾 Saved frame as: {filename}")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"❌ Error during processing: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("✅ Stream processing completed")
    
    def default_callback(self, result):
        """
        Default callback function for processing results.
        
        Args:
            result (dict): Detection results
        """
        if result['number_of_vehicles_detected'] > 0:
            print(f"🚗 Detected {result['number_of_vehicles_detected']} vehicle(s)")
            
            for vehicle in result['detected_vehicles']:
                vehicle_id = vehicle['vehicle_id']
                vehicle_type = vehicle['vehicle_type']
                confidence = vehicle['detection_confidence']
                
                # Speed information
                speed_info = vehicle['speed_info']
                speed_text = ""
                if speed_info['kph'] is not None:
                    speed_text = f" | Speed: {speed_info['kph']:.1f} km/h"
                
                print(f"   ID: {vehicle_id} | Type: {vehicle_type} | Conf: {confidence:.3f}{speed_text}")

# Example usage
if __name__ == "__main__":
    # RTSP stream configuration
    rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
    
    # Create tracker instance
    tracker = AdvancedRTSPTracker(rtsp_url, max_retries=3, retry_delay=5)
    
    # Custom callback function (optional)
    def custom_callback(result):
        """
        Custom callback function - you can modify this to handle results as needed.
        For example, save to database, send alerts, etc.
        """
        if result['number_of_vehicles_detected'] > 0:
            print(f"🎯 {result['number_of_vehicles_detected']} vehicle(s) detected!")
            
            # You could add your custom logic here:
            # - Save to database
            # - Send alerts
            # - Log to file
            # - etc.
    
    # Start processing
    tracker.process_stream(custom_callback) 