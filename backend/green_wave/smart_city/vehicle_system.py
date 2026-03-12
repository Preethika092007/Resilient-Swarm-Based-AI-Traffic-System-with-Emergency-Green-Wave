"""
Vehicle System Module
Manages moving vehicles and traffic dynamics
"""

import random

class Vehicle:
    def __init__(self, vehicle_id, initial_position):
        self.vehicle_id = vehicle_id
        self.position = initial_position
        self.destination = None
        self.path = []
    
    def move_to_neighbor(self, city):
        """Move to a random neighboring intersection"""
        neighbors = city.get_neighbors(self.position)
        if neighbors:
            self.position = random.choice(neighbors)
    
    def get_position(self):
        """Get current position"""
        return self.position

class EmergencyVehicle(Vehicle):
    def __init__(self, vehicle_id, initial_position, destination):
        super().__init__(vehicle_id, initial_position)
        self.destination = destination
        self.vehicle_type = "ambulance"
    
    def move_along_route(self, route, step):
        """Move along predetermined emergency route"""
        if step < len(route):
            self.position = route[step]

class VehicleManager:
    def __init__(self, city, num_vehicles=15):
        self.city = city
        self.vehicles = []
        self.emergency_vehicle = None
        self._spawn_vehicles(num_vehicles)
    
    def _spawn_vehicles(self, num_vehicles):
        """Spawn vehicles at random intersections"""
        nodes = self.city.get_all_nodes()
        
        for i in range(num_vehicles):
            position = random.choice(nodes)
            vehicle = Vehicle(i, position)
            self.vehicles.append(vehicle)
    
    def move_all_vehicles(self):
        """Move all regular vehicles"""
        for vehicle in self.vehicles:
            vehicle.move_to_neighbor(self.city)
    
    def spawn_emergency_vehicle(self, start, destination):
        """Spawn emergency vehicle (ambulance)"""
        self.emergency_vehicle = EmergencyVehicle("ambulance", start, destination)
    
    def move_emergency_vehicle(self, route, step):
        """Move emergency vehicle along route"""
        if self.emergency_vehicle:
            self.emergency_vehicle.move_along_route(route, step)
    
    def get_vehicle_positions(self):
        """Get positions of all regular vehicles"""
        return [vehicle.get_position() for vehicle in self.vehicles]
    
    def get_emergency_position(self):
        """Get emergency vehicle position"""
        if self.emergency_vehicle:
            return self.emergency_vehicle.get_position()
        return None
    
    def get_vehicle_count_at_intersection(self, intersection_id):
        """Count vehicles at specific intersection"""
        count = 0
        for vehicle in self.vehicles:
            if vehicle.get_position() == intersection_id:
                count += 1
        return count
    
    def get_all_vehicles(self):
        """Get all vehicles"""
        return self.vehicles
    
    def has_emergency_vehicle(self):
        """Check if emergency vehicle exists"""
        return self.emergency_vehicle is not None