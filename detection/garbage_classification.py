"""
Garbage Classification Detection Module
Uses the waste classification model for additional detection.
"""

import cv2
from ultralytics import YOLO
import os

# Use the waste classifier model
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(_PROJECT_ROOT, "models", "waste_classify.pt")

_model = None
_model_loaded = False


def _load_model():
    """Load garbage classification model once."""
    global _model, _model_loaded
    if not _model_loaded:
        if os.path.exists(MODEL_PATH):
            _model = YOLO(MODEL_PATH)
            print(f"✅ Garbage classification model loaded: {MODEL_PATH}")
        else:
            print(f"⚠️ Garbage classification model not found: {MODEL_PATH}")
            _model = None
        _model_loaded = True
    return _model


def classify_garbage(frame, box, confidence_threshold=0.25):
    """
    Classify a detected garbage object using the classification model.
    """
    model = _load_model()
    if model is None:
        return None
    
    x1, y1, x2, y2 = box
    
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return None
    
    results = model(roi, verbose=False, conf=confidence_threshold)
    
    for result in results:
        if result.boxes is not None and len(result.boxes) > 0:
            box = result.boxes[0]
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls_id]
            return f"{class_name} ({conf:.0%})"
    
    return None


def detect_with_classification(frame, hand_boxes, person_boxes, confidence_threshold=0.20):
    """
    Detect garbage objects using classification model.
    """
    model = _load_model()
    if model is None:
        return []
    
    detections = []
    results = model(frame, verbose=False, conf=confidence_threshold)
    
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                
                obj_box = (x1, y1, x2, y2)
                
                if _is_in_hands(obj_box, hand_boxes):
                    detections.append({
                        'box': obj_box,
                        'class_name': class_name,
                        'confidence': conf
                    })
    
    return detections


def _is_in_hands(obj_box, hand_boxes):
    """Check if object is in hands."""
    if not hand_boxes:
        return False
    
    ox1, oy1, ox2, oy2 = obj_box
    obj_cx = (ox1 + ox2) // 2
    obj_cy = (oy1 + oy2) // 2
    
    for hx1, hy1, hx2, hy2 in hand_boxes:
        expand = 80
        if (hx1 - expand) <= obj_cx <= (hx2 + expand) and (hy1 - expand) <= obj_cy <= (hy2 + expand):
            return True
    
    return False
