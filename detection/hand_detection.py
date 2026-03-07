"""
Hand Detection Module
=====================
Uses trained hand detection model to identify hands in frame.
This helps focus garbage detection on objects in hands only.
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os

# Path to trained hand model - relative to project root
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND_MODEL_PATH = os.path.join(_PROJECT_ROOT, "models", "hand_best.pt")

_hand_model = None
_model_loaded = False


def _load_model():
    """Load hand detection model once."""
    global _hand_model, _model_loaded
    if not _model_loaded:
        if os.path.exists(HAND_MODEL_PATH):
            _hand_model = YOLO(HAND_MODEL_PATH)
            print(f"✅ Hand detection model loaded: {HAND_MODEL_PATH}")
        else:
            print(f"⚠️ Hand model not found at: {HAND_MODEL_PATH}")
            print("   Using person body detection as fallback")
            _hand_model = None
        _model_loaded = True
    return _hand_model


class HandStabilityTracker:
    """
    Stability tracker for hand detections.
    Prevents flickering by requiring consistent detections.
    """
    def __init__(self):
        self.tracked = {}  # id -> {box, count, last_seen}
        self.next_id = 0
        self.frame_num = 0
        self.min_frames = 3  # Must see 3 frames to be stable
        self.max_missing = 5  # Remove after 5 missing frames
    
    def update(self, raw_boxes):
        """Update with raw detections, return only stable ones."""
        self.frame_num += 1
        stable = []
        used_ids = set()
        
        for box in raw_boxes:
            x1, y1, x2, y2, conf = box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            # Find matching track
            match_id = None
            min_dist = 80  # Max distance to match
            
            for tid, data in self.tracked.items():
                if tid in used_ids:
                    continue
                tx1, ty1, tx2, ty2, _ = data['box']
                tcx, tcy = (tx1 + tx2) // 2, (ty1 + ty2) // 2
                dist = ((cx - tcx)**2 + (cy - tcy)**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    match_id = tid
            
            if match_id is not None:
                # Update existing
                self.tracked[match_id]['box'] = box
                self.tracked[match_id]['count'] += 1
                self.tracked[match_id]['last_seen'] = self.frame_num
                used_ids.add(match_id)
                
                if self.tracked[match_id]['count'] >= self.min_frames:
                    stable.append(box)
            else:
                # New track
                self.tracked[self.next_id] = {
                    'box': box,
                    'count': 1,
                    'last_seen': self.frame_num
                }
                self.next_id += 1
        
        # Remove old tracks
        to_del = [tid for tid, d in self.tracked.items() 
                  if self.frame_num - d['last_seen'] > self.max_missing]
        for tid in to_del:
            del self.tracked[tid]
        
        return stable
    
    def reset(self):
        """Reset tracking."""
        self.tracked = {}
        self.next_id = 0


_tracker = HandStabilityTracker()


def detect_hands(frame, confidence_threshold=0.35, person_boxes=None):
    """
    Detect hands in frame.
    
    Args:
        frame: Input frame
        confidence_threshold: Minimum confidence for hand detection
        person_boxes: Optional person boxes to filter hands
    
    Returns:
        hand_boxes: List of (x1, y1, x2, y2) tuples
    """
    model = _load_model()
    
    # If no model, estimate hands from person boxes
    if model is None:
        if person_boxes:
            return _estimate_hand_regions_from_person(person_boxes)
        return []
    
    # Detect hands using trained model
    results = model(frame, verbose=False, conf=confidence_threshold)
    
    raw_boxes = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                raw_boxes.append((x1, y1, x2, y2, conf))
    
    # Apply stability tracking
    stable_boxes = _tracker.update(raw_boxes)
    
    # Convert to simple tuples
    hand_boxes = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2, _ in stable_boxes]
    
    # Filter by person boxes if provided
    if person_boxes:
        hand_boxes = _filter_hands_near_person(hand_boxes, person_boxes)
    
    return hand_boxes


def _estimate_hand_regions_from_person(person_boxes):
    """
    Fallback: Estimate hand regions from person boxes.
    Returns likely hand locations (sides and bottom of person box).
    """
    hand_regions = []
    
    for px1, py1, px2, py2 in person_boxes:
        pw = px2 - px1
        ph = py2 - py1
        
        # Expand person box slightly for hands
        expand_x = int(pw * 0.20)
        expand_y = int(ph * 0.05)
        
        hx1 = px1 - expand_x
        hx2 = px2 + expand_x
        hy1 = py1 + int(ph * 0.10)  # Below head
        hy2 = py2 + expand_y
        
        hand_regions.append((hx1, hy1, hx2, hy2))
    
    return hand_regions


def _filter_hands_near_person(hand_boxes, person_boxes, max_distance=100):
    """
    Filter hands that are near person boxes.
    """
    filtered = []
    
    for hx1, hy1, hx2, hy2 in hand_boxes:
        hcx = (hx1 + hx2) // 2
        hcy = (hy1 + hy2) // 2
        
        for px1, py1, px2, py2 in person_boxes:
            # Check if hand center is within or near person box
            if (px1 - max_distance <= hcx <= px2 + max_distance and
                py1 - max_distance <= hcy <= py2 + max_distance):
                filtered.append((hx1, hy1, hx2, hy2))
                break
    
    return filtered


def draw_hands(frame, hand_boxes):
    """
    Draw hand detection boxes on frame.
    """
    for x1, y1, x2, y2 in hand_boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(frame, "Hand", (x1, y1 - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    return frame


def is_model_available():
    """Check if hand model exists."""
    return os.path.exists(HAND_MODEL_PATH)


def reset_tracker():
    """Reset hand tracking."""
    global _tracker
    _tracker.reset()
