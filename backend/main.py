"""
Urban Swarm - AI Traffic Management System
Main Integration Pipeline

This module integrates all backend components:
- Vehicle Detection
- Traffic Analytics
- Signal Optimization
- Emergency Vehicle Detection
- Green Wave Activation
"""

import cv2
import json
import os
import sys
import random
from pathlib import Path

# Add backend modules to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from ultralytics import YOLO

# import green_wave routing components
from green_wave.smart_city.city import City
from green_wave.smart_city.routing_engine import EmergencyRouter

# ============================================================================
# MODULE 1: Vehicle Detection
# ============================================================================

class VehicleDetector:
    """Detects regular vehicles using YOLO"""
    
    def __init__(self):
        model_path = backend_path / 'detection' / 'yolov8n.pt'
        self.model = YOLO(str(model_path))
        self.vehicle_classes = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
    
    def detect(self, frame):
        """Detect vehicles in frame and return detections"""
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                if cls_id in self.vehicle_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    x_center = (x1 + x2) // 2
                    y_center = (y1 + y2) // 2
                    confidence = float(box.conf[0])
                    
                    detections.append({
                        'type': self.vehicle_classes[cls_id],
                        'x_center': x_center,
                        'y_center': y_center,
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence
                    })
        
        return detections

# ============================================================================
# MODULE 2: Emergency Vehicle Detection
# ============================================================================

