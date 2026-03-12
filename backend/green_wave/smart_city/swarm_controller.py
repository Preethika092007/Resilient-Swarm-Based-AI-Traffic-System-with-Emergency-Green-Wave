"""
Swarm Controller Module
Decentralized coordination of traffic signals using swarm intelligence
"""

class SwarmController:
    def __init__(self, agent_manager):
        self.agent_manager = agent_manager
        self.communication_log = []
    
    def activate_emergency_corridor(self, route):
        """Activate emergency green wave corridor"""
        print("\n🧠 SWARM INTELLIGENCE ACTIVATION")
        print("Coordinating traffic signals for emergency corridor...")
        
        # Reset all signals first
        self.agent_manager.reset_all_signals()
        
        # Activate green corridor
        self.agent_manager.set_emergency_corridor(route)
        
        # Log swarm communication
        self._log_swarm_communication(route)
    
    def _log_swarm_communication(self, route):
        """Simulate swarm communication between signals"""
        print("\n📡 Swarm Communication Network:")
        
        for i in range(len(route) - 1):
            current_signal = route[i]
            next_signal = route[i + 1]
            
            message = f"Signal {current_signal} → notifying Signal {next_signal} to prepare green corridor"
            print(f"  {message}")
            self.communication_log.append(message)
            
            # Send message to agent
            if next_signal in self.agent_manager.agents:
                agent = self.agent_manager.get_agent(next_signal)
                agent.receive_message({
                    'type': 'emergency_prepare',
                    'from': current_signal,
                    'action': 'prepare_green'
                })
    
    def coordinate_normal_traffic(self):
        """Coordinate normal traffic flow using priority scores"""
        agents = self.agent_manager.get_all_agents()
        
        # Calculate priority scores for all intersections
        priorities = {}
        for intersection_id, agent in agents.items():
            priorities[intersection_id] = agent.compute_priority_score()
        
        # Sort by priority (highest first)
        sorted_priorities = sorted(priorities.items(), key=lambda x: x[1], reverse=True)
        
        # Give green light to highest priority intersections
        green_count = 0
        max_green = len(agents) // 3  # Allow 1/3 of signals to be green
        
        for intersection_id, priority in sorted_priorities:
            if green_count < max_green:
                agents[intersection_id].set_signal_state("green")
                green_count += 1
            else:
                agents[intersection_id].set_signal_state("red")
    
    def propagate_traffic_updates(self):
        """Propagate traffic state updates through swarm network"""
        agents = self.agent_manager.get_all_agents()
        
        for intersection_id, agent in agents.items():
            # Share traffic information with neighbors
            for neighbor_id in agent.neighbors:
                if neighbor_id in agents:
                    neighbor_agent = agents[neighbor_id]
                    
                    # Send traffic state information
                    message = {
                        'type': 'traffic_update',
                        'from': intersection_id,
                        'density': agent.vehicle_density,
                        'queue': agent.queue_length,
                        'waiting': agent.waiting_time
                    }
                    neighbor_agent.receive_message(message)
    
    def update_swarm_intelligence(self):
        """Update swarm intelligence coordination"""
        # Update all agent states
        self.agent_manager.update_all_agents()
        
        # Propagate information through swarm
        self.propagate_traffic_updates()
        
        # Clear old messages
        for agent in self.agent_manager.get_all_agents().values():
            agent.clear_messages()
    
    def get_communication_log(self):
        """Get swarm communication history"""
        return self.communication_log
    
    def clear_communication_log(self):
        """Clear communication log"""
        self.communication_log = []
    
    def analyze_swarm_performance(self):
        """Analyze swarm coordination performance"""
        agents = self.agent_manager.get_all_agents()
        
        total_priority = sum(agent.compute_priority_score() for agent in agents.values())
        avg_priority = total_priority / len(agents)
        
        green_signals = sum(1 for agent in agents.values() if agent.signal_state == "green")
        green_ratio = green_signals / len(agents)
        
        return {
            'total_intersections': len(agents),
            'average_priority': round(avg_priority, 2),
            'green_signals': green_signals,
            'green_ratio': round(green_ratio, 2),
            'communication_messages': len(self.communication_log)
        }