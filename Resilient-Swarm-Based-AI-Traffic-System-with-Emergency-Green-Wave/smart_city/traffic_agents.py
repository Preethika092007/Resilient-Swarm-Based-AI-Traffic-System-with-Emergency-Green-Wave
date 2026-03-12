"""
Traffic Signal Agents Module
Autonomous traffic signal agents with swarm intelligence
"""

import random

class TrafficAgent:
    def __init__(self, intersection_id, neighbors):
        self.intersection_id = intersection_id
        self.neighbors = neighbors
        
        # Traffic state variables
        self.vehicle_density = random.randint(2, 8)
        self.queue_length = random.randint(0, 5)
        self.waiting_time = random.uniform(0, 3.0)
        self.signal_state = "red"  # red or green
        
        # Communication
        self.messages = []
    
    def update_traffic_state(self):
        """Update traffic conditions with random fluctuations"""
        # Vehicle density changes
        density_change = random.uniform(-1.5, 2.0)
        self.vehicle_density = max(0, self.vehicle_density + density_change)
        
        # Queue length changes
        queue_change = random.randint(-2, 3)
        self.queue_length = max(0, self.queue_length + queue_change)
        
        # Waiting time changes
        time_change = random.uniform(-0.5, 1.0)
        self.waiting_time = max(0, self.waiting_time + time_change)
    
    def compute_priority_score(self):
        """Calculate priority score for signal timing"""
        return (self.vehicle_density * 0.5 + 
                self.queue_length * 0.3 + 
                self.waiting_time * 0.2)
    
    def set_signal_state(self, state):
        """Set traffic signal state"""
        self.signal_state = state
    
    def receive_message(self, message):
        """Receive communication from other agents"""
        self.messages.append(message)
    
    def clear_messages(self):
        """Clear received messages"""
        self.messages = []

class TrafficAgentManager:
    def __init__(self, city):
        self.city = city
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize traffic agents for all intersections"""
        for node in self.city.get_all_nodes():
            neighbors = self.city.get_neighbors(node)
            self.agents[node] = TrafficAgent(node, neighbors)
    
    def update_all_agents(self):
        """Update all traffic agents"""
        for agent in self.agents.values():
            agent.update_traffic_state()
    
    def get_agent(self, intersection_id):
        """Get specific traffic agent"""
        return self.agents.get(intersection_id)
    
    def get_all_agents(self):
        """Get all traffic agents"""
        return self.agents
    
    def set_emergency_corridor(self, route):
        """Set emergency corridor signals to green"""
        for intersection_id in route:
            if intersection_id in self.agents:
                self.agents[intersection_id].set_signal_state("green")
    
    def reset_all_signals(self):
        """Reset all signals to red"""
        for agent in self.agents.values():
            agent.set_signal_state("red")
    
    def get_intersection_stats(self, intersection_id):
        """Get traffic statistics for intersection"""
        if intersection_id not in self.agents:
            return None
        
        agent = self.agents[intersection_id]
        return {
            'density': round(agent.vehicle_density, 1),
            'queue': round(agent.queue_length, 1),
            'waiting': round(agent.waiting_time, 1),
            'priority': round(agent.compute_priority_score(), 2),
            'signal': agent.signal_state
        }