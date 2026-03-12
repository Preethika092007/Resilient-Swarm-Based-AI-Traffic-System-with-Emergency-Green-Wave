"""
Emergency Routing Engine
AI-powered routing for emergency vehicles using A* search
"""

import networkx as nx

class EmergencyRouter:
    def __init__(self, city, congestion_weight=0.6):
        self.city = city
        self.congestion_weight = congestion_weight
    
    def compute_emergency_route(self, start, destination):
        """
        Compute optimal emergency route using A* search
        Cost = distance + (congestion_weight * congestion)
        """
        def cost_function(u, v, edge_data):
            # Get edge cost considering distance and congestion
            return self.city.get_edge_cost(u, v, self.congestion_weight)
        
        try:
            # Use NetworkX A* algorithm
            route = nx.astar_path(
                self.city.graph,
                start,
                destination,
                heuristic=self._manhattan_distance,
                weight=cost_function
            )
            return route
        except nx.NetworkXNoPath:
            # Fallback to shortest path if A* fails
            return nx.shortest_path(self.city.graph, start, destination)
    
    def _manhattan_distance(self, node1, node2):
        """Manhattan distance heuristic for A* search"""
        pos1 = self.city.positions[node1]
        pos2 = self.city.positions[node2]
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_route_cost(self, route):
        """Calculate total cost of a route"""
        total_cost = 0
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            total_cost += self.city.get_edge_cost(u, v, self.congestion_weight)
        return total_cost
    
    def get_alternative_routes(self, start, destination, num_routes=3):
        """Get multiple alternative routes"""
        routes = []
        
        # Primary route
        primary_route = self.compute_emergency_route(start, destination)
        routes.append(primary_route)
        
        # Try to find alternative routes by temporarily increasing edge costs
        for _ in range(num_routes - 1):
            # Temporarily increase costs of primary route edges
            temp_increases = {}
            for i in range(len(primary_route) - 1):
                u, v = primary_route[i], primary_route[i + 1]
                if (u, v) in self.city.edge_data:
                    temp_increases[(u, v)] = self.city.edge_data[(u, v)]['congestion']
                    self.city.edge_data[(u, v)]['congestion'] += 5
            
            try:
                alt_route = self.compute_emergency_route(start, destination)
                if alt_route not in routes:
                    routes.append(alt_route)
            except:
                pass
            
            # Restore original costs
            for edge, original_cost in temp_increases.items():
                self.city.edge_data[edge]['congestion'] = original_cost
        
        return routes
    
    def analyze_route_efficiency(self, route):
        """Analyze route efficiency metrics"""
        if len(route) < 2:
            return {}
        
        total_distance = 0
        total_congestion = 0
        
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            edge_data = self.city.edge_data.get((u, v), {})
            total_distance += edge_data.get('distance', 0)
            total_congestion += edge_data.get('congestion', 0)
        
        return {
            'total_distance': total_distance,
            'average_congestion': total_congestion / (len(route) - 1),
            'route_length': len(route),
            'total_cost': self.get_route_cost(route)
        }