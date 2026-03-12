import cv2
from ultralytics import YOLO

# Use pretrained YOLOv8 model (no training needed)
model = YOLO('yolov8n.pt')

# COCO dataset vehicle classes that look like emergency vehicles
VEHICLE_CLASSES = {
    2: 'car',  # Can be emergency vehicle
    5: 'bus',  # Can be emergency vehicle
    7: 'truck'  # Can be emergency vehicle
}

print("Starting emergency vehicle detection (demo mode)... Press 'q' to quit")
print("Note: Using pretrained model - detects all vehicles")

# Start webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame from webcam")
        break
    
    # Run YOLO detection
    results = model(frame, conf=0.5, verbose=False)
    
    vehicle_count = 0
    
    # Process detections
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            
            # Check if detected object is a vehicle
            if cls_id in VEHICLE_CLASSES:
                vehicle_count += 1
                confidence = float(box.conf[0])
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Draw bounding box (red for emergency demo)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                
                # Draw label
                label = f"Emergency Vehicle {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Display emergency status
    if vehicle_count > 0:
        status_text = "⚠️ EMERGENCY VEHICLE DETECTED ⚠️"
        cv2.putText(frame, status_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Show frame
    cv2.imshow('Emergency Vehicle Detection (Demo)', frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
try:
    cv2.destroyAllWindows()
except:
    pass
