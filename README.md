# Underwater Object Detection — Remote Server

This repository serves as the companion backend for [UWOD-RC](https://github.com/poran-dip/uwod-rc), the main control interface for real-time object detection.

This backend is designed to be deployed on a Single Board Computer (SBC) such as the Jetson Nano. It handles camera streaming and optionally performs YOLOv8-based object detection, making the results accessible to the main controller.

---

## Setup

To set up the server on a Jetson Nano (or other compatible SBC), follow these steps:

```bash
git clone https://github.com/poran-dip/uwod-remote.git
cd uwod-remote
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Ensure your camera is connected and accessible via OpenCV.

---

## Integration with UWOD-RC

Once the server is running, obtain its network URL (e.g., `http://jetson-nano.local:5000`) and enter it in the UI of the UWOD-RC project.

Supported functionality includes:

* Starting and stopping camera detection
* Capturing annotated snapshots
* Recording annotated video streams

---

## Notes

* The default YOLOv8 model used is `yolov8n.pt`. This can be adjusted in `config.py`.
* Video stream is available at `/api/video_feed`
* Fully compatible with the Flask + React frontend provided by [uwod-rc](https://github.com/poran-dip/uwod-rc)
