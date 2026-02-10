"""
Test complete backend import including FastAPI and YOLO
"""

import os
os.environ["ENABLE_GEMINI"] = "false"  # Disable Gemini for basic test
os.environ["CONFIDENCE_THRESHOLD"] = "0.65"

print("Testing Complete Backend Import...\n")
print("=" * 60)

try:
    print("1. Testing utils...")
    from utils import get_dustbin_color, normalize_class_name
    print("   ✅ utils imported")
    
    print("\n2. Testing gemini_service...")
    from gemini_service import generate_awareness_tip
    print("   ✅ gemini_service imported")
    
    print("\n3. Testing FastAPI app...")
    from app import app, model
    print("   ✅ FastAPI app imported")
    print(f"   ✅ Model loaded: {model is not None}")
    
    if model:
        print(f"   ✅ Model type: {type(model).__name__}")
        print(f"   ✅ Model classes: {list(model.names.values())}")
    
    print("\n" + "=" * 60)
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("=" * 60)
    
    # Test class normalization with actual model classes
    print("\n📋 Testing Class Normalization:")
    for class_name in ["BIODEGRADABLE", "RECYCLABLE", "HAZARDOUS"]:
        normalized = normalize_class_name(class_name)
        color = get_dustbin_color(normalized)
        print(f"   {class_name} → {normalized} → {color} dustbin")
    
    print("\n🎉 Backend is ready to run!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
