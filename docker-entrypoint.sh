#!/bin/bash
set -e

echo "🔍 Starting DynamicGroundingDINO API with debugging..."
echo "=================================================="

# Print environment info
echo "📋 Environment Info:"
echo "Working directory: $(pwd)"
echo "User: $(whoami)"
echo "Python version: $(python --version)"
echo "Available files: $(ls -la)"
echo ""

# Check if critical files exist
echo "📁 Checking critical files:"
for file in server.py model.py video_action_model.py queue_worker_rabbitmq.py requirements.txt; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done
echo ""

# Test Python imports
echo "🐍 Testing Python imports:"
python -c "import sys; print('Python path:', sys.path)" || echo "❌ Python path failed"
python -c "import fastapi; print('✅ FastAPI imported')" || echo "❌ FastAPI import failed"
python -c "import torch; print('✅ PyTorch imported')" || echo "❌ PyTorch import failed"
python -c "import cv2; print('✅ OpenCV imported')" || echo "❌ OpenCV import failed"
python -c "import pika; print('✅ Pika imported')" || echo "❌ Pika import failed"
python -c "from model import ModelManager; print('✅ Model imported')" || echo "❌ Model import failed"
python -c "from video_action_model import ActionDetector; print('✅ Video action model imported')" || echo "❌ Video action model import failed"
python -c "from queue_worker_rabbitmq import TaskManager; print('✅ Queue worker imported')" || echo "❌ Queue worker import failed"
python -c "from youtube_downloader import download_video_from_url; print('✅ Video downloader imported')" || echo "❌ Video downloader import failed"
echo ""

# Check memory and disk space
echo "💾 System Resources:"
echo "Memory: $(free -h | grep Mem | awk '{print $2 " total, " $3 " used, " $7 " available"}')"
echo "Disk: $(df -h /app | tail -1 | awk '{print $2 " total, " $3 " used, " $4 " available"}')"
echo ""

echo "🚀 Starting server..."
echo "===================="

# Try to start with simple uvicorn first
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --workers 1 --log-level debug
