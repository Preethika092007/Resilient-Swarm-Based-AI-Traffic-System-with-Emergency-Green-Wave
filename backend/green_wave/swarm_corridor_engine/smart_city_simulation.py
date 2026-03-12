import networkx as nx
import matplotlib.pyplot as plt
import random

CITY_SIZE = 4
CONGESTION_WEIGHT = 0.6

class IntersectionAgent:
    def __init__(self, node_id):
        self.node_id = node_id
        self.vehicle_density = random.randint(2, 8)
        self.queue_length = random.randint(0, 5)
        self.waiting_time = random.uniform(0, 3)
        self.signal_state = "red"
        
    def update_traffic(self):
        self.vehicle_density = max(0, self.vehicle_density + random.uniform(-1, 1.5))
        self.queue_length = max(0, self.queue_length + random.randint(-1, 2))
        self.waiting_time = max(0, self.waiting_time + random.uniform(-0.5, 0.8))
        
    def priority_score(self):
        return (self.vehicle_density * 0.5 + self.queue_length * 0.3 + self.waiting_time * 0.2)

class Vehicle:
    def __init__(self, position):
        self.position = position
        
    def move(self, G):
        neighbors = list(G.neighbors(self.position))
        self.position = random.choice(neighbors) if neighbors else self.position

class SwarmController:
    def __init__(self, agents):
        self.agents = agents
        
    def propagate_emergency(self, route):
        print("\n🧠 Swarm Communication:")
        for i in range(len(route)-1):
            print(f"Signal {route[i]} → notifying Signal {route[i+1]} to prepare green corridor")
            self.agents[route[i]].signal_state = "green"

class TrafficEnvironment:
    def __init__(self, G):
        self.G = G
        self.edge_congestion = {}
        for u, v in G.edges():
            cong = random.randint(1, 10)
            self.edge_congestion[(u,v)] = cong
            self.edge_congestion[(v,u)] = cong
            
    def update_congestion(self, vehicles):
        for u, v in self.G.edges():
            self.edge_congestion[(u,v)] = max(1, self.edge_congestion[(u,v)] + random.uniform(-0.5, 0.5))
            self.edge_congestion[(v,u)] = self.edge_congestion[(u,v)]
        
        for vehicle in vehicles:
            for neighbor in self.G.neighbors(vehicle.position):
                self.edge_congestion[(vehicle.position, neighbor)] += 0.3
                
    def get_node_congestion(self, node):
        total = sum(self.edge_congestion[(node, n)] for n in self.G.neighbors(node))
        return round(total / max(1, self.G.degree(node)))

class EmergencyController:
    def __init__(self, G, environment):
        self.G = G
        self.environment = environment
        
    def compute_route(self, start, end):
        def cost_func(u, v, d):
            base = d.get('weight', 1)
            cong = self.environment.edge_congestion.get((u, v), 1)
            return base + CONGESTION_WEIGHT * cong
        
        return nx.astar_path(self.G, start, end, heuristic=None, weight=cost_func)

def build_city():
    G = nx.grid_2d_graph(CITY_SIZE, CITY_SIZE)
    G = nx.convert_node_labels_to_integers(G)
    
    for u, v in G.edges():
        G[u][v]["weight"] = 1
    
    pos = {}
    spacing = 5
    for node in G.nodes():
        row = node // CITY_SIZE
        col = node % CITY_SIZE
        pos[node] = (col * spacing, -row * spacing)
    
    return G, pos

def draw_city(G, pos, agents, environment, route, vehicles, ambulance_pos, step):
    plt.clf()
    
    nx.draw_networkx_edges(G, pos, width=18, edge_color="#2f2f2f")
    
    colors = ["green" if agents[n].signal_state == "green" and n in route[:step+2] else "red" for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2400)
    nx.draw_networkx_labels(G, pos, font_size=11)
    
    for node, (x, y) in pos.items():
        plt.text(x, y+0.9, "🚦", fontsize=20, ha="center")
        cong = environment.get_node_congestion(node)
        plt.text(x, y-1.0, f"{cong}", fontsize=10, ha="center", bbox=dict(facecolor="white", alpha=0.9))
    
    corridor = list(zip(route[:step+2], route[1:step+3]))
    nx.draw_networkx_edges(G, pos, edgelist=corridor, edge_color="lime", width=22)
    
    for vehicle in vehicles:
        plt.text(pos[vehicle.position][0], pos[vehicle.position][1], "🚗", fontsize=10, ha="center")
    
    plt.scatter(pos[ambulance_pos][0], pos[ambulance_pos][1], s=3500, c="red", edgecolors="black", zorder=10)
    plt.text(pos[ambulance_pos][0], pos[ambulance_pos][1], "🚑", fontsize=22, ha="center", va="center")
    
    plt.title("AI Smart City Traffic System — Emergency Green Wave")
    plt.axis("off")
    plt.pause(0.3)

def run_simulation():
    G, pos = build_city()
    
    agents = {node: IntersectionAgent(node) for node in G.nodes()}
    environment = TrafficEnvironment(G)
    swarm = SwarmController(agents)
    emergency = EmergencyController(G, environment)
    
    vehicles = [Vehicle(random.choice(list(G.nodes()))) for _ in range(12)]
    
    start, end = 0, 15
    
    print("\nTraffic Conditions:\n")
    for (u, v), t in list(environment.edge_congestion.items())[:20]:
        if u < v:
            print(f"{u}->{v} congestion: {int(t)}")
    
    route = emergency.compute_route(start, end)
    print("\nOptimal Emergency Route:", route)
    print("\n🚑 Emergency Corridor Activated")
    
    swarm.propagate_emergency(route)
    
    plt.figure(figsize=(10, 8))
    
    for step, node in enumerate(route):
        for agent in agents.values():
            agent.update_traffic()
        
        for vehicle in vehicles:
            vehicle.move(G)
        
        environment.update_congestion(vehicles)
        
        if step < len(route) - 1:
            agents[route[step+1]].signal_state = "green"
        
        draw_city(G, pos, agents, environment, route, vehicles, node, step)
    
    plt.show()

if __name__ == "__main__":
    run_simulation()