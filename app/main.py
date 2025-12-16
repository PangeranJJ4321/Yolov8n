import shutil
import os
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import sys

# Add parent directory to path to allow importing src
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

import cv2
import numpy as np

# Import our system
from src.pothole_detection_system import PotholeDetectionSystem
from app.utils_api import format_pothole_payload

# --- Configuration ---
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output" / "api_results"
MODEL_PATH = BASE_DIR / "runs/segment/yolov8m-seg-custom/weights/best.pt"
CALIB_PATH = BASE_DIR / "calibration_results/camera_params.yaml"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Global variables
system: Optional[PotholeDetectionSystem] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events: Load model on startup"""
    global system
    print("🚀 Starting Pothole Detection API...")
    
    if not MODEL_PATH.exists():
        print(f"❌ Model not found at {MODEL_PATH}")
    else:
        print(f"📥 Loading PotholeDetectionSystem...")
        try:
            calib = CALIB_PATH if CALIB_PATH.exists() else None
            system = PotholeDetectionSystem(
                yolo_model_path=MODEL_PATH,
                depth_model_type="small",
                camera_calib_path=calib,
                conf_threshold=0.25,
                enable_tracking=True
            )
            print("✅ System ready!")
        except Exception as e:
            print(f"❌ Failed to load system: {e}")
            import traceback
            traceback.print_exc()
            
    yield
    print("👋 Shutting down API...")

app = FastAPI(
    title="Pothole Detection API",
    description="API for detecting and measuring potholes using YOLOv8 and DepthAnything V2",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount paths
app.mount("/results", StaticFiles(directory=str(OUTPUT_DIR)), name="results")
app.mount("/static", StaticFiles(directory="app/web_ui"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('app/web_ui/index.html')

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "model_loaded": system is not None,
        "version": "1.0.0"
    }

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    """Process a single image and return structured JSON payload"""
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    file_id = uuid.uuid4().hex
    ext = Path(file.filename).suffix
    input_path = UPLOAD_DIR / f"{file_id}{ext}"
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        image = cv2.imread(str(input_path))
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
            
        # Process
        results = system.process_frame(image)
        
        # Visualize
        vis_image = system.visualize_results(
            image, results, 
            show_depth=False,
            show_measurements=True, 
            show_tracks=False
        )
        
        output_filename = f"{file_id}_processed.jpg"
        output_path = OUTPUT_DIR / output_filename
        cv2.imwrite(str(output_path), vis_image)
        
        # Transform measurements to Standard Payload
        measurements_payload = []
        result_url_base = f"/results/{output_filename}" # Ideally absolute URL logic here
        
        for m in results['measurements']:
            # Format using utility function
            payload = format_pothole_payload(
                measurement=m,
                image_url=result_url_base,
                device_id="web_console_01"
            )
            measurements_payload.append(payload)
        
        return {
            "success": True,
            "filename": file.filename,
            "measurements": measurements_payload, # Now follows the strict schema
            "processed_image_url": result_url_base,
            "pothole_count": len(measurements_payload)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect/video")
async def detect_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Process a video (Async)"""
    # ... logic remains similar, ideally tracking would aggregate measurements ...
    # For now, let's keep the simple async implementation
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
        
    file_id = uuid.uuid4().hex
    ext = Path(file.filename).suffix or ".mp4"
    input_path = UPLOAD_DIR / f"{file_id}{ext}"
    output_filename = f"{file_id}_processed.avi"
    output_path = OUTPUT_DIR / output_filename
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    # Define background task
    def process_video_task(in_path, out_path):
        print(f"🎬 Processing video {in_path}...")
        try:
            # Note: process_video saves standard json, we might want to post-process it to new schema later?
            # For this MVP, we rely on the internal json save.
            system.process_video(
                video_path=in_path,
                output_path=out_path,
                show_preview=False,
                save_measurements=True
            )
            print(f"✅ Video processing complete: {out_path}")
        except Exception as e:
            print(f"❌ Video processing failed: {e}")

    background_tasks.add_task(process_video_task, input_path, output_path)

    return {
        "success": True,
        "message": "Video processing started in background",
        "job_id": file_id,
        "result_video_url": f"/results/{output_filename}"
    }

if __name__ == "__main__":
    import uvicorn
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=8000)
