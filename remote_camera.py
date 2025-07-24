import threading
import time
import cv2
# from ultralytics import YOLO

class RemoteCameraManager:
    def __init__(self):
        self.model = None
        self.camera = None
        self.camera_lock = threading.Lock()
        self.is_active = False
        
        # Camera settings
        self.camera_width = 640
        self.camera_height = 480
        self.camera_fps = 30
        self.jpeg_quality = 80
    
    """def load_model(self):"""
    """Load YOLO model"""
    """
        try:
            print("Loading YOLOv5 model...")
            # Use YOLOv5n nano for performance
            self.model = YOLO('yolov5nu.pt')
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    """
    def start_camera(self):
        """Start camera capture"""
        try:
            print("Starting camera...")
            """""
            # Load model if not loaded
            if self.model is None:
                if not self.load_model():
                    return False, "Failed to load model"
            """
            with self.camera_lock:
                if self.is_active:
                    return False, "Camera already active"
                
                # Try different camera indices for remote camera manager
                # 0 = USB camera, 1 = CSI camera (if available)
                camera_indices = [0, 1]
                
                for idx in camera_indices:
                    self.camera = cv2.VideoCapture(idx)
                    if self.camera.isOpened():
                        print(f"Camera opened successfully on index {idx}")
                        break
                    else:
                        self.camera = None
                
                if self.camera is None:
                    return False, "Failed to open any camera"
                
                # Set camera properties
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
                self.camera.set(cv2.CAP_PROP_FPS, self.camera_fps)
                
                # Test frame capture
                ret, frame = self.camera.read()
                if not ret or frame is None:
                    self.camera.release()
                    self.camera = None
                    return False, "Camera opened but failed to capture frame"
                
                self.is_active = True
                print("Camera started successfully")
                return True, "Camera started successfully"
                
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False, str(e)
    
    def stop_camera(self):
        """Stop camera capture"""
        try:
            with self.camera_lock:
                if not self.is_active:
                    return False, "Camera not active"
                
                if self.camera is not None:
                    self.camera.release()
                    self.camera = None
                
                self.is_active = False
                print("Camera stopped")
                return True, "Camera stopped successfully"
                
        except Exception as e:
            print(f"Error stopping camera: {e}")
            return False, str(e)
    
    def is_camera_active(self):
        """Check if camera is active"""
        return self.is_active and self.camera is not None
    
    def generate_frames(self, annotations_enabled=True):
        """Generate frames with optional annotations"""
        print(f"Starting frame generation... (annotations: {annotations_enabled})")
        failed_frames = 0
        max_failed_frames = 30
        
        while True:
            if not self.is_camera_active():
                print("Camera stopped, ending stream...")
                break
            
            try:
                with self.camera_lock:
                    if self.camera is None:
                        break
                    ret, frame = self.camera.read()
                
                if not ret or frame is None:
                    failed_frames += 1
                    print(f"Failed to capture frame ({failed_frames}/{max_failed_frames})")
                    
                    if failed_frames >= max_failed_frames:
                        print("Too many failed frames, ending stream...")
                        break
                    
                    time.sleep(0.1)
                    continue
                
                # Reset failed frames counter on successful frame
                failed_frames = 0
                """"
                # Apply YOLO detection only if annotations are enabled
                if annotations_enabled and self.model is not None:
                    results = self.model(frame, verbose=False)
                    annotated_frame = results[0].plot()
                else:
                    annotated_frame = frame
                """
                
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame, # use annotated_frame later
                                        [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality])
                
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                else:
                    print("Failed to encode frame")
                    break
                    
            except Exception as e:
                print(f"Error processing frame: {e}")
                break
        
        print("Frame generation ended")