class EmergencyDetector:
    """Detects emergency vehicles (ambulance, police)"""
    
    def __init__(self):
        self.model = self._load_emergency_model()
        self.emergency_classes = {0: 'ambulance', 1: 'police'}
    
    def _load_emergency_model(self):
        """Load trained emergency vehicle model"""
        # Search for trained model
        home = Path.home()
        search_paths = [
            home / 'runs' / 'detect',
            backend_path.parent / 'runs' / 'detect'
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                for model_dir in search_path.glob('emergency_vehicle_train*'):
                    best_pt = model_dir / 'weights' / 'best.pt'
                    if best_pt.exists():
                        print(f"✓ Loaded emergency model: {best_pt}")
                        return YOLO(str(best_pt))
        
        # Fallback to pretrained
        print("⚠ Using pretrained model for emergency detection")
        return YOLO('yolov8n.pt')
    
    def detect(self, frame):
        """Detect emergency vehicles in frame"""
        results = self.model(frame, conf=0.85, iou=0.6, verbose=False)
        emergency_detected = False
        emergency_type = None
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                if cls_id in self.emergency_classes and confidence >= 0.90:
                    emergency_detected = True
                    emergency_type = self.emergency_classes[cls_id]
                    
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append({
                        'type': emergency_type,
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence
                    })
        
        return emergency_detected, emergency_type, detections

# ============================================================================
# MODULE 3: Traffic Analytics
# ============================================================================

class TrafficAnalyzer:
    """Analyzes traffic density and lane distribution"""
    
    def __init__(self, num_lanes=4):
        self.num_lanes = num_lanes
        self.lane_names = [f"Lane {chr(65+i)}" for i in range(num_lanes)]
        self.lane_waiting_times = {lane: 0 for lane in self.lane_names}
    
    def map_to_lane(self, x_coord, frame_width):
        """Map x coordinate to lane"""
        lane_width = frame_width / self.num_lanes
        lane_idx = min(int(x_coord / lane_width), self.num_lanes - 1)
        return self.lane_names[lane_idx]
    
    def analyze(self, detections, frame_width):
        """Analyze traffic and return lane distribution"""
        # Count vehicles per lane
        lane_counts = {lane: 0 for lane in self.lane_names}
        
        for det in detections:
            lane = self.map_to_lane(det['x_center'], frame_width)
            lane_counts[lane] += 1
        
        # Calculate density
        total_vehicles = sum(lane_counts.values())
        if total_vehicles <= 5:
            density = "Low"
        elif total_vehicles <= 15:
            density = "Medium"
        else:
            density = "High"
        
        # Update waiting times
        for lane in self.lane_waiting_times:
            self.lane_waiting_times[lane] += 1
        
        # Calculate priority scores
        lane_analysis = {}
        for lane, count in lane_counts.items():
            priority_score = (count * 5) + self.lane_waiting_times[lane]
            lane_analysis[lane] = {
                'vehicle_count': count,
                'waiting_time': self.lane_waiting_times[lane],
                'priority_score': priority_score
            }
        
        return {
            'total_vehicles': total_vehicles,
            'density': density,
            'lane_distribution': lane_counts,
            'lane_analysis': lane_analysis
        }

# ============================================================================
# MODULE 4: Signal Optimizer
# ============================================================================

class SignalOptimizer:
    """Optimizes traffic signal timings"""
    
    def __init__(self):
        self.base_time = 10  # seconds
        self.max_time = 60
        self.emergency_time = 90
        self.priority_factor = 2
    
    def optimize(self, lane_analysis, emergency_detected=False):
        """Calculate optimal signal timings"""
        signal_timings = {}
        
        # Find priority lane
        priority_lane = max(lane_analysis.items(), 
                          key=lambda x: x[1]['priority_score'])[0]
        
        for lane, data in lane_analysis.items():
            if emergency_detected and lane == priority_lane:
                green_time = self.emergency_time
            else:
                score = data['priority_score']
                green_time = self.base_time + (score * self.priority_factor)
                green_time = min(int(green_time), self.max_time)
            
            signal_timings[lane] = {
                'green_time': green_time,
                'is_priority': lane == priority_lane
            }
        
        return signal_timings, priority_lane

# ============================================================================
# MODULE 5: Green Wave Controller
# ============================================================================

class GreenWaveController:
    """Activates green corridor for emergency vehicles"""
    
    def __init__(self):
        self.active = False
        self.route = []
    
    def activate(self, emergency_type, priority_lane):
        """Activate green wave corridor"""
        self.active = True
        # Simulate route (in real system, this would be calculated)
        self.route = [priority_lane, "Intersection-1", "Intersection-2", "Intersection-3"]
        return {
            'active': True,
            'emergency_type': emergency_type,
            'route': self.route,
            'message': f'🚨 Green Wave activated for {emergency_type}'
        }
    
    def deactivate(self):
        """Deactivate green wave"""
        self.active = False
        self.route = []
        return {'active': False, 'route': [], 'message': 'Green Wave deactivated'}

# ============================================================================
# MAIN TRAFFIC SYSTEM
# ============================================================================

class TrafficManagementSystem:
    """Main system integrating all modules"""
    
    def __init__(self):
        print("🚦 Initializing Urban Swarm Traffic Management System...")
        self.vehicle_detector = VehicleDetector()
        self.emergency_detector = EmergencyDetector()
        self.traffic_analyzer = TrafficAnalyzer(num_lanes=4)
        self.signal_optimizer = SignalOptimizer()
        # initialize city and router from green_wave package for real routing
        self.city = City(grid_size=4)
        self.router = EmergencyRouter(self.city)
        self.green_wave = GreenWaveController()
        print("✓ All modules loaded successfully\n")
    
    def process_frame(self, frame):
        """Process single frame through entire pipeline"""
        frame_height, frame_width = frame.shape[:2]
        
        # Step 1: Detect regular vehicles
        vehicle_detections = self.vehicle_detector.detect(frame)
        
        # Step 2: Analyze traffic
        traffic_data = self.traffic_analyzer.analyze(vehicle_detections, frame_width)
        
        # Step 3: Detect emergency vehicles
        emergency_detected, emergency_type, emergency_detections = \
            self.emergency_detector.detect(frame)
        # if no real emergency detected, occasionally simulate one for demo
        if not emergency_detected and (random.random() < 0.02):  # 2% chance per frame
            emergency_detected = True
            emergency_type = 'ambulance'
            emergency_detections = []
        
        # Step 4: Optimize signals
        signal_timings, priority_lane = self.signal_optimizer.optimize(
            traffic_data['lane_analysis'], 
            emergency_detected
        )
        
        # Step 5: Green wave control (use actual router when available)
        if emergency_detected:
            # compute a route using the green_wave routing engine
            try:
                # use fixed start/end or derive from context if available
                route = self.router.compute_emergency_route(0, 15)
            except Exception:
                route = []
            green_wave_status = {
                'active': True,
                'route': route,
                'message': f'🚨 Green Wave activated for {emergency_type}'
            }
        else:
            green_wave_status = self.green_wave.deactivate()
        
        # Compile system state
        system_state = {
            'vehicle_count': traffic_data['total_vehicles'],
            'traffic_density': traffic_data['density'],
            'lane_distribution': traffic_data['lane_distribution'],
            'signal_timings': signal_timings,
            'priority_lane': priority_lane,
            'emergency_detected': emergency_detected,
            'emergency_type': emergency_type if emergency_detected else None,
            'green_wave_active': green_wave_status['active'],
            'green_wave_route': green_wave_status.get('route', [])
        }
        
        # Draw visualizations
        annotated_frame = self._draw_annotations(
            frame, vehicle_detections, emergency_detections, system_state
        )
        
        return system_state, annotated_frame
    
    def _draw_annotations(self, frame, vehicle_detections, emergency_detections, state):
        """Draw bounding boxes and info on frame"""
        annotated = frame.copy()
        
        # Draw regular vehicles (green boxes)
        for det in vehicle_detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['type']} {det['confidence']:.2f}"
            cv2.putText(annotated, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw emergency vehicles (red boxes)
        for det in emergency_detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 0, 255), 3)
            label = f"EMERGENCY: {det['type']} {det['confidence']:.2f}"
            cv2.putText(annotated, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw system info
        y_offset = 30
        cv2.putText(annotated, f"Vehicles: {state['vehicle_count']}", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 30
        cv2.putText(annotated, f"Density: {state['traffic_density']}", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 30
        cv2.putText(annotated, f"Priority: {state['priority_lane']}", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if state['green_wave_active']:
            y_offset += 30
            cv2.putText(annotated, "GREEN WAVE ACTIVE", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        return annotated

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_traffic_system(video_source=0, save_output=True):
    """
    Run the complete traffic management system
    
    Args:
        video_source: 0 for webcam, or path to video file
        save_output: Save system state to JSON
    
    Returns:
        System state dictionary
    """
    system = TrafficManagementSystem()
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("❌ Error: Could not access video source")
        return None
    
    print("🎥 Starting traffic monitoring...")
    print("Press 'q' to quit\n")
    
    latest_state = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame through pipeline
            system_state, annotated_frame = system.process_frame(frame)
            latest_state = system_state
            
            # Save to JSON for dashboard
            if save_output:
                output_path = backend_path / 'system_state.json'
                with open(output_path, 'w') as f:
                    json.dump(system_state, f, indent=2)
                # also copy into frontend directory so simple http server can serve it directly
                try:
                    frontend_copy = backend_path.parent / 'frontend' / 'system_state.json'
                    with open(frontend_copy, 'w') as f2:
                        json.dump(system_state, f2, indent=2)
                except Exception:
                    pass
            
            # Display
            cv2.imshow('Urban Swarm - Traffic Management', annotated_frame)
            
            # Print status
            print(f"\r🚗 Vehicles: {system_state['vehicle_count']} | "
                  f"Density: {system_state['traffic_density']} | "
                  f"Priority: {system_state['priority_lane']} | "
                  f"Emergency: {'YES' if system_state['emergency_detected'] else 'NO'}", 
                  end='')
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\n\n✓ System stopped")
    
    return latest_state

if __name__ == '__main__':
    # start API server in a background thread so frontend can query state
    try:
        from api_server import app as api_app
        import threading
        def run_api():
            # disable flask reloader to avoid double-start
            api_app.run(debug=False, port=5000, use_reloader=False)
        threading.Thread(target=run_api, daemon=True).start()
        print("🖧 API server started on http://localhost:5000")
    except Exception as e:
        print(f"⚠️  Failed to start API server: {e}")
    
    # Run the integrated system
    final_state = run_traffic_system(video_source=0, save_output=True)
    
    if final_state:
        print("\n" + "="*60)
        print("FINAL SYSTEM STATE")
        print("="*60)
        print(json.dumps(final_state, indent=2))
