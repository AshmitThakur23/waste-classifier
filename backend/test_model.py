"""
Test YOLOv8 model - Check if best.pt is valid and what classes it has
"""

import os
from ultralytics import YOLO

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'best.pt')

print(f"📁 Model path: {MODEL_PATH}")
print(f"📊 File exists: {os.path.exists(MODEL_PATH)}")

if os.path.exists(MODEL_PATH):
    print(f"📦 File size: {os.path.getsize(MODEL_PATH) / 1024 / 1024:.2f} MB\n")
    
    try:
        print("🔄 Loading model...")
        model = YOLO(MODEL_PATH)
        print("✅ Model loaded successfully!\n")
        
        # Get model info
        print("📋 Model Information:")
        print(f"  Task: {model.task}")
        print(f"  Model type: {type(model).__name__}\n")
        
        # Get class names
        if hasattr(model, 'names'):
            print("🏷️  Model Classes:")
            for idx, name in model.names.items():
                print(f"    {idx}: {name}")
            print(f"\n  Total classes: {len(model.names)}")
        else:
            print("⚠️  No class names found in model")
        
        print("\n✅ Model is ready for use!")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print("❌ Model file not found!")
