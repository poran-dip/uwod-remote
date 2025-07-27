#!/bin/bash

echo "Setting up Underwater Object Detection Remote Server..."

# update and install system OpenCV (fast!)
echo "Installing system OpenCV..."
sudo apt update
sudo apt install -y python3-opencv

# install python packages
echo "Installing Python packages..."
pip install -r requirements.txt

# run device check (opencv, realsense, cuda)
echo "Running device check..."
python3 check_device.py
if [ $? -ne 0 ]; then
    echo "Error: Critical components missing or CUDA check failed!"
    echo "Make sure JetPack 4.6+ and compatible PyTorch are installed."
    exit 1
fi

echo "Setup complete! Run 'python app.py' to start the server."
