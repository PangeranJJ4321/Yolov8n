import datetime
import uuid
import random
from typing import Dict, Any, List

def classify_severity(depth_cm: float, diameter_cm: float) -> Dict[str, Any]:
    """
    Classify pothole severity based on dissertation rules.
    
    Rules:
    - Depth: Light (<2.5), Medium (2.5-7.5), Heavy (>=7.5)
    - Diameter: Small (<30), Medium (30-60), Large (>=60)
    - Combined: 
        - Heavy if Depth=Heavy OR Diameter=Large
        - Medium if (Depth=Medium OR Diameter=Medium) AND not Heavy
        - Light otherwise
    """
    # Depth Category
    if depth_cm < 2.5:
        depth_cat = "ringan"
        depth_score = 1
    elif depth_cm < 7.5:
        depth_cat = "sedang"
        depth_score = 2
    else:
        depth_cat = "berat"
        depth_score = 3
        
    # Diameter Category
    if diameter_cm < 30:
        diam_cat = "kecil"
        diam_score = 1
    elif diameter_cm < 60:
        diam_cat = "sedang"
        diam_score = 2
    else:
        diam_cat = "besar"
        diam_score = 3
        
    # Combined Severity
    if depth_cat == "berat" or diam_cat == "besar":
        final_severity = "berat"
        priority_score = 8.0 + (depth_cm / 10.0) # Example scoring
    elif depth_cat == "sedang" or diam_cat == "sedang":
        final_severity = "sedang"
        priority_score = 5.0 + (depth_cm / 10.0)
    else:
        final_severity = "ringan"
        priority_score = 2.0 + (depth_cm / 10.0)
        
    return {
        "depth_category": depth_cat,
        "diameter_category": diam_cat,
        "severity": final_severity,
        "priority_score": min(10.0, round(priority_score, 2))
    }

def format_pothole_payload(
    measurement: Any, 
    image_url: str,
    device_id: str = "dashcam_unit_001",
    geo_lat: float = -5.14769, # Dummy default (Makassar)
    geo_lon: float = 119.43232
) -> Dict[str, Any]:
    """
    Format a single measurement into the standard JSON payload.
    """
    
    # Generate unique ID
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    pid = f"pothole_{timestamp.strftime('%Y%m%d')}_{uuid.uuid4().hex[:5]}"
    
    # Severity
    severity_info = classify_severity(measurement.depth_cm, measurement.diameter_cm)
    
    return {
        "id": pid,
        "latitude": geo_lat + (random.random() - 0.5) * 0.001, # Add slight jitter for demo
        "longitude": geo_lon + (random.random() - 0.5) * 0.001,
        "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "confidence": float(round(measurement.confidence, 2)),
        "size": {
            "diameter_cm": float(round(measurement.diameter_cm, 1)),
            "depth_cm": float(round(measurement.depth_cm, 1)),
            "measurement_method": "depth_estimation_v2",
            "measurement_confidence": float(round(measurement.confidence, 2)), # Placeholder
            "frames_tracked": 1 # For single image
        },
        "severity": severity_info["severity"],
        "severity_classification": {
            "depth_category": severity_info["depth_category"],
            "diameter_category": severity_info["diameter_category"],
            "priority_score": severity_info["priority_score"]
        },
        "measurement_metadata": {
            "scale_recovery_method": "height_based",
            "scale_factor": 1.0, # Placeholder if not exposed
            "camera_height_m": 1.5,
            "segmentation_used": True
        },
        "image_url": image_url,
        "device_id": device_id
    }
