import cv2
from ultralytics import YOLO
import os

# Use relative path from project root
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODEL_PATH = os.path.join(_PROJECT_ROOT, "models", "person_yolov8n.pt")

model = YOLO(_MODEL_PATH)


def detect_person(frame):
    """
    Detect persons in a video frame using YOLO.
    
    Args:
        frame: One video frame (image)
    
    Returns:
        frame: Frame with bounding boxes drawn
        person_found: True if at least one person detected
    """
    
    # Run YOLO detection
    results = model(frame, verbose=False)
    
    person_found = False
    
    for result in results:
        boxes = result.boxes
        
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # YOLO class 0 = "person"
            if class_name == "person":
                person_found = True
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                
                # Draw green bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"Person: {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return frame, person_found
