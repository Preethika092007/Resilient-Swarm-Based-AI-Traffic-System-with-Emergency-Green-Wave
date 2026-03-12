"""
Module for simulating traffic signal logic and switching.
"""
from typing import Dict
import signal_optimizer

class TrafficController:
    def __init__(self):
        self.current_green_lane = None

    def process_traffic_data(self, traffic_data: Dict[str, Dict]):
        """
        Receives traffic input, calls the optimizer, and decides signal order.
        """
        print("\n" + "="*40)
        print("Traffic Signal Optimization Result:")
        print("="*40)

        # 1. Rank lanes based on priority
        ranked_lanes = signal_optimizer.rank_lanes(traffic_data)

        # 2. Calculate green times and prepare results
        results = []
        for lane_id, score in ranked_lanes:
            green_time = signal_optimizer.calculate_green_time(score)
            results.append({
                "lane": lane_id,
                "priority": score,
                "green_time": green_time
            })
            
            # Print individual lane results
            # For emergency, we display a special tag
            display_score = f"{score - 1000} (EMERGENCY)" if score >= 1000 else f"{int(score)}"
            print(f"{lane_id} → Priority: {display_score} → Green Time: {green_time}s")

        print("\nGreen Order:")
        for idx, res in enumerate(results, 1):
            print(f"{idx} → {res['lane']}")
        
        # 3. Simulate Signal Switching (Logic for first lane)
        if results:
            self.switch_signal(results[0]["lane"], results[0]["green_time"])

    def switch_signal(self, lane_id: str, duration: int):
        """
        Simulates the switching of a signal to green.
        """
        self.current_green_lane = lane_id
        print(f"\n[CONTROL] Signal {lane_id} is now GREEN for {duration} seconds.")
        print("="*40 + "\n")
