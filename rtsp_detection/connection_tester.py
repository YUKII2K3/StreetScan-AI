"""
RTSP Connection Tester Module
Tests RTSP stream connectivity and provides detailed stream information.

This module provides:
- RTSP connection testing
- Stream property analysis
- Performance benchmarking
- Connection diagnostics
- Detailed reporting

Author: Academic Research Team
"""

import cv2
import time
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from .rtsp_manager import RTSPManager, RTSPConfig

@dataclass
class ConnectionTestResult:
    """Results of RTSP connection test."""
    success: bool
    connection_time: float
    stream_properties: Optional[Dict[str, Any]]
    performance_metrics: Optional[Dict[str, Any]]
    error_message: Optional[str]
    recommendations: list

class RTSPConnectionTester:
    """
    Tests RTSP stream connectivity and provides detailed analysis.
    
    Features:
    - Connection testing
    - Stream property detection
    - Performance benchmarking
    - Diagnostic reporting
    - Recommendations for optimization
    """
    
    def __init__(self, rtsp_url: str, test_duration: int = 10):
        """
        Initialize connection tester.
        
        Args:
            rtsp_url: RTSP stream URL to test
            test_duration: Duration of performance test in seconds
        """
        self.rtsp_url = rtsp_url
        self.test_duration = test_duration
        self.config = RTSPConfig(url=rtsp_url)
    
    def test_connection(self) -> ConnectionTestResult:
        """
        Perform comprehensive RTSP connection test.
        
        Returns:
            ConnectionTestResult: Detailed test results
        """
        print(f"🔍 Testing RTSP connection to: {self.rtsp_url}")
        print("=" * 60)
        
        start_time = time.time()
        recommendations = []
        
        try:
            # Test basic connection
            with RTSPManager(self.config) as rtsp_manager:
                connection_time = time.time() - start_time
                
                print("✅ RTSP connection successful!")
                
                # Get stream properties
                stream_props = rtsp_manager.stream_properties
                print(f"📐 Frame size: {stream_props.width}x{stream_props.height}")
                print(f"🎬 FPS: {stream_props.fps}")
                print(f"📊 Stream type: {'Live' if stream_props.is_live else 'Recorded'}")
                
                # Performance test
                print(f"\n📹 Running performance test for {self.test_duration} seconds...")
                performance_metrics = self._run_performance_test(rtsp_manager)
                
                # Generate recommendations
                recommendations = self._generate_recommendations(stream_props, performance_metrics)
                
                return ConnectionTestResult(
                    success=True,
                    connection_time=connection_time,
                    stream_properties=asdict(stream_props),
                    performance_metrics=performance_metrics,
                    error_message=None,
                    recommendations=recommendations
                )
                
        except Exception as e:
            connection_time = time.time() - start_time
            error_msg = str(e)
            
            print(f"❌ Connection test failed: {error_msg}")
            recommendations = self._generate_error_recommendations(error_msg)
            
            return ConnectionTestResult(
                success=False,
                connection_time=connection_time,
                stream_properties=None,
                performance_metrics=None,
                error_message=error_msg,
                recommendations=recommendations
            )
    
    def _run_performance_test(self, rtsp_manager: RTSPManager) -> Dict[str, Any]:
        """
        Run performance test on the RTSP stream.
        
        Args:
            rtsp_manager: Active RTSP manager instance
            
        Returns:
            Dict[str, Any]: Performance metrics
        """
        frame_count = 0
        start_time = time.time()
        frame_times = []
        
        print("Press 'q' to quit early")
        
        try:
            while time.time() - start_time < self.test_duration:
                frame_start = time.time()
                
                success, frame = rtsp_manager.read_frame()
                if not success or frame is None:
                    print("❌ Failed to read frame during performance test")
                    break
                
                frame_count += 1
                frame_time = time.time() - frame_start
                frame_times.append(frame_time)
                
                # Display frame with FPS
                elapsed_time = time.time() - start_time
                current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
                
                # Add FPS text to frame
                cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Frames: {frame_count}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow("RTSP Performance Test", frame)
                
                # Check for 'q' key to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Performance test interrupted by user")
        finally:
            cv2.destroyAllWindows()
        
        # Calculate metrics
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time if total_time > 0 else 0
        avg_frame_time = sum(frame_times) / len(frame_times) if frame_times else 0
        min_frame_time = min(frame_times) if frame_times else 0
        max_frame_time = max(frame_times) if frame_times else 0
        
        metrics = {
            "total_frames": frame_count,
            "total_time": total_time,
            "average_fps": avg_fps,
            "average_frame_time": avg_frame_time,
            "min_frame_time": min_frame_time,
            "max_frame_time": max_frame_time,
            "frame_time_variance": self._calculate_variance(frame_times)
        }
        
        print(f"\n📊 Performance Results:")
        print(f"   Frames captured: {frame_count}")
        print(f"   Time elapsed: {total_time:.1f} seconds")
        print(f"   Average FPS: {avg_fps:.1f}")
        print(f"   Average frame time: {avg_frame_time*1000:.1f} ms")
        print(f"   Frame time range: {min_frame_time*1000:.1f} - {max_frame_time*1000:.1f} ms")
        
        return metrics
    
    def _calculate_variance(self, values: list) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def _generate_recommendations(self, stream_props, performance_metrics) -> list:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # FPS recommendations
        if performance_metrics['average_fps'] < 15:
            recommendations.append("Consider reducing stream resolution for better performance")
            recommendations.append("Use wired network connection instead of WiFi")
        
        if performance_metrics['average_fps'] < 10:
            recommendations.append("Performance is very low - check network bandwidth")
            recommendations.append("Consider using a lower quality stream")
        
        # Resolution recommendations
        if stream_props.width > 1920 or stream_props.height > 1080:
            recommendations.append("High resolution detected - consider 1080p or lower for better performance")
        
        # Network recommendations
        if performance_metrics['frame_time_variance'] > 0.01:
            recommendations.append("High frame time variance detected - network may be unstable")
            recommendations.append("Consider using a more stable network connection")
        
        # General recommendations
        recommendations.append("Ensure camera and computer are on the same network")
        recommendations.append("Check if other applications are using network bandwidth")
        
        return recommendations
    
    def _generate_error_recommendations(self, error_msg: str) -> list:
        """Generate recommendations for connection errors."""
        recommendations = [
            "Check if the camera IP address is correct",
            "Verify username and password credentials",
            "Ensure the camera is accessible on the network",
            "Try accessing the camera's web interface first",
            "Check if RTSP is enabled on the camera",
            "Verify port 554 is not blocked by firewall",
            "Test with a different RTSP client (e.g., VLC media player)"
        ]
        
        if "timeout" in error_msg.lower():
            recommendations.append("Connection timeout - check network latency")
        
        if "authentication" in error_msg.lower():
            recommendations.append("Authentication failed - verify credentials")
        
        return recommendations
    
    def save_test_report(self, result: ConnectionTestResult, filename: str = "rtsp_test_report.json"):
        """Save test results to a JSON file."""
        report = {
            "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "rtsp_url": self.rtsp_url,
            "test_duration": self.test_duration,
            "result": asdict(result)
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Test report saved to: {filename}")

def main():
    """Main function for standalone connection testing."""
    # Your RTSP URL
    rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
    
    # Create tester and run test
    tester = RTSPConnectionTester(rtsp_url, test_duration=10)
    result = tester.test_connection()
    
    # Display results
    if result.success:
        print("\n🎉 RTSP connection test passed!")
        print("You can now run the vehicle detection system.")
        
        if result.recommendations:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")
        
        # Save report
        tester.save_test_report(result)
        
    else:
        print("\n❌ RTSP connection test failed!")
        print(f"Error: {result.error_message}")
        
        if result.recommendations:
            print("\n💡 Troubleshooting tips:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")

if __name__ == "__main__":
    main() 