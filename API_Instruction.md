# DynamicGroundingDINO API Instructions

## 🔍 Overview

API Collection Here :

https://.postman.co/workspace/My-Workspace~037fa8a1-6581-46ff-83f8-ed6dd846dd8b/collection/31194739-7fe6cb7e-0c6f-45b4-9753-8907129a0d13?action=share&creator=31194739


DAMZ API can detect objects in images by describing them with natural language text queries.

**Base URL:** `https://api.hackathon2025.ai.in.th/team06-1` (or your server address)

## Easiest way to test our API

# Detect cats and dogs in an image
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://images.squarespace-cdn.com/content/v1/607f89e638219e13eee71b1e/1684821560422-SD5V37BAG28BURTLIXUQ/michael-sum-LEpfefQf4rU-unsplash.jpg",
    "text_queries": ["cat", "dog", "the person"],
    "box_threshold": 0.4,
    "text_threshold": 0.3,
    "return_visualization": true
  }'

## 📚 Quick Reference

### Image Object Detection
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API home page with documentation |
| `/health` | GET | Health check and model status |
| `/model/info` | GET | Model information |
| `/detect` | POST | Detect objects from image URL |
| `/detect/upload` | POST | Detect objects from uploaded file |
| `/detect/async` | POST | Async detection from URL (if queue enabled) |
| `/detect/async/upload` | POST | Async detection from upload (if queue enabled) |
| `/task/{task_id}` | GET | Get async task status |

### Video Action Detection
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/video_action/detect` | POST | Detect actions in video from URL (JSON body) |
| `/video_action/detect/upload` | POST | Detect actions in uploaded video file (form data) |
| `/video_action/status` | GET | Video action detection system status |

### Documentation
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/docs` | GET | Interactive API documentation (Swagger) |

---

## 🚀 API Examples

### 1. Health Check

```bash
# Check if the API is running and model is loaded
curl -X GET "https://api.hackathon2025.ai.in.th/team06-1/health"
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "API is running and model is loaded (Worker PID: 123)"
}
```

### 2. Model Information

```bash
# Get model details
curl -X GET "https://api.hackathon2025.ai.in.th/team06-1/model/info"
```

**Response:**
```json
{
  "model_loaded": true,
  "device": "cuda",
  "model_id": "onnx-community/grounding-dino-tiny-ONNX",
  "worker_pid": 123,
  "worker_info": {
    "process_id": 123,
    "python_version": "3.11.0"
  }
}
```

---

## 🎯 Object Detection Examples

### 3. Basic Detection from URL

```bash
# Detect cats and dogs in an image
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "http://images.cocodataset.org/val2017/000000039769.jpg",
    "text_queries": ["cat", "dog"],
    "box_threshold": 0.4,
    "text_threshold": 0.3,
    "return_visualization": true
  }'
```

### 4. Multiple Object Detection

```bash
# Detect multiple objects with custom thresholds
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://picsum.photos/800/600",
    "text_queries": ["person", "car", "bicycle", "dog", "cat"],
    "box_threshold": 0.35,
    "text_threshold": 0.25,
    "return_visualization": true
  }'
```

### 5. Single Query Detection

```bash
# Detect only people in the image
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e",
    "text_queries": "person",
    "box_threshold": 0.5,
    "text_threshold": 0.4,
    "return_visualization": false
  }'
```

### 6. Upload Image File

```bash
# Upload and analyze a local image file
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect/upload" \
  -F "file=@/path/to/your/image.jpg" \
  -F "text_queries=person,car,building" \
  -F "box_threshold=0.4" \
  -F "text_threshold=0.3" \
  -F "return_visualization=true"
```

### 7. Upload with Multiple Queries

```bash
# Upload image with detailed detection
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect/upload" \
  -F "file=@./images/sample.jpg" \
  -F "text_queries=dog,cat,person,car,bicycle,tree,building" \
  -F "box_threshold=0.3" \
  -F "text_threshold=0.25" \
  -F "return_visualization=true"
```

---

## 🎬 Video Action Detection Examples

### 14. Video Action Detection from URL (JSON)

```bash
# Detect "person running" action in a video from URL using JSON
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/video_action/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/running_video.mp4",
    "prompt": "person running",
    "person_weight": 0.2,
    "action_weight": 0.7,
    "context_weight": 0.1,
    "similarity_threshold": 0.5,
    "action_threshold": 0.4,
    "return_timeline": true
  }'
```

### 15. Video Action Detection with Custom Weights (JSON)

