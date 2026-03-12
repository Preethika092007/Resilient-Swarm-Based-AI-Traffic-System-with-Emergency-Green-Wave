import cv2
import json
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Vehicle classes to detect (COCO dataset class IDs)
VEHICLE_CLASSES = {
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}

def calculate_density(count):
    """Calculate traffic density based on vehicle count"""
    if count <= 5:
        return "Low"
    elif count <= 15:
        return "Medium"
    else:
        return "High"

def save_traffic_data(vehicle_count, density):
    """Save detection results to JSON file for other modules"""
    data = {
        "vehicle_count": vehicle_count,
        "density": density
    }
    with open('traffic_data.json', 'w') as f:
        json.dump(data, f, indent=2)

# Start webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam")
    exit()

print("Starting vehicle detection... Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame from webcam")
        break
    
    # Run YOLO detection
    results = model(frame, verbose=False)
    
    vehicle_count = 0
    
    # Process detections
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            
            # Check if detected object is a vehicle
            if cls_id in VEHICLE_CLASSES:
                vehicle_count += 1
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{VEHICLE_CLASSES[cls_id]} {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Calculate density
    density = calculate_density(vehicle_count)
    
    # Save data for other modules
    save_traffic_data(vehicle_count, density)
    
    # Display vehicle count and density on frame
    cv2.putText(frame, f"Vehicles Detected: {vehicle_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Lane Density: {density}", (10, 70),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Show frame
    cv2.imshow('Vehicle Detection', frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
try:
    cv2.destroyAllWindows()
except:
    pass
