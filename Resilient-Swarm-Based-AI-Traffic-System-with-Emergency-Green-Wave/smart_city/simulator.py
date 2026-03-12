"""
Traffic Simulation Engine
Main simulation loop with NetworkX and Matplotlib visualization
"""

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as mpatches

class TrafficSimulator:
    def __init__(self, city, agent_manager, vehicle_manager, emergency_router, swarm_controller):
        self.city = city
        self.agent_manager = agent_manager
        self.vehicle_manager = vehicle_manager
        self.emergency_router = emergency_router
        self.swarm_controller = swarm_controller
        
        # Enhanced visualization setup
        plt.style.use('default')  # Ensure clean style
        self.fig, self.ax = plt.subplots(figsize=(14, 12))  # Larger figure
        self.fig.patch.set_facecolor('#2c2c2c')  # Dark frame
        self.ax.set_facecolor('#f5f5dc')  # City background
    
    def run_emergency_simulation(self, start, destination):
        """Run complete emergency simulation"""
        # Compute emergency route
        route = self.emergency_router.compute_emergency_route(start, destination)
        
        print(f"\n🛣️  Emergency Route Calculated: {' → '.join(map(str, route))}")
        print(f"Route Length: {len(route)} intersections")
        
        # Analyze route
        route_analysis = self.emergency_router.analyze_route_efficiency(route)
        print(f"Route Analysis: {route_analysis}")
        
        # Activate emergency corridor
        self.swarm_controller.activate_emergency_corridor(route)
        
        # Spawn emergency vehicle
        self.vehicle_manager.spawn_emergency_vehicle(start, destination)
        
        # Run simulation steps
        print(f"\n🚑 Starting ambulance movement...")
        
        for step in range(len(route)):
            print(f"\nStep {step + 1}/{len(route)}: Ambulance at intersection {route[step]}")
            
            # Update simulation state
            self._update_simulation_state(route, step)
            
            # Draw current frame
            self._draw_simulation_frame(route, step)
            
            # Pause for visualization
            plt.pause(1.5)
        
        print("\n✅ Emergency vehicle reached destination!")
        print("🏥 Patient delivered to hospital successfully!")
        
        # Show final statistics
        self._show_final_statistics()
        
        # Keep plot open
        plt.show()
    
    def _update_simulation_state(self, route, step):
        """Update all simulation components"""
        # Move emergency vehicle
        self.vehicle_manager.move_emergency_vehicle(route, step)
        
        # Move regular vehicles
        self.vehicle_manager.move_all_vehicles()
        
        # Update traffic congestion
        vehicle_positions = self.vehicle_manager.get_vehicle_positions()
        self.city.update_congestion(vehicle_positions)
        
        # Update swarm intelligence
        self.swarm_controller.update_swarm_intelligence()
    
    def _draw_simulation_frame(self, route, step):
        """Draw enhanced simulation frame with realistic city appearance"""
        self.ax.clear()
        # Set background to a city-like color
        self.ax.set_facecolor('#f5f5dc')  # Beige background like satellite view
        
        # Draw elements in proper layering order
        self._draw_road_network()           # Layer 1-4: Roads and lane markers
        self._draw_emergency_corridor(route, step)  # Layer 5-8: Emergency corridor
        self._draw_traffic_signals(route)   # Layer 9-14: Traffic signals and info
        self._draw_vehicles()              # Layer 15-16: Regular vehicles
        self._draw_emergency_vehicle()     # Layer 17-21: Emergency vehicle
        
        # Add simulation information
        self._add_simulation_info(route, step)
        
        # Set clean layout with proper bounds
        self.ax.set_xlim(-1, (self.city.grid_size - 1) * 4 + 1)
        self.ax.set_ylim(-(self.city.grid_size - 1) * 4 - 1, 1)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Add subtle grid lines for city block effect
        for i in range(self.city.grid_size):
            x = i * 4
            y = -i * 4
            self.ax.axvline(x=x, color='#e0e0e0', alpha=0.3, linewidth=0.5, zorder=0)
            self.ax.axhline(y=y, color='#e0e0e0', alpha=0.3, linewidth=0.5, zorder=0)
        
        plt.tight_layout()
    
    def _draw_road_network(self):
        """Draw realistic road network with lanes"""
        for u, v in self.city.get_all_edges():
            x1, y1 = self.city.positions[u]
            x2, y2 = self.city.positions[v]
            
            # Draw road base (dark asphalt)
            self.ax.plot([x1, x2], [y1, y2], color='#2c2c2c', linewidth=20, 
                        solid_capstyle='round', zorder=1)
            
            # Draw road surface (lighter gray)
            self.ax.plot([x1, x2], [y1, y2], color='#404040', linewidth=16, 
                        solid_capstyle='round', zorder=2)
            
            # Draw lane divider (yellow dashed line)
            self.ax.plot([x1, x2], [y1, y2], color='#FFD700', linewidth=2, 
                        linestyle='--', alpha=0.8, zorder=3)
            
            # Add road emoji for longer roads
            distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if distance > 2.5:  # Only on longer roads
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax.text(mid_x, mid_y + 0.3, '🛣️', fontsize=8, 
                           ha='center', va='center', alpha=0.6, zorder=4)
    
    def _draw_emergency_corridor(self, route, step):
        """Draw bright green emergency corridor with enhanced visibility"""
        if len(route) > 1:
            # Create edge list for emergency route
            route_edges = [(route[i], route[i+1]) for i in range(len(route)-1)]
            
            for u, v in route_edges:
                x1, y1 = self.city.positions[u]
                x2, y2 = self.city.positions[v]
                
                # Draw glowing emergency corridor
                # Outer glow
                self.ax.plot([x1, x2], [y1, y2], color='#00FF00', linewidth=28, 
                           alpha=0.3, solid_capstyle='round', zorder=5)
                # Middle layer
                self.ax.plot([x1, x2], [y1, y2], color='#00FF00', linewidth=22, 
                           alpha=0.6, solid_capstyle='round', zorder=6)
                # Inner bright core
                self.ax.plot([x1, x2], [y1, y2], color='#FFFFFF', linewidth=16, 
                           alpha=0.9, solid_capstyle='round', zorder=7)
                # Center line
                self.ax.plot([x1, x2], [y1, y2], color='#00FF00', linewidth=12, 
                           alpha=1.0, solid_capstyle='round', zorder=8)
    
    def _draw_traffic_signals(self, route):
        """Draw realistic traffic signals with detailed information"""
        for node in self.city.get_all_nodes():
            x, y = self.city.positions[node]
            
            # Get agent stats
            stats = self.agent_manager.get_intersection_stats(node)
            
            # Draw intersection base (concrete pad)
            intersection_base = plt.Circle((x, y), 0.4, color='#D3D3D3', 
                                         alpha=0.8, zorder=9)
            self.ax.add_patch(intersection_base)
            
            # Draw traffic signal pole (above intersection)
            pole_x, pole_y = x, y + 0.8
            self.ax.plot([x, pole_x], [y + 0.4, pole_y], color='#2F4F4F', 
                        linewidth=6, solid_capstyle='round', zorder=10)
            
            # Draw traffic signal box
            signal_box = plt.Rectangle((pole_x - 0.15, pole_y - 0.1), 0.3, 0.2, 
                                     facecolor='#1C1C1C', edgecolor='#FFD700', 
                                     linewidth=1, zorder=11)
            self.ax.add_patch(signal_box)
            
            # Draw traffic signal emoji (large and prominent)
            self.ax.text(pole_x, pole_y, '🚦', fontsize=24, ha='center', va='center', zorder=12)
            
            # Draw signal state indicator
            if stats['signal'] == 'green':
                # Green light active
                self.ax.text(pole_x + 0.3, pole_y, '🟢', fontsize=16, ha='center', va='center', zorder=13)
                signal_status = "GREEN"
                status_color = '#00FF00'
            else:
                # Red light active
                self.ax.text(pole_x + 0.3, pole_y, '🔴', fontsize=16, ha='center', va='center', zorder=13)
                signal_status = "RED"
                status_color = '#FF0000'
            
            # Draw intersection information panel
            info_y = y - 0.8
            
            # Node ID
            self.ax.text(x, info_y, f"Node: {node}", fontsize=10, ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                 edgecolor='black', alpha=0.9), zorder=14)
            
            # Vehicle density
            density = int(stats['density'])
            self.ax.text(x, info_y - 0.3, f"Cars: {density}", fontsize=9, ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', 
                                 alpha=0.8), zorder=14)
            
            # Signal status
            self.ax.text(x, info_y - 0.6, signal_status, fontsize=8, ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=status_color, 
                                 alpha=0.7), color='white', weight='bold', zorder=14)
    
    def _draw_vehicles(self):
        """Draw realistic moving vehicles with proper positioning"""
        vehicle_positions = self.vehicle_manager.get_vehicle_positions()
        
        # Count vehicles at each intersection
        position_counts = {}
        for pos in vehicle_positions:
            position_counts[pos] = position_counts.get(pos, 0) + 1
        
        # Draw vehicles with realistic positioning
        for pos, count in position_counts.items():
            x, y = self.city.positions[pos]
            
            # Create a circle of vehicles around the intersection
            import math
            for i in range(min(count, 6)):  # Show max 6 vehicles per intersection
                if count == 1:
                    # Single vehicle - place slightly offset
                    offset_x, offset_y = 0.2, -0.2
                else:
                    # Multiple vehicles - arrange in circle
                    angle = (2 * math.pi * i) / min(count, 6)
                    radius = 0.3 + (count - 1) * 0.05  # Larger radius for more vehicles
                    offset_x = radius * math.cos(angle)
                    offset_y = radius * math.sin(angle)
                
                vehicle_x = x + offset_x
                vehicle_y = y + offset_y
                
                # Draw vehicle with shadow effect
                self.ax.text(vehicle_x + 0.02, vehicle_y - 0.02, '🚗', 
                           fontsize=12, ha='center', va='center', alpha=0.3, zorder=15)
                self.ax.text(vehicle_x, vehicle_y, '🚗', 
                           fontsize=12, ha='center', va='center', zorder=16)
    
    def _draw_emergency_vehicle(self):
        """Draw prominent emergency vehicle with animation effects"""
        ambulance_pos = self.vehicle_manager.get_emergency_position()
        if ambulance_pos is not None:
            x, y = self.city.positions[ambulance_pos]
            
            # Draw multiple glow layers for dramatic effect
            glow_colors = ['#FF0000', '#FF3333', '#FF6666']
            glow_sizes = [1200, 800, 400]
            
            for color, size in zip(glow_colors, glow_sizes):
                self.ax.scatter(x, y, s=size, c=color, alpha=0.2, zorder=17)
            
            # Draw ambulance shadow
            self.ax.text(x + 0.05, y - 0.05, '🚑', fontsize=32, ha='center', va='center', 
                        alpha=0.3, zorder=18)
            
            # Draw main ambulance (large and prominent)
            self.ax.text(x, y, '🚑', fontsize=32, ha='center', va='center', zorder=19)
            
            # Add emergency label
            self.ax.text(x, y - 1.2, 'EMERGENCY', fontsize=10, ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.9),
                        color='white', weight='bold', zorder=20)
            
            # Add flashing effect (alternating visibility)
            import random
            if random.random() > 0.5:  # 50% chance to show flashing lights
                # Left flasher
                self.ax.text(x - 0.2, y + 0.2, '🔴', fontsize=8, ha='center', va='center', zorder=21)
                # Right flasher  
                self.ax.text(x + 0.2, y + 0.2, '🔵', fontsize=8, ha='center', va='center', zorder=21)
    
    def _add_simulation_info(self, route, step):
        """Add enhanced simulation information and legend"""
        # Enhanced title with better styling
        title_text = '🚨 SMART CITY TRAFFIC SYSTEM 🚨\nEmergency Green Wave Coordination'
        self.ax.text(0.5, 0.95, title_text, transform=self.ax.transAxes,
                    fontsize=16, fontweight='bold', ha='center', va='top',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a1a', 
                             edgecolor='#FFD700', linewidth=2, alpha=0.9),
                    color='#FFD700')
        
        # Current step info with better styling
        current_intersection = route[step]
        progress_percent = int((step + 1) / len(route) * 100)
        info_text = f"Step {step + 1}/{len(route)} ({progress_percent}%) | Ambulance at Intersection {current_intersection}"
        
        self.ax.text(0.02, 0.02, info_text, transform=self.ax.transAxes,
                    fontsize=11, ha='left', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='#FF4444', 
                             edgecolor='white', linewidth=1, alpha=0.95),
                    color='white', weight='bold')
        
        # Enhanced legend with more detail
        legend_elements = [
            mpatches.Patch(color='#00FF00', label='🟢 Emergency Corridor'),
            mpatches.Patch(color='#404040', label='🛣️ City Roads'),
            mpatches.Rectangle((0,0),1,1, facecolor='red', alpha=0.3, label='🚑 Emergency Vehicle'),
            mpatches.Patch(color='#FFD700', label='🚦 Traffic Signals'),
            mpatches.Patch(color='#D3D3D3', label='🏙️ Intersections'),
            mpatches.Rectangle((0,0),1,1, facecolor='blue', alpha=0.7, label='🚗 Regular Traffic')
        ]
        
        legend = self.ax.legend(handles=legend_elements, loc='upper right', 
                               bbox_to_anchor=(0.98, 0.88), fontsize=9,
                               fancybox=True, shadow=True, framealpha=0.9,
                               facecolor='white', edgecolor='black')
        legend.get_frame().set_linewidth(1.5)
    
    def _show_final_statistics(self):
        """Show final simulation statistics"""
        print("\n" + "="*50)
        print("📊 SIMULATION STATISTICS")
        print("="*50)
        
        # Swarm performance
        swarm_stats = self.swarm_controller.analyze_swarm_performance()
        print(f"🧠 Swarm Intelligence:")
        print(f"   - Total Intersections: {swarm_stats['total_intersections']}")
        print(f"   - Average Priority Score: {swarm_stats['average_priority']}")
        print(f"   - Green Signals: {swarm_stats['green_signals']}")
        print(f"   - Communication Messages: {swarm_stats['communication_messages']}")
        
        # Vehicle statistics
        total_vehicles = len(self.vehicle_manager.get_all_vehicles())
        print(f"\n🚗 Traffic Flow:")
        print(f"   - Total Vehicles: {total_vehicles}")
        print(f"   - Emergency Vehicle: {'✅ Delivered' if self.vehicle_manager.has_emergency_vehicle() else '❌ None'}")
        
        # Network statistics
        total_intersections = len(self.city.get_all_nodes())
        total_roads = len(self.city.get_all_edges())
        print(f"\n🏙️ City Network:")
        print(f"   - Intersections: {total_intersections}")
        print(f"   - Roads: {total_roads}")
        
        print("="*50)