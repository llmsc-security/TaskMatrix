#!/bin/bash
set -e

echo "Starting TaskMatrix Visual ChatGPT on port 11220..."
cd /app

# Start Gradio app on port 11220
export WEB_PORT=11220
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0" --port 11220 &
GRADIO_PID=$!

# Wait a bit for Gradio to start
sleep 5

# Start HTTP server on port 11220
export HTTP_PORT=11220
python http_server.py &
HTTP_PID=$!

echo "Gradio PID: $GRADIO_PID, HTTP Server PID: $HTTP_PID"

# Wait for both processes
wait
