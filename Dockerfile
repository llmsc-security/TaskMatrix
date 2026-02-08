# Dockerfile for TaskMatrix Visual ChatGPT
# Based on Python 3.11-slim for optimal size and compatibility

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY visual_chatgpt.py .
COPY assets/ ./assets/

# Create checkpoints directory (will be used at runtime)
RUN mkdir -p /app/checkpoints

# Expose the container port (Gradio default is 7860, but app uses 7861)
EXPOSE 11220

# Set entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
