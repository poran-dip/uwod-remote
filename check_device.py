#!/usr/bin/env python3
"""
CUDA and device availability checker for Jetson Nano
"""

import sys

def check_cuda():
    """Check CUDA availability"""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        device_count = torch.cuda.device_count()
        
        print(f"CUDA Available: {cuda_available}")
        if cuda_available:
            print(f"CUDA Devices: {device_count}")
            for i in range(device_count):
                device_name = torch.cuda.get_device_name(i)
                print(f"  Device {i}: {device_name}")
        else:
            print("CUDA not available - will use CPU")
            
        return cuda_available
    except ImportError:
        print("PyTorch not installed - CUDA check skipped")
        return True  # Don't fail setup if PyTorch isn't installed yet

def check_opencv():
    """Check OpenCV installation"""
    try:
        import cv2
        print(f"OpenCV Version: {cv2.__version__}")
        return True
    except ImportError:
        print("ERROR: OpenCV not found")
        return False

def check_realsense():
    """Check RealSense SDK"""
    try:
        import pyrealsense2 as rs
        print("RealSense SDK: Available")
        return True
    except ImportError:
        print("ERROR: RealSense SDK not found")
        return False

if __name__ == "__main__":
    print("=== Device Check ===")
    
    # Check critical components
    opencv_ok = check_opencv()
    realsense_ok = check_realsense()
    cuda_ok = check_cuda()
    
    print("\n=== Summary ===")
    print(f"OpenCV: {'✓' if opencv_ok else '✗'}")
    print(f"RealSense: {'✓' if realsense_ok else '✗'}")
    print(f"CUDA: {'✓' if cuda_ok else '⚠ (CPU mode)'}")
    
    # Only fail if critical components are missing
    if not opencv_ok or not realsense_ok:
        print("\nERROR: Critical components missing!")
        sys.exit(1)
    
    print("\nDevice check completed successfully!")
    sys.exit(0)
