"""
Traffic Density & Lane Analysis Module
Backend Logic for Smart Traffic System
"""

# Thresholds for density classification
DENSITY_THRESHOLDS = {
    "LOW": (0, 4),
    "MEDIUM": (5, 9),
    "HIGH": (10, float('inf'))
}

# Simulated waiting times for lanes (in seconds)
# In a real system, these would be tracked by a timer
lane_waiting_times = {
    "Lane A": 0,
    "Lane B": 0,
    "Lane C": 0,
    "Lane D": 0
}

def map_x_to_lane(x_coord, frame_width=800):
    """
    Maps an X coordinate from a video frame to a specific Lane label.
    Assumes 4 equal lanes.
    """
    lane_width = frame_width / 4
    if x_coord < lane_width:
        return "Lane A"
    elif x_coord < lane_width * 2:
        return "Lane B"
    elif x_coord < lane_width * 3:
        return "Lane C"
    else:
        return "Lane D"

def count_vehicles_per_lane(detections, frame_width=800):
    """
    Counts vehicles in each lane based on raw YOLO detection data.
    Assumes detections is a list of dicts: {'x_center': 150, 'label': 'car', ...}
    """
    counts = {"Lane A": 0, "Lane B": 0, "Lane C": 0, "Lane D": 0}
    for det in detections:
        # If Member 1 already provided the lane, use it
        lane = det.get('lane')
        
        # Otherwise, calculate it from the X coordinate
        if not lane and 'x_center' in det:
            lane = map_x_to_lane(det['x_center'], frame_width)
            
        if lane in counts:
            counts[lane] += 1
    return counts

def calculate_density(vehicle_count):
    """
    Categorizes traffic density based on predefined thresholds.
    0-4: LOW, 5-9: MEDIUM, 10+: HIGH
    """
    if vehicle_count <= 4:
        return "LOW"
    elif vehicle_count <= 9:
        return "MEDIUM"
    else:
        return "HIGH"

def calculate_priority_score(vehicle_count, waiting_time):
    """
    Calculates a priority score for a lane.
    Formula: (Vehicle Count * 5) + Waiting Time
    """
    return (vehicle_count * 5) + waiting_time

def select_priority_lane(lane_results):
    """
    Determines which lane should receive the green signal based on the highest priority score.
    """
    best_lane = None
    highest_score = -1

    for lane, data in lane_results.items():
        if data['priority_score'] > highest_score:
            highest_score = data['priority_score']
            best_lane = lane
    
    return best_lane

def process_traffic_analysis(detections, frame_width=800):
    """
    Main processing function to analyze traffic and determine signal priority.
    """
    # 1. Count vehicles (using coordinate mapping)
    lane_counts = count_vehicles_per_lane(detections, frame_width)
    
    # Update internal waiting times (simulation logic)
    # Increment waiting time for all lanes; in a real loop, you'd reset the one that got green
    for lane in lane_waiting_times:
        lane_waiting_times[lane] += 1 

    results = {}
    
    # 2 & 3. Calculate Density and Priority Score for each lane
    for lane, count in lane_counts.items():
        results[lane] = {
            "vehicle_count": count,
            "density": calculate_density(count),
            "priority_score": calculate_priority_score(count, lane_waiting_times[lane])
        }

    # 4. Select priority lane for green signal
    priority_lane = select_priority_lane(results)
    
    return results, priority_lane

# --- Demo / Integration Test ---
if __name__ == "__main__":
    # Simulated YOLO discovery output (Raw coordinates from Member 1)
    mock_detections = [
        {'x_center': 50, 'type': 'car'}, {'x_center': 150, 'type': 'bus'}, # Lane A
        {'x_center': 250, 'type': 'car'}, {'x_center': 350, 'type': 'bike'}, # Lane B
        {'x_center': 450, 'type': 'car'}, # Lane C
        {'x_center': 650, 'type': 'truck'}, {'x_center': 750, 'type': 'car'} # Lane D
    ]

    analysis, green_signal = process_traffic_analysis(mock_detections, frame_width=800)

    print("--- Traffic Analysis Results ---")
    for lane, data in analysis.items():
        print(f"{lane}: {data['vehicle_count']} vehicles → {data['density']} (Score: {data['priority_score']})")
    
    print(f"\nGreen Signal → {green_signal}")