```bash
# Focus more on action detection with higher action weight
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/video_action/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/sports_video.mp4",
    "prompt": "person jumping",
    "person_weight": 0.1,
    "action_weight": 0.8,
    "context_weight": 0.1,
    "similarity_threshold": 0.4,
    "action_threshold": 0.3,
    "return_timeline": true
  }'
```

### 16. Upload Video File for Action Detection (Form Data)

```bash
# Upload and analyze a local video file using form data
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/video_action/detect/upload" \
  -F "file=@/path/to/your/video.mp4" \
  -F "prompt=person dancing" \
  -F "person_weight=0.3" \
  -F "action_weight=0.6" \
  -F "context_weight=0.1" \
  -F "similarity_threshold=0.5" \
  -F "action_threshold=0.4" \
  -F "return_timeline=true"
```

### 17. Complex Action Detection with Context (Form Data)

```bash
# Detect complex actions with context emphasis using file upload
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/video_action/detect/upload" \
  -F "file=@/path/to/sports_compilation.mp4" \
  -F "prompt=person playing basketball" \
  -F "person_weight=0.2" \
  -F "action_weight=0.6" \
  -F "context_weight=0.2" \
  -F "similarity_threshold=0.5" \
  -F "action_threshold=0.4" \
  -F "return_timeline=true"
```
    "action_threshold": 0.4,
    "return_timeline": true
  }'
```

### 18. Check Video Action Detection Status

```bash
# Check if video action detection is available
curl -X GET "https://api.hackathon2025.ai.in.th/team06-1/video_action/status"
```

**Response:**
```json
{
  "video_action_available": true,
  "detector_loaded": true,
  "supported_formats": ["mp4", "avi", "mov", "mkv", "webm"],
  "features": {
    "action_detection": true,
    "timeline_visualization": true,
    "custom_weights": true,
    "parallel_processing": true
  },
  "model_info": {
    "blip_model": "Salesforce/blip-image-captioning-large",
    "similarity_model": "all-MiniLM-L6-v2",
    "nlp_available": true
  }
}
```

### Video Action Detection Response Format

```json
{
  "success": true,
  "job_id": "job_20250803_143022",
  "video_path": "https://example.com/video.mp4",
  "prompt": "person running",
  "action_verb": "running",
  "timestamp": "2025-08-03T14:30:22.123456",
  "video_duration": 30.5,
  "stats": {
    "total_frames": 30,
    "total_detections": 30,
    "passed_detections": 15,
    "success_rate": 50.0,
    "segments_found": 2
  },
  "passed_detections": [
    {
      "timestamp": 5.2,
      "frame_idx": 156,
      "confidence": 0.78,
      "blip_description": "a person is running on a track",
      "similarity_scores": {
        "person": 0.85,
        "action": 0.92,
        "context": 0.45,
        "weighted": 0.78
      },
      "passed": true
    }
  ],
  "segments": [
    {
      "start_time": 5.0,
      "end_time": 12.5,
      "confidence": 0.76,
      "frame_count": 8,
      "action_label": "running",
      "detections": [...]
    }
  ],
  "timeline_visualization": "./results/visualizations/job_20250803_143022_timeline.png"
}
```

---

## 🔄 Async Processing (If Queue Enabled)

### 8. Submit Async Detection Task

```bash
# Submit a task for async processing
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect/async" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "http://images.cocodataset.org/val2017/000000039769.jpg",
    "text_queries": ["cat", "remote control", "person"],
    "box_threshold": 0.4,
    "text_threshold": 0.3,
    "return_visualization": true,
    "priority": 5
  }'
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "status": "submitted",
  "message": "Task submitted for async processing"
}
```

### 9. Check Task Status

```bash
# Check the status of an async task
curl -X GET "https://api.hackathon2025.ai.in.th/team06-1/task/task_abc123"
```

**Responses:**

**Processing:**
```json
{
  "task_id": "task_abc123",
  "status": "processing",
  "progress": 50,
  "stage": "model_inference",
  "message": "Processing detection..."
}
```

**Completed:**
```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "result": {
    "success": true,
    "num_detections": 2,
    "detections": [...]
  }
}
```

### 10. Queue Status

```bash
# Check queue statistics
curl -X GET "https://api.hackathon2025.ai.in.th/team06-1/queue/status"
```

---

## 📊 Response Format

### Successful Detection Response

```json
{
  "success": true,
  "num_detections": 2,
  "detections": [
    {
      "id": 1,
      "label": "cat",
      "confidence": 0.89,
      "bounding_box": {
        "x_min": 100.5,
        "y_min": 150.2,
        "x_max": 250.8,
        "y_max": 300.1,
        "width": 150.3,
        "height": 149.9
      }
    },
    {
      "id": 2,
      "label": "person",
      "confidence": 0.76,
      "bounding_box": {
        "x_min": 300.0,
        "y_min": 50.0,
        "x_max": 450.0,
        "y_max": 400.0,
        "width": 150.0,
        "height": 350.0
      }
    }
  ],
  "image_size": {
    "width": 800,
    "height": 600
  },
  "queries": ["cat", "person"],
  "thresholds": {
    "box_threshold": 0.4,
    "text_threshold": 0.3
  },
  "visualization": {
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
    "format": "png"
  }
}
```

---

## 🛠 Advanced Usage

### 11. High Precision Detection

```bash
# Use higher thresholds for more precise detections
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "text_queries": ["person"],
    "box_threshold": 0.7,
    "text_threshold": 0.6,
    "return_visualization": true
  }'
