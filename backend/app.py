"""
FastAPI Backend for Waste Classification
Classifies waste into: ORGANIC, RECYCLABLE, HAZARDOUS
Uses Gemini Vision AI (primary) + YOLOv8 (fallback) for intelligent waste segregation
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from PIL import Image
import io
import os
from datetime import datetime
from typing import Optional
import logging
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)
print(f"📁 Loaded .env from: {env_path}")

# Import custom modules
from utils import (
    get_dustbin_color, 
    get_dustbin_icon, 
    normalize_class_name,
    validate_image_format
)
from gemini_service import generate_awareness_tip, generate_safety_warning, classify_with_gemini_vision

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Waste Classification API",
    description="Personal waste-segregation assistant powered by YOLOv8 and Gemini AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), 'model', 'best.pt'))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.65"))
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", "10485760"))  # 10MB
FRONTEND_PATH = Path(__file__).parent.parent / "frontend"

# Global model variable
model: Optional[YOLO] = None


@app.on_event("startup")
async def startup_event():
    """Load YOLOv8 model on application startup"""
    global model
    try:
        logger.info(f"Loading model from: {MODEL_PATH}")
        model = YOLO(MODEL_PATH)
        logger.info("✅ Model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        raise RuntimeError(f"Model loading failed: {str(e)}")


@app.get("/")
async def root():
    """Serve frontend HTML"""
    index_path = FRONTEND_PATH / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    else:
        return {
            "message": "Waste Classification API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "classify": "/api/classify",
                "categories": "/api/categories"
            }
        }


# Mount static files for frontend
if FRONTEND_PATH.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PATH)), name="static")


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/classify")
async def classify_waste(file: UploadFile = File(...)):
    """
    Main classification endpoint
    
    Accepts image file and returns:
    - Waste category (ORGANIC/RECYCLABLE/HAZARDOUS)
    - Dustbin color and icon
    - AI-generated awareness tip
    - Confidence score
    """
    # Validate model is loaded
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size: {MAX_IMAGE_SIZE/1024/1024}MB"
        )
    
    # Validate file type - check both filename and content-type
    valid_content_types = {
        'image/jpeg', 'image/png', 'image/jpg', 'image/bmp', 
        'image/webp', 'image/gif', 'image/tiff'
    }
    is_valid_by_name = validate_image_format(file.filename)
    is_valid_by_type = file.content_type and file.content_type.lower() in valid_content_types
    
    if not is_valid_by_name and not is_valid_by_type:
        logger.warning(f"Invalid file: name={file.filename}, type={file.content_type}")
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Supported: JPG, PNG, JPEG, BMP, WEBP, GIF, TIFF"
        )
    
    try:
        # Process image
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed (handle RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # ===== PRIMARY: Try Gemini Vision for accurate classification =====
        logger.info("🔍 Attempting Gemini Vision classification...")
        gemini_category, gemini_item, gemini_confidence = classify_with_gemini_vision(image)
        
        if gemini_category and gemini_confidence > 0:
            # Gemini Vision succeeded - use its result
            logger.info(f"✅ Gemini Vision: {gemini_category} ({gemini_item}) - {gemini_confidence:.2%}")
            
            category = gemini_category
            detected_item = gemini_item
            confidence = gemini_confidence
            is_safe_classification = True
            
            # Get dustbin info
            dustbin_color = get_dustbin_color(category)
            dustbin_icon = get_dustbin_icon(category)
            
            # Generate awareness tip
            awareness_tip = generate_awareness_tip(detected_item, category, confidence)
            safety_warning = ""
            
            return {
                "success": True,
                "category": category,
                "confidence": round(confidence, 4),
                "dustbin_color": dustbin_color,
                "dustbin_icon": dustbin_icon,
                "explanation": awareness_tip,
                "safety_warning": safety_warning,
                "is_safe_classification": is_safe_classification,
                "detected_item": detected_item,
                "timestamp": datetime.utcnow().isoformat(),
                "model_used": "Gemini Vision AI"
            }
        
        # ===== FALLBACK: Use YOLO model if Gemini fails =====
        logger.info("⚠️ Gemini unavailable, falling back to YOLO model...")
        results = model(image, verbose=False)
        
        # Process results
        if len(results) > 0 and len(results[0].boxes) > 0:
            # Extract predictions
            boxes = results[0].boxes
            confidences = boxes.conf.cpu().numpy()
            classes = boxes.cls.cpu().numpy()
            
            # Get highest confidence prediction
            max_conf_idx = confidences.argmax()
            predicted_class_id = int(classes[max_conf_idx])
            confidence = float(confidences[max_conf_idx])
            
            # Get class name from model
            class_names = results[0].names
            yolo_class_name = class_names[predicted_class_id]
            
            # Normalize to standard categories
            category = normalize_class_name(yolo_class_name)
            
            # Apply safety threshold
            is_safe_classification = confidence >= CONFIDENCE_THRESHOLD
            if not is_safe_classification:
                category = "HAZARDOUS"  # Default to hazardous for safety
                logger.warning(f"Low confidence ({confidence:.2f}), classifying as HAZARDOUS")
            
            # Get dustbin info
            dustbin_color = get_dustbin_color(category)
            dustbin_icon = get_dustbin_icon(category)
            
            # Generate awareness tip using Gemini
            logger.info("Generating awareness tip...")
            awareness_tip = generate_awareness_tip(yolo_class_name, category, confidence)
            
            # Generate safety warning if needed
            safety_warning = generate_safety_warning(confidence)
            
            # Build response
            response = {
                "success": True,
                "category": category,
                "confidence": round(confidence, 4),
                "dustbin_color": dustbin_color,
                "dustbin_icon": dustbin_icon,
                "explanation": awareness_tip,
                "safety_warning": safety_warning,
                "is_safe_classification": is_safe_classification,
                "detected_item": yolo_class_name,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"✅ Classification successful: {category} (confidence: {confidence:.2f})")
            return response
        
        else:
            # No waste detected
            logger.warning("No waste detected in image")
            return {
                "success": False,
                "category": "HAZARDOUS",  # Safety default
                "confidence": 0.0,
                "dustbin_color": "red",
                "dustbin_icon": "warning",
                "explanation": "No recognizable waste item detected. For safety, treat unknown items as hazardous waste.",
                "safety_warning": "⚠️ Unable to identify item - dispose as HAZARDOUS for safety",
                "is_safe_classification": False,
                "detected_item": None,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    except Exception as e:
        logger.error(f"❌ Classification error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.get("/api/categories")
async def get_categories():
    """Get available waste categories and their properties"""
    return {
        "categories": [
            {
                "name": "ORGANIC",
                "dustbin_color": "green",
                "icon": "leaf",
                "description": "Organic waste that decomposes naturally. Examples: food scraps, garden waste."
            },
            {
                "name": "RECYCLABLE",
                "dustbin_color": "blue",
                "icon": "recycle",
                "description": "Materials that can be reprocessed. Examples: plastic, paper, glass, metal."
            },
            {
                "name": "HAZARDOUS",
                "dustbin_color": "red",
                "icon": "warning",
                "description": "Waste that poses risks to health or environment. Examples: batteries, chemicals, e-waste."
            }
        ],
        "confidence_threshold": CONFIDENCE_THRESHOLD
    }


# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
