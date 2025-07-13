from flask import Flask
from jetson_routes import jetson_bp, camera_manager

app = Flask(__name__)

# Register the Jetson camera blueprint
app.register_blueprint(jetson_bp)

if __name__ == '__main__':
    try:
        print("Starting Jetson Camera Backend...")
        print("Endpoints available:")
        print("  POST /api/start_camera - Start camera")
        print("  POST /api/stop_camera - Stop camera") 
        print("  GET  /api/camera_status - Check camera status")
        print("  GET  /api/video_feed - Video stream")
        print("  GET  /api/health - Health check")
        
        # Run on all interfaces so it's accessible from other devices
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting server: {e}")