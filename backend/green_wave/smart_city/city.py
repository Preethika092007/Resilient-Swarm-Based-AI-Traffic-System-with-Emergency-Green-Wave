"""
City Infrastructure Module
Manages the 4x4 grid network of intersections and roads
"""

import networkx as nx
import random

class City:
    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.graph = self._build_city_grid()
        self.positions = self._compute_positions()
        self.edge_data = self._initialize_road_data()
    
    def _build_city_grid(self):
        """Build 4x4 grid network of intersections"""
        G = nx.grid_2d_graph(self.grid_size, self.grid_size)
        # Convert to integer node labels (0-15)
        G = nx.convert_node_labels_to_integers(G)
        return G
    
    def _compute_positions(self):
        """Compute clean grid positions for intersections"""
        positions = {}
        spacing = 4  # Increased spacing for better visibility
        
        for node in self.graph.nodes():
            row = node // self.grid_size
            col = node % self.grid_size
            # Create perfect grid layout
            positions[node] = (col * spacing, -row * spacing)
        
        return positions
    
    def _initialize_road_data(self):
        """Initialize road data: distance, congestion, flow"""
        edge_data = {}
        
        for u, v in self.graph.edges():
            # Base distance between adjacent intersections
            distance = random.randint(200, 500)  # meters
            
            # Initial traffic congestion (1-10 scale)
            congestion = random.randint(1, 8)
            
            # Vehicle flow rate
            flow = random.randint(5, 20)
            
            # Store bidirectional data
            edge_data[(u, v)] = {
                'distance': distance,
                'congestion': congestion,
                'flow': flow
            }
            edge_data[(v, u)] = {
                'distance': distance,
                'congestion': congestion,
                'flow': flow
            }
        
        return edge_data
    
    def get_edge_cost(self, u, v, congestion_weight=0.6):
        """Calculate edge cost for routing (distance + congestion)"""
        if (u, v) not in self.edge_data:
            return float('inf')
        
        data = self.edge_data[(u, v)]
        return data['distance'] + congestion_weight * data['congestion']
    
    def update_congestion(self, vehicle_positions):
        """Update road congestion based on vehicle positions"""
        # Reset congestion with natural fluctuation
        for edge in self.edge_data:
            current = self.edge_data[edge]['congestion']
            # Random fluctuation ±1
            change = random.uniform(-1, 1)
            new_congestion = max(1, min(10, current + change))
            self.edge_data[edge]['congestion'] = new_congestion
        
        # Increase congestion where vehicles are present
        vehicle_count = {}
        for pos in vehicle_positions:
            vehicle_count[pos] = vehicle_count.get(pos, 0) + 1
        
        for node, count in vehicle_count.items():
            # Increase congestion on roads connected to this intersection
            for neighbor in self.graph.neighbors(node):
                edge = (node, neighbor)
                if edge in self.edge_data:
                    self.edge_data[edge]['congestion'] = min(10, 
                        self.edge_data[edge]['congestion'] + count * 0.5)
    
    def get_neighbors(self, node):
        """Get neighboring intersections"""
        return list(self.graph.neighbors(node))
    
    def get_all_nodes(self):
        """Get all intersection nodes"""
        return list(self.graph.nodes())
    
    def get_all_edges(self):
        """Get all road edges"""
        return list(self.graph.edges())