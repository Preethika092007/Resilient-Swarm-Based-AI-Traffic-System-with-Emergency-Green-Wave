import cv2
import os
from ultralytics import YOLO

# Load trained emergency vehicle detection model
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# helper to locate a `best.pt` file produced by training
def locate_best_weights():
    # 1. check canonical location under project tree
    candidate = os.path.join(project_root, 'runs', 'detect', 'emergency_vehicle_train', 'weights', 'best.pt')
    if os.path.exists(candidate):
        return candidate
    # 2. sometimes training is executed from home or another cwd – search user dirs
    home = os.path.expanduser('~')
    home_runs = os.path.join(home, 'runs')
    if os.path.isdir(home_runs):
        for root, dirs, files in os.walk(home_runs):
            if 'best.pt' in files and 'emergency_vehicle_train' in root:
                return os.path.join(root, 'best.pt')
    # 3. final fallback: not found
    return None

model_path = locate_best_weights()
if model_path is None:
    print("⚠️  Could not locate emergency vehicle weights file (best.pt).")
    print(f"Expected under {os.path.join(project_root, 'runs', 'detect')} or in ~/runs.")
    print("Please re-run the training script or copy the file to the project.")
    print("Using pretrained yolov8n network for now (detections will be generic).\n")
    model = YOLO('yolov8n.pt')
else:
    print(f"Loading model weights from {model_path}")
    model = YOLO(model_path)

# Emergency vehicle classes (only 2 classes - fire trucks are mislabeled in dataset)
EMERGENCY_CLASSES = {
    0: 'ambulance',
    1: 'police'
}

# Emergency messages
EMERGENCY_MESSAGES = {
    'ambulance': '🚑 Ambulance detected – Emergency Mode Activated',
    'police': '🚓 Police vehicle detected'
}

# Start webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam")
    exit()

print("Starting emergency vehicle detection... Press 'q' to quit")

# Track detected vehicles to avoid repeated messages
detected_vehicles = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame from webcam")
        break
    
    # Run YOLO detection with very high confidence threshold
    results = model(frame, conf=0.85, iou=0.6, verbose=False)
    
    current_detections = set()
    
    # Process detections
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            
            # Only process if class ID is valid emergency vehicle (0, 1, or 2)
            if cls_id not in EMERGENCY_CLASSES:
                continue
            
            # Skip low confidence detections
            if confidence < 0.90:
                continue
            
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Get vehicle class name
            vehicle_type = EMERGENCY_CLASSES.get(cls_id)
            current_detections.add(vehicle_type)
            
            # Draw bounding box (red for emergency vehicles)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            
            # Draw label with background
            label = f"{vehicle_type} {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (0, 0, 255), -1)
            cv2.putText(frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Print emergency message (only once per detection)
            if vehicle_type not in detected_vehicles:
                print(EMERGENCY_MESSAGES.get(vehicle_type, f"Emergency vehicle detected: {vehicle_type}"))
    
    # Update detected vehicles
    detected_vehicles = current_detections
    
    # Display emergency status on frame
    if current_detections:
        status_text = "⚠️ EMERGENCY VEHICLE DETECTED ⚠️"
        cv2.putText(frame, status_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    # Show frame
    cv2.imshow('Emergency Vehicle Detection', frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
try:
    cv2.destroyAllWindows()
except:
    pass
