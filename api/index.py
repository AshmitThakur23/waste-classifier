"""
Vercel Serverless Function Handler
Waste Classification API powered by Gemini Vision AI
"""
import os
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app for Vercel
app = FastAPI(
    title="Waste Classification API",
    description="Waste segregation assistant powered by Gemini Vision AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Waste categories mapping
WASTE_CATEGORIES = {
    "ORGANIC": {
        "dustbin_color": "green",
        "icon": "leaf",
        "description": "Biodegradable waste like food scraps, garden waste"
    },
    "RECYCLABLE": {
        "dustbin_color": "blue", 
        "icon": "recycle",
        "description": "Materials that can be recycled: plastic, paper, glass, metal"
    },
    "HAZARDOUS": {
        "dustbin_color": "red",
        "icon": "warning",
        "description": "Dangerous waste: batteries, chemicals, electronics"
    },
    "GENERAL": {
        "dustbin_color": "grey",
        "icon": "trash",
        "description": "Non-recyclable, non-hazardous waste"
    }
}

# Try to import Gemini service
try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        GEMINI_AVAILABLE = True
        logger.info("✅ Gemini Vision AI initialized")
    else:
        GEMINI_AVAILABLE = False
        logger.warning("⚠️ GEMINI_API_KEY not set")
except Exception as e:
    GEMINI_AVAILABLE = False
    logger.error(f"❌ Gemini init failed: {e}")


async def classify_with_gemini(image_bytes: bytes) -> dict:
    """Classify waste using Gemini Vision AI"""
    if not GEMINI_AVAILABLE:
        raise Exception("Gemini not available")
    
    prompt = """Analyze this image and classify the waste item into ONE of these categories:
    - ORGANIC (food waste, garden waste, biodegradable items)
    - RECYCLABLE (plastic bottles, glass, metal cans, cardboard, paper)
    - HAZARDOUS (batteries, chemicals, electronics, medical waste, bulbs)
    - GENERAL (chip packets, tissues, styrofoam, mixed waste)
    
    Respond in this exact format:
    CATEGORY: [category name]
    ITEM: [detected item]
    CONFIDENCE: [0.0-1.0]
    TIP: [disposal tip in 1-2 sentences]
    """
    
    image = Image.open(io.BytesIO(image_bytes))
    response = gemini_model.generate_content([prompt, image])
    
    # Parse response
    text = response.text.upper()
    category = "GENERAL"  # default
    
    for cat in ["HAZARDOUS", "ORGANIC", "RECYCLABLE", "GENERAL"]:
        if cat in text:
            category = cat
            break
    
    return {
        "category": category,
        "raw_response": response.text,
        "model": "Gemini Vision AI"
    }


@app.get("/")
async def root():
    """API info"""
    return {
        "message": "Waste Classification API",
        "version": "1.0.0",
        "platform": "Vercel",
        "endpoints": {
            "health": "/health",
            "classify": "/api/classify",
            "categories": "/api/categories"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gemini_available": GEMINI_AVAILABLE,
        "timestamp": datetime.utcnow().isoformat(),
        "platform": "Vercel"
    }


@app.get("/api/categories")
async def get_categories():
    """Get all waste categories"""
    return {"categories": WASTE_CATEGORIES}


@app.post("/api/classify")
async def classify_waste(file: UploadFile = File(...)):
    """
    Classify waste using Gemini Vision AI
    """
    # Validate file type
    valid_types = {'image/jpeg', 'image/png', 'image/jpg', 'image/webp'}
    if file.content_type and file.content_type.lower() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Supported: JPG, PNG, JPEG, WEBP"
        )
    
    contents = await file.read()
    
    # Check file size (5MB limit for Vercel)
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Max 5MB")
    
    try:
        # Classify with Gemini
        result = await classify_with_gemini(contents)
        category = result["category"]
        
        cat_info = WASTE_CATEGORIES.get(category, WASTE_CATEGORIES["GENERAL"])
        
        return {
            "success": True,
            "category": category,
            "confidence": 0.85,
            "dustbin_color": cat_info["dustbin_color"],
            "dustbin_icon": cat_info["icon"],
            "description": cat_info["description"],
            "model_used": "Gemini Vision AI",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Classification error: {e}")
        # Fallback response
        return {
            "success": False,
            "category": "GENERAL",
            "confidence": 0.5,
            "dustbin_color": "grey",
            "dustbin_icon": "trash",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


# Vercel handler
handler = app
