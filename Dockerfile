# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Add labels for better image management
LABEL maintainer="team06" \
      description="DynamicGroundingDINO API with FastAPI and worker support" \
      version="2.0.0"

# Set working directory
WORKDIR /app

# Create cache directories
RUN mkdir -p /app/cache/transformers /app/cache/huggingface /app/cache/torch

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (cached layer)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    wget \
    curl \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Install spaCy English model for video action detection
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY model.py .
COPY server.py .
COPY video_action_model.py .
COPY youtube_downloader.py .
COPY queue_worker_rabbitmq.py .
COPY gunicorn.conf.py .
COPY start_server.py .
COPY docker-entrypoint.sh .

# Make scripts executable
RUN chmod +x start_server.py docker-entrypoint.sh

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Environment variables for production
ENV MODE=prod
ENV WORKERS=auto
ENV MAX_REQUESTS=1000
ENV WORKER_TIMEOUT=120

# Run the application with debugging entry point
CMD ["./docker-entrypoint.sh"]