```

### 12. Multiple Specific Objects

```bash
# Detect specific items in a room
curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/room.jpg",
    "text_queries": ["chair", "table", "laptop", "book", "cup", "phone"],
    "box_threshold": 0.3,
    "text_threshold": 0.25,
    "return_visualization": true
  }'
```

### 13. Batch Processing Script

```bash
#!/bin/bash
# Process multiple images

images=(
  "https://example.com/image1.jpg"
  "https://example.com/image2.jpg"
  "https://example.com/image3.jpg"
)

for image_url in "${images[@]}"; do
  echo "Processing: $image_url"
  curl -X POST "https://api.hackathon2025.ai.in.th/team06-1/detect" \
    -H "Content-Type: application/json" \
    -d "{
      \"image_url\": \"$image_url\",
      \"text_queries\": [\"person\", \"car\", \"dog\"],
      \"box_threshold\": 0.4,
      \"text_threshold\": 0.3,
      \"return_visualization\": false
    }" | jq '.num_detections'
  echo "---"
done
```

---

## � Postman Usage Guide

### For Video File Upload in Postman

1. **Set Request Method**: POST
2. **Set URL**: `https://api.hackathon2025.ai.in.th/team06-1/video_action/detect/upload`
3. **Set Headers**: Remove any Content-Type header (Postman will set it automatically for form-data)
4. **Body Configuration**:
   - Select **form-data** (not raw/JSON)
   - Add key-value pairs:

| Key | Type | Value | Example |
|-----|------|-------|---------|
| `file` | File | Select your video file | `sample_video.mp4` |
| `prompt` | Text | Action description | `person running` |
| `person_weight` | Text | 0.2 | `0.2` |
| `action_weight` | Text | 0.7 | `0.7` |
| `context_weight` | Text | 0.1 | `0.1` |
| `similarity_threshold` | Text | 0.5 | `0.5` |
| `action_threshold` | Text | 0.4 | `0.4` |
| `return_timeline` | Text | true | `true` |

### For URL-based Detection in Postman

1. **Set Request Method**: POST
2. **Set URL**: `https://api.hackathon2025.ai.in.th/team06-1/video_action/detect`
3. **Set Headers**: `Content-Type: application/json`
4. **Body Configuration**:
   - Select **raw** and **JSON**
   - Use JSON format:

```json
{
  "video_url": "https://example.com/your_video.mp4",
  "prompt": "person running",
  "person_weight": 0.2,
  "action_weight": 0.7,
  "context_weight": 0.1,
  "similarity_threshold": 0.5,
  "action_threshold": 0.4,
  "return_timeline": true
}
```

---

## �🔧 Parameters Reference

### Image Detection Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|--------|-------------|
| `image_url` | string | - | Valid URL | Image URL to analyze |
| `text_queries` | string/array | - | - | Objects to detect |
| `box_threshold` | float | 0.4 | 0.0-1.0 | Bounding box confidence |
| `text_threshold` | float | 0.3 | 0.0-1.0 | Text matching confidence |
| `return_visualization` | boolean | true | - | Return annotated image |
| `async_processing` | boolean | false | - | Use async queue |
| `priority` | integer | 5 | 0-9 | Task priority (async only) |

