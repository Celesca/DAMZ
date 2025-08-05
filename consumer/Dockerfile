FROM nvcr.io/nvidia/cuda:12.1.1-base-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgtk-3-0 \
    libgl1-mesa-glx \
    libfontconfig1 \
    libxrender1 \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python

# Create cache directories
RUN mkdir -p /app/cache/transformers /app/cache/huggingface /app/cache/torch

# Copy requirements from consumer directory
COPY consumer/requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA support
RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Install spaCy English model for video action detection
RUN python3 -m spacy download en_core_web_sm

# Copy application code
COPY model.py .
COPY video_action_model.py .
COPY queue_worker_rabbitmq.py .
COPY consumer/consumer.py .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Command to run the consumer
CMD ["python", "consumer.py"]