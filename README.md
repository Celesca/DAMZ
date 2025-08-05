# DAMZ (Detect-Anything-Model with Zero-shot Object Detection) 

## by Ex_Machina Team 06

### Objective

Nowadays, people in Thailand are developing a wide range of applications for various industries, including manufacturing, agriculture, healthcare, and security. However, a common challenge faced by these applications is the need for flexible and accurate object detection systems. Traditional object detection models require extensive retraining and large labeled datasets for each new object or scenario, which is time-consuming and costly.

Many Thai industries need to detect new or rare objects that may not be present in standard datasets. This limitation slows down innovation and makes it difficult to adapt AI solutions to rapidly changing environments or specific local needs.

### Solution: DAMZ - Detect-Anything-Model with Zero-shot Object Detection

DAMZ (Detect-anything-model with Zero-shot object detection) addresses this challenge by enabling detection of arbitrary objects without the need for retraining. Leveraging advanced vision-language models, DAMZ can understand textual queries and detect objects in images based on descriptions, even if those objects were never seen during training.

#### Key Features

- **Zero-shot detection:** Detect objects using natural language queries without retraining.
- **Flexible API:** Easily integrate with existing applications via RESTful endpoints.
- **Queue-based processing:** Supports asynchronous task submission and scalable processing using RabbitMQ.
- **GPU acceleration:** Optimized for H100 GPUs for fast inference.
- **Industry-ready:** Designed for real-world deployment in Thai industrial environments.

#### Example Use Cases

- Detecting new machinery or equipment in factory images.
- Locating specific medical instruments in hospital scenes.
- Security applications for identifying suspicious objects.

### How It Works

1. **Submit an image and text query** (e.g., "Find all forklifts in this warehouse photo") via the API.
2. **DAMZ processes the request** using zero-shot object detection.
3. **Results are returned** with bounding boxes and confidence scores for detected objects.

---

## API Endpoints

### 0. `/health`
Healthcheck the system.

### 1. `/detect` (Image Zero-shot Object Detection)
Detect objects in an image using zero-shot prompting.

**Method:** `POST`

**Input:**
- `image` (form-data): The image file to analyze (JPEG, PNG, etc.)
- `text_queries` (form-data or JSON): Comma-separated or JSON array of text queries for object detection
- `box_threshold` (form-data or JSON): Confidence threshold for bounding boxes (default: 0.4)
- `text_threshold` (form-data or JSON): Confidence threshold for text matching (default: 0.4)
- `return_visualization` (form-data or JSON): Whether to return visualization image (default: true)
- `async_processing` (form-data or JSON): Whether to process asynchronously using queue (default: false)
- `priority` (form-data or JSON): Task priority (default: 5)

**Example JSON:**
```json
{
  "image_url": "https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aHVtYW4lMjBmYWNlfGVufDB8fDB8fHww",
  "text_queries": ["a cat", "a remote control", "a person"],
  "box_threshold": 0.4,
  "text_threshold": 0.4,
  "return_visualization": true,
  "async_processing": false,
  "priority": 5
}
```

**Response:**
- Bounding boxes, confidence scores, and (optionally) visualization image.

---

### 2. `/detect/upload` (Image Upload)
Detect objects from an uploaded image file. Accepts the same parameters as `/detect/` but uses file upload.

**Method:** `POST`

**Input:**
- `image` (form-data): The image file to analyze
- Other parameters as above

---

### 3. `/video_action/detect/upload` (Video Zero-shot Object Detection)
Detect objects in video using zero-shot prompting with contextual understanding.

**Method:** `POST`

**Input:**
- `file` (form-data): The video file to analyze (MP4, AVI, etc.)
- `prompt` (form-data): Text query for object detection (e.g., "a person")
- `person_weight` (form-data): Weight for person detection confidence (default: 0.3)
- `action_weight` (form-data): Weight for action recognition (default: 0.6)
- `context_weight` (form-data): Weight for contextual understanding (default: 0.1)
- `similarity_threshold` (form-data): Minimum similarity score for detection (default: 0.5)
- `action_threshold` (form-data): Minimum confidence for action detection (default: 0.4)
- `return_timeline` (form-data): Whether to return frame-by-frame timeline (default: true)

**Response:**
- Frame-by-frame object detections with bounding boxes
- Confidence scores for each detection
- Optional timeline of detected objects throughout video
- Optional visualization video with annotations

---

---

### Challenge :

1. The accuracy of the base-model that cannot rised because of the zero-shot training.

2. The sentence object detection in video 

The way to did the video object detection in zero-shot training. If the object is like the single word ("Person", "Cat") it's too normal and the YOLO and do it. So we decided to did the "Sentence object detection" to find the bounding boxes that are mutual and can specify the object.

### Connection to AI4Thais

1. English-Thailand Translation

2. Text-Cleasing (NLP)
