"""
Main Entry Point for Resilient Swarm-Based AI Traffic System
Emergency Green Wave Simulation
"""

from smart_city.city import City
from smart_city.traffic_agents import TrafficAgentManager
from smart_city.vehicle_system import VehicleManager
from smart_city.routing_engine import EmergencyRouter
from smart_city.swarm_controller import SwarmController
from smart_city.simulator import TrafficSimulator

def main():
    print("=" * 60)
    print("🚨 RESILIENT SWARM-BASED AI TRAFFIC SYSTEM 🚨")
    print("Emergency Green Wave Simulation")
    print("=" * 60)
    
    # Initialize city infrastructure
    print("\n🏙️  Building 4x4 city grid...")
    city = City(grid_size=4)
    
    # Initialize traffic signal agents
    print("🚦 Initializing traffic signal agents...")
    agent_manager = TrafficAgentManager(city)
    
    # Initialize vehicle system
    print("🚗 Spawning traffic vehicles...")
    vehicle_manager = VehicleManager(city, num_vehicles=15)
    
    # Initialize emergency routing
    print("🚑 Setting up emergency routing system...")
    emergency_router = EmergencyRouter(city)
    
    # Initialize swarm controller
    print("🧠 Activating swarm intelligence...")
    swarm_controller = SwarmController(agent_manager)
    
    # Initialize simulator
    print("📊 Starting traffic simulation...")
    simulator = TrafficSimulator(
        city=city,
        agent_manager=agent_manager,
        vehicle_manager=vehicle_manager,
        emergency_router=emergency_router,
        swarm_controller=swarm_controller
    )
    
    # Emergency scenario
    start_intersection = 0   # Top-left corner
    end_intersection = 15    # Bottom-right corner
    
    print(f"\n🚨 EMERGENCY ALERT!")
    print(f"Ambulance dispatched from intersection {start_intersection} to {end_intersection}")
    
    # Run simulation
    simulator.run_emergency_simulation(start_intersection, end_intersection)

if __name__ == "__main__":
    main()