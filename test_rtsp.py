#!/usr/bin/env python3
"""
RTSP Connection Test Script
Simple script to test RTSP camera connectivity.

Usage:
    python3 test_rtsp.py

Author: Academic Research Team
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rtsp_detection.connection_tester import RTSPConnectionTester

def main():
    """Main function for RTSP connection testing."""
    print("🔍 RTSP Connection Test")
    print("=" * 50)
    
    # Your RTSP URL - modify this for your camera
    rtsp_url = "rtsp://admin:CamPassword_0718@192.168.0.101:554"
    
    print(f"Testing connection to: {rtsp_url}")
    print()
    
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
        
        # Save detailed report
        tester.save_test_report(result)
        
    else:
        print("\n❌ RTSP connection test failed!")
        print(f"Error: {result.error_message}")
        
        if result.recommendations:
            print("\n💡 Troubleshooting tips:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 