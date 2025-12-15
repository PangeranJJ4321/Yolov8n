import shutil
import os
import uuid
from pathlib import Path
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import cv2
import numpy as np

# Import our system
# Pastikan src ada di path atau script ini dijalankan sebagai modul
try:
    from src.pothole_detection_system import PotholeDetectionSystem
except ImportError:
    # Fallback jika dijalankan langsung dari src/
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from src.pothole_detection_system import PotholeDetectionSystem

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
        # Could raise error, but we'll let it run without system (will error on request)
    else:
        print(f"📥 Loading PotholeDetectionSystem...")
        try:
            # Check calibration
            calib = CALIB_PATH if CALIB_PATH.exists() else None
            
            system = PotholeDetectionSystem(
                yolo_model_path=MODEL_PATH,
                depth_model_type="small", # vits
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse

# Mount Output directory
app.mount("/results", StaticFiles(directory=str(OUTPUT_DIR)), name="results")
app.mount("/static", StaticFiles(directory="web_ui"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('web_ui/index.html')

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "model_loaded": system is not None
    }

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    """Process a single image"""
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    # Save upload
    file_id = uuid.uuid4().hex
    ext = Path(file.filename).suffix
    input_path = UPLOAD_DIR / f"{file_id}{ext}"
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Read image
        image = cv2.imread(str(input_path))
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
            
        # Process
        results = system.process_frame(image)
        
        # Visualize
        vis_image = system.visualize_results(
            image, results, 
            show_depth=False, # Overlay depth might be too cluttered for API result image? Let's keep clean or use what user liked.
            show_measurements=True, 
            show_tracks=False # Single image usually no tracks (unless we fake it)
        )
        
        # Save output
        output_filename = f"{file_id}_processed.jpg"
        output_path = OUTPUT_DIR / output_filename
        cv2.imwrite(str(output_path), vis_image)
        
        # Convert measurements to JSON-serializable format
        measurements_data = [m.to_dict() for m in results['measurements']]
        
        return {
            "success": True,
            "filename": file.filename,
            "measurements": measurements_data,
            "processed_image_url": f"/results/{output_filename}",
            "pothole_count": len(measurements_data)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup input?
        # input_path.unlink(missing_ok=True)
        pass

@app.post("/detect/video")
async def detect_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Process a video (Async)"""
    if system is None:
        raise HTTPException(status_code=503, detail="System not initialized")
        
    file_id = uuid.uuid4().hex
    ext = Path(file.filename).suffix
    input_path = UPLOAD_DIR / f"{file_id}{ext}"
    output_filename = f"{file_id}_processed.avi" # or mp4 if we fix codec
    output_path = OUTPUT_DIR / output_filename
    json_filename = f"{file_id}_measurements.json"
    json_path = OUTPUT_DIR / json_filename
    
    # Save input
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    # Define background task
    def process_video_task(in_path, out_path, j_path):
        print(f"🎬 Processing video {in_path}...")
        try:
            # Use process_video method
            system.process_video(
                video_path=in_path,
                output_path=out_path,
                show_preview=False,
                save_measurements=True
            )
            # The system saves measurements to a json path derived from output_path or custom?
            # system.process_video returns a Dict.
            # But wait, system.process_video logic for saving json:
            # It saves to f"{output_path.parent}/{output_path.stem}_measurements.json" usually.
            # Let's verify process_video implementation.
            
            # Rename the auto-generated json to our target json_path if needed
            # Or just let it be.
            print(f"✅ Video processing complete: {out_path}")
        except Exception as e:
            print(f"❌ Video processing failed: {e}")

    background_tasks.add_task(process_video_task, input_path, output_path, json_path)

    return {
        "success": True,
        "message": "Video processing started in background",
        "job_id": file_id,
        "result_video_url": f"/results/{output_filename}",
        "result_json_url": f"/results/{Path(output_filename).stem}_measurements.json" # Default naming convention
    }

if __name__ == "__main__":
    import uvicorn
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=8000)
