"""
Main entry point for the Resilient Swarm-Based AI Traffic System backend.
"""
from traffic_controller import TrafficController

def run_simulation():
    controller = TrafficController()

    # Scenario 1: Normal Traffic Data
    print("Running Scenario 1: Normal Traffic Conditions")
    normal_traffic = {
        "Lane A": {"vehicle_count": 15, "waiting_time": 20},
        "Lane B": {"vehicle_count": 5, "waiting_time": 10},
        "Lane C": {"vehicle_count": 8, "waiting_time": 12},
        "Lane D": {"vehicle_count": 3, "waiting_time": 5}
    }
    controller.process_traffic_data(normal_traffic)

    # Scenario 2: Emergency Vehicle Detected
    print("Running Scenario 2: Emergency Vehicle in Lane B")
    emergency_traffic = {
        "Lane A": {"vehicle_count": 15, "waiting_time": 20},
        "Lane B": {"vehicle_count": 5, "waiting_time": 10, "emergency": True},
        "Lane C": {"vehicle_alias": 8, "waiting_time": 12}, # Testing missing field robustness
        "Lane D": {"vehicle_count": 3, "waiting_time": 5}
    }
    controller.process_traffic_data(emergency_traffic)

if __name__ == "__main__":
    run_simulation()
