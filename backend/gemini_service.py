"""
Gemini API Integration for Waste Classification
Uses Gemini Vision for accurate waste classification + awareness tips
"""

import os
import base64
from io import BytesIO
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

from typing import Optional, Tuple
from PIL import Image
from utils import get_fallback_awareness_tip

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ENABLE_GEMINI = os.getenv("ENABLE_GEMINI", "true").lower() == "true"

# Initialize Gemini
model = None
vision_model = None
if GEMINI_API_KEY and ENABLE_GEMINI and GENAI_AVAILABLE:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use gemini-1.5-flash - higher free tier quota
        model = genai.GenerativeModel('gemini-1.5-flash')
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini API configured successfully (gemini-1.5-flash with Vision)")
    except Exception as e:
        print(f"⚠️ Gemini API configuration failed: {e}")
        model = None
        vision_model = None
else:
    if not GENAI_AVAILABLE:
        print("⚠️ Gemini API library not available")
    else:
        print("⚠️ Gemini API disabled or no API key provided (using YOLO model only)")


def classify_with_gemini_vision(image: Image.Image) -> Tuple[str, str, float]:
    """
    Classify waste using Gemini Vision AI for accurate results
    
    Args:
        image: PIL Image object
    
    Returns:
        Tuple of (category, detected_item, confidence)
    """
    if not vision_model:
        return None, None, 0.0
    
    try:
        # Convert PIL image to bytes
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        image_bytes = buffered.getvalue()
        
        # Create image part for Gemini
        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_bytes).decode()
        }
        
        # Classification prompt
        prompt = """You are a waste classification expert. Analyze this image and classify the waste item.

RESPOND IN THIS EXACT FORMAT (one line only):
CATEGORY|ITEM_NAME|CONFIDENCE

Where:
- CATEGORY must be exactly one of: ORGANIC, RECYCLABLE, HAZARDOUS
- ITEM_NAME is what you see (e.g., "plastic bottle", "banana peel", "battery")
- CONFIDENCE is a number between 0.70 and 0.99

CLASSIFICATION RULES:
- ORGANIC: Food waste, fruit/vegetable peels, garden waste, paper tissues, biodegradable items
- RECYCLABLE: Plastic bottles, glass, metal cans, cardboard, paper, aluminum, PET bottles
- HAZARDOUS: Batteries, electronics, chemicals, medicines, paint, light bulbs, e-waste

Examples:
- Plastic water bottle → RECYCLABLE|plastic bottle|0.95
- Banana peel → ORGANIC|banana peel|0.92
- AA battery → HAZARDOUS|battery|0.94

Analyze the image and respond with ONLY the classification line, nothing else."""

        # Call Gemini Vision
        response = vision_model.generate_content([prompt, image_part])
        
        if response and response.text:
            result = response.text.strip()
            parts = result.split("|")
            
            if len(parts) >= 3:
                category = parts[0].strip().upper()
                item_name = parts[1].strip()
                try:
                    confidence = float(parts[2].strip())
                except:
                    confidence = 0.85
                
                # Validate category
                if category not in ["ORGANIC", "RECYCLABLE", "HAZARDOUS"]:
                    category = "HAZARDOUS"  # Safety default
                
                return category, item_name, min(confidence, 0.99)
        
        return None, None, 0.0
        
    except Exception as e:
        print(f"⚠️ Gemini Vision error: {e}")
        return None, None, 0.0


def generate_awareness_tip(item_name: str, category: str, confidence: float) -> str:
    """
    Generate educational awareness tip using Gemini AI
    
    Args:
        item_name: Detected item name (from YOLO)
        category: Classification (ORGANIC/RECYCLABLE/HAZARDOUS)
        confidence: Model confidence score
    
    Returns:
        str: Awareness tip (Gemini-generated or fallback)
    """
    # Use fallback if Gemini is disabled or not configured
    if not model or not ENABLE_GEMINI:
        return get_fallback_awareness_tip(category)
    
    try:
        # Generate contextual prompt for Gemini
        prompt = f"""You are a friendly waste management expert helping people sort their garbage correctly.

ITEM DETECTED: {item_name}
CATEGORY: {category} waste

Write a SHORT, CLEAR awareness tip (2-3 sentences) that includes:
1. Why this belongs in {category} category
2. The correct disposal method
3. ONE environmental impact fact

Rules:
- Be direct and helpful
- Use simple language anyone can understand
- Include a practical disposal tip
- DO NOT use emojis
- Keep under 200 characters"""

        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.6,
                'max_output_tokens': 150,
            }
        )
        
        # Extract and clean response
        if response and response.text:
            tip = response.text.strip()
            # Ensure it's not too long
            if len(tip) > 250:
                tip = tip[:247] + "..."
            return tip
        else:
            return get_fallback_awareness_tip(category)
    
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        # Always return fallback on error
        return get_fallback_awareness_tip(category)


def generate_safety_warning(confidence: float) -> str:
    """
    Generate safety warning for low-confidence predictions
    
    Args:
        confidence: Model confidence score
    
    Returns:
        str: Safety warning message
    """
    if confidence < 0.5:
        return "⚠️ Low confidence detection. When unsure, treat as HAZARDOUS waste for safety."
    elif confidence < 0.7:
        return "⚠️ Uncertain classification. Please verify or consult local waste guidelines."
    else:
        return ""
