from datetime import datetime
from flask import Blueprint, Response, jsonify, request
from remote_camera import RemoteCameraManager

# Create blueprint
remote_bp = Blueprint('remote_camera', __name__)

# Initialize camera manager
camera_manager = RemoteCameraManager()

@remote_bp.route('/api/start_camera', methods=['POST'])
def start_camera():
    """Start camera endpoint"""
    try:
        success, message = camera_manager.start_camera()
        if success:
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'error', 'message': message}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@remote_bp.route('/api/stop_camera', methods=['POST'])
def stop_camera():
    """Stop camera endpoint"""
    try:
        success, message = camera_manager.stop_camera()
        if success:
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'error', 'message': message}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@remote_bp.route('/api/camera_status', methods=['GET'])
def camera_status():
    """Get camera status"""
    try:
        is_active = camera_manager.is_camera_active()
        return jsonify({
            'status': 'success',
            'camera_active': is_active,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@remote_bp.route('/api/video_feed')
def video_feed():
    """Video feed endpoint with optional annotations"""
    try:
        print("Video feed endpoint called")
        
        if not camera_manager.is_camera_active():
            print("Camera not initialized")
            return jsonify({'error': 'Camera not started'}), 400
        
        # Get annotations parameter from query string (default: True)
        annotations_enabled = request.args.get('annotations', 'true').lower() == 'true'
        
        print(f"Starting video stream... (annotations: {annotations_enabled})")
        return Response(camera_manager.generate_frames(),   # pass annotations_enabled as a param later
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error in video feed: {e}")
        return jsonify({'error': str(e)}), 500

@remote_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'remote-camera-backend',
        'timestamp': datetime.now().isoformat()
    }), 200

# Cleanup on app shutdown
@remote_bp.teardown_appcontext
def cleanup(error):
    """Cleanup resources"""
    try:
        camera_manager.stop_camera()
    except:
        pass

@remote_bp.route('/api/shutdown', methods=['POST'])
def shutdown_server():
    """Shutdown server and cleanup resources"""
    try:
        # Get the shutdown function from werkzeug
        from werkzeug.serving import make_server
        import os
        import signal
        
        # Send shutdown signal
        def shutdown():
            os.kill(os.getpid(), signal.SIGINT)
        
        # Schedule shutdown after response is sent
        import threading
        threading.Timer(1.0, shutdown).start()
        
        return jsonify({
            'status': 'success', 
            'message': 'Server shutting down...'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
