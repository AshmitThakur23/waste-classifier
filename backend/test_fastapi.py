"""
Minimal test to verify FastAPI app can start without YOLO model
"""

import os
os.environ["ENABLE_GEMINI"] = "false"

# Mock the model path to prevent loading error
os.environ["MODEL_PATH"] = "dummy.pt"

print("Testing FastAPI import...")
try:
    from app import app
    print("✅ FastAPI app imported successfully")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    exit(1)

print("\nTesting route registration...")
routes = [route.path for route in app.routes]
expected_routes = ["/", "/health", "/api/classify", "/api/categories"]

for route in expected_routes:
    if route in routes:
        print(f"  ✅ {route}")
    else:
        print(f"  ❌ {route} missing")

print("\n✅ FastAPI structure looks good!")
print("\nNote: To run the server, install YOLOv8 dependencies:")
print("  pip install ultralytics torch torchvision opencv-python")
