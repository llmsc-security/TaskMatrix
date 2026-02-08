#!/bin/bash
# Entrypoint script for TaskMatrix Visual ChatGPT

cd /app

# Set default port from environment variable
WEB_PORT=${WEB_PORT:-11220}
export WEB_PORT

echo "Starting TaskMatrix Visual ChatGPT on port ${WEB_PORT}..."
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0"
