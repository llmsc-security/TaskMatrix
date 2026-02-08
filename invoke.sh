#!/bin/bash
# Build and run Docker container for TaskMatrix Visual ChatGPT

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Build the Docker image
echo "Building Docker image..."
docker build -t taskmatrix-vchatgpt:latest .

# Run the container with port mapping
echo "Starting container..."
docker run --gpus all -p 11220:7861 \
    --name taskmatrix-vchatgpt \
    -v "$SCRIPT_DIR/checkpoints:/app/checkpoints" \
    -v "$SCRIPT_DIR/assets:/app/assets" \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    --rm -it \
    taskmatrix-vchatgpt:latest