### Video Action Detection Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|--------|-------------|
| **JSON Request (URL-based)** | | | | |
| `video_url` | string | - | Valid URL | Video URL to analyze |
| `prompt` | string | - | - | Action description (e.g., "person running") |
| `person_weight` | float | 0.2 | 0.0-1.0 | Weight for person detection component |
| `action_weight` | float | 0.7 | 0.0-1.0 | Weight for action detection component |
| `context_weight` | float | 0.1 | 0.0-1.0 | Weight for context detection component |
| `similarity_threshold` | float | 0.5 | 0.0-1.0 | Overall similarity threshold |
| `action_threshold` | float | 0.4 | 0.0-1.0 | Action-specific threshold |
| `return_timeline` | boolean | true | - | Return timeline visualization |
| **Form Data (File Upload)** | | | | |
| `file` | file | - | - | Video file to upload (MP4, AVI, MOV, etc.) |
| `prompt` | string | - | - | Action description (e.g., "person running") |
| `person_weight` | float | 0.2 | 0.0-1.0 | Weight for person detection component |
| `action_weight` | float | 0.7 | 0.0-1.0 | Weight for action detection component |
| `context_weight` | float | 0.1 | 0.0-1.0 | Weight for context detection component |
| `similarity_threshold` | float | 0.5 | 0.0-1.0 | Overall similarity threshold |
| `action_threshold` | float | 0.4 | 0.0-1.0 | Action-specific threshold |
| `return_timeline` | boolean | true | - | Return timeline visualization |

**Usage Notes:**
- For URL-based detection: Use JSON request body with `Content-Type: application/json`
- For file upload: Use form data with `Content-Type: multipart/form-data`
- Only provide one input method per request (either JSON with video_url OR form data with file)

### Upload Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `file` | file | Image file (JPEG, PNG, etc.) or Video file (MP4, AVI, etc.) |
| `text_queries` | string | Comma-separated objects to detect (images only) |
| `prompt` | string | Action description for video detection |
| `video_url` | string | Video URL for video action detection (alternative to file) |
| `box_threshold` | float | Bounding box confidence threshold (images only) |
| `text_threshold` | float | Text matching confidence threshold (images only) |
| `return_visualization` | boolean | Return annotated image/timeline |

---

## ❌ Error Handling

### Common Error Responses

```bash
# Invalid image URL
{
  "success": false,
  "error": "Failed to load image from URL: HTTP 404",
  "num_detections": 0,
  "detections": []
}

# Invalid parameters
{
  "detail": "box_threshold must be between 0.0 and 1.0"
}

# Model not loaded
{
  "status": "loading",
  "model_loaded": false,
  "message": "API is running but model is still loading"
}
```

---

## 🎨 Example Text Queries

### Image Object Detection

#### General Objects
- `"person"`, `"people"`
- `"car"`, `"vehicle"`, `"automobile"`
- `"dog"`, `"cat"`, `"animal"`
- `"building"`, `"house"`, `"structure"`

#### Specific Items
- `"laptop"`, `"computer"`, `"smartphone"`
- `"chair"`, `"table"`, `"sofa"`
- `"tree"`, `"flower"`, `"plant"`
- `"ball"`, `"toy"`, `"book"`

#### Descriptive Queries
- `"person wearing red shirt"`
- `"small dog"`
- `"blue car"`
- `"woman with glasses"`

### Video Action Detection

#### Basic Actions
- `"person running"`
- `"person walking"`
- `"person jumping"`
- `"person dancing"`

#### Sports Actions
- `"person playing basketball"`
- `"person kicking ball"`
- `"person swimming"`
- `"person riding bicycle"`

#### Complex Actions
- `"person cooking food"`
- `"person driving car"`
- `"person playing guitar"`
- `"person writing on paper"`

#### Context-Rich Actions
- `"person running in park"`
- `"person dancing on stage"`
- `"person swimming in pool"`
- `"person playing basketball in court"`

---

## 📈 Performance Tips

1. **Optimal Thresholds:**
   - `box_threshold: 0.3-0.5` for general detection
   - `text_threshold: 0.25-0.4` for text matching

2. **Image Size:**
   - Works best with images 800x600 to 1920x1080
   - Larger images take more processing time

3. **Query Optimization:**
   - Use specific, descriptive terms
   - Avoid overly generic queries like "object" or "thing"
   - Combine related objects in one request

4. **Async Processing:**
   - Use for large images or batch processing
   - Set appropriate priority levels
   - Monitor queue status for optimization

---

## 🔗 Interactive Documentation

Visit these URLs for interactive API exploration:

- **Swagger UI:** `https://api.hackathon2025.ai.in.th/team06-1/docs`
- **ReDoc:** `https://api.hackathon2025.ai.in.th/team06-1/redoc`
- **API Home:** `https://api.hackathon2025.ai.in.th/team06-1/`

---

## 📞 Support

For issues or questions:
1. Check the health endpoint: `GET /health`
2. Review the logs for error messages
3. Verify image URLs are accessible
4. Ensure proper JSON formatting in requests

The API supports both synchronous and asynchronous processing with comprehensive error handling and detailed response formats.
