import os
import json
import uuid
import requests
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Team06 Grounding DINO Proxy", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GROUNDING_DINO_HOST = os.getenv('GROUNDING_DINO_HOST', 'team06-grounding-dino')
GROUNDING_DINO_PORT = int(os.getenv('GROUNDING_DINO_PORT', 8000))

# Pydantic models
class DetectionRequest(BaseModel):
    image_url: str
    text_queries: Union[str, List[str]]
    box_threshold: Optional[float] = 0.4
    text_threshold: Optional[float] = 0.3
    return_visualization: Optional[bool] = True
    async_processing: Optional[bool] = False
    priority: Optional[int] = 5

class AsyncDetectionRequest(BaseModel):
    image_url: str
    text_queries: Union[str, List[str]]
    box_threshold: Optional[float] = 0.4
    text_threshold: Optional[float] = 0.3
    return_visualization: Optional[bool] = True
    priority: Optional[int] = 5

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Team06 Grounding DINO Proxy",
        "version": "1.0.0",
        "backend": f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}",
        "endpoints": {
            "health": "/health",
            "detect": "/detect",
            "detect_upload": "/detect/upload",
            "detect_async": "/detect/async",
            "detect_async_upload": "/detect/async/upload",
            "task_status": "/task/{task_id}",
            "queue_status": "/queue/status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check - proxy to backend"""
    try:
        response = requests.get(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/health",
            timeout=30
        )
        return response.json()
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service unavailable: {str(e)}")

@app.post("/detect")
@app.post("/detect/")
async def detect_objects_from_url(request: DetectionRequest):
    """Proxy detection request to backend"""
    try:
        response = requests.post(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/detect",
            json=request.dict(),
            timeout=300
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.post("/detect/upload")
@app.post("/detect/upload/")
async def detect_objects_from_upload(
    file: UploadFile = File(...),
    text_queries: str = Form(...),
    box_threshold: float = Form(0.4),
    text_threshold: float = Form(0.3),
    return_visualization: bool = Form(True),
    async_processing: bool = Form(False),
    priority: int = Form(5)
):
    """Proxy upload detection request to backend"""
    try:
        # Prepare form data for backend
        files = {"file": (file.filename, await file.read(), file.content_type)}
        data = {
            "text_queries": text_queries,
            "box_threshold": box_threshold,
            "text_threshold": text_threshold,
            "return_visualization": return_visualization,
            "async_processing": async_processing,
            "priority": priority
        }
        
        response = requests.post(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/detect/upload",
            files=files,
            data=data,
            timeout=300
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Upload request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.post("/detect/async")
async def submit_async_detection_url(request: AsyncDetectionRequest):
    """Proxy async detection request to backend"""
    try:
        response = requests.post(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/detect/async",
            json=request.dict(),
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Async request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.post("/detect/async/upload")
async def submit_async_detection_upload(
    file: UploadFile = File(...),
    text_queries: str = Form(...),
    box_threshold: float = Form(0.4),
    text_threshold: float = Form(0.3),
    return_visualization: bool = Form(True),
    priority: int = Form(5)
):
    """Proxy async upload detection request to backend"""
    try:
        # Prepare form data for backend
        files = {"file": (file.filename, await file.read(), file.content_type)}
        data = {
            "text_queries": text_queries,
            "box_threshold": box_threshold,
            "text_threshold": text_threshold,
            "return_visualization": return_visualization,
            "priority": priority
        }
        
        response = requests.post(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/detect/async/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Async upload request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Proxy task status request to backend"""
    try:
        response = requests.get(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/task/{task_id}",
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Task status request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.delete("/task/{task_id}")
async def cancel_task(task_id: str):
    """Proxy task cancellation request to backend"""
    try:
        response = requests.delete(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/task/{task_id}",
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Task cancellation request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.get("/queue/status")
async def get_queue_status():
    """Proxy queue status request to backend"""
    try:
        response = requests.get(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/queue/status",
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Queue status request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    """Proxy model info request to backend"""
    try:
        response = requests.get(
            f"http://{GROUNDING_DINO_HOST}:{GROUNDING_DINO_PORT}/model/info",
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.RequestException as e:
        logger.error(f"Model info request to backend failed: {e}")
        raise HTTPException(status_code=503, detail=f"Backend service error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
