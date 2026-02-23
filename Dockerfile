FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV and git
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    git \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install groundingdino from GitHub using wget
RUN wget -q https://github.com/IDEA-Research/GroundingDINO/archive/refs/heads/main.zip -O /tmp/groundingdino.zip \
    && unzip -q /tmp/groundingdino.zip -d /tmp \
    && pip install --no-cache-dir /tmp/GroundingDINO-main \
    && rm -rf /tmp/groundingdino.zip /tmp/GroundingDINO-main

# Copy application code
COPY visual_chatgpt.py .
COPY assets/ ./assets/
COPY http_server.py .

# Create checkpoints directory
RUN mkdir -p /app/checkpoints

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 11220
ENTRYPOINT ["./entrypoint.sh"]
