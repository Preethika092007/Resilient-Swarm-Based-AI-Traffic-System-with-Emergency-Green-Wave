# Resilient Swarm-Based AI Traffic System with Emergency Green Wave

A Python-based smart-city traffic simulation prototype that demonstrates decentralized AI traffic signal coordination using swarm intelligence to create predictive green corridors for emergency vehicles.

## 🚨 Project Overview

This hackathon project simulates an intelligent traffic management system where autonomous traffic signal agents cooperate to:
- Dynamically optimize traffic flow using swarm intelligence
- Detect and route emergency vehicles (ambulances)
- Create predictive green wave corridors
- Adapt to real-time congestion changes

## ✨ Key Features

- **🧠 Swarm Intelligence**: Decentralized traffic signal coordination
- **🚦 Autonomous Agents**: Each intersection operates independently
- **🚑 Emergency Routing**: AI-powered A* pathfinding for ambulances
- **🌊 Green Wave System**: Sequential signal activation ahead of emergency vehicles
- **📊 Real-time Visualization**: Animated city traffic with NetworkX and Matplotlib
- **🚗 Dynamic Traffic**: Moving vehicles with realistic congestion simulation

## 🏗️ Architecture

```
project_root/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── README.md                 # Documentation
└── smart_city/               # Core package
    ├── __init__.py
    ├── city.py               # 4x4 grid network infrastructure
    ├── traffic_agents.py     # Autonomous signal agents
    ├── vehicle_system.py     # Vehicle spawning and movement
    ├── routing_engine.py     # A* emergency routing
    ├── swarm_controller.py   # Decentralized coordination
    └── simulator.py          # Visualization and simulation loop
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Resilient-Swarm-Based-AI-Traffic-System-with-Emergency-Green-Wave

# Install dependencies
pip install -r requirements.txt
```

### Run Simulation

```bash
python main.py
```

## 🎯 How It Works

### 1. City Network (4x4 Grid)
```
0  1  2  3
4  5  6  7
8  9  10 11
12 13 14 15
```

### 2. Traffic Signal Agents
Each intersection agent maintains:
- `vehicle_density`: Number of vehicles in the area
- `queue_length`: Waiting vehicles at the signal
- `waiting_time`: Average wait time
- `signal_state`: Current signal color (red/green)

**Priority Score Formula:**
```
priority = (vehicle_density × 0.5) + (queue_length × 0.3) + (waiting_time × 0.2)
```

### 3. Emergency Routing
Route cost calculation:
```
cost = distance + (congestion × 0.6)
```

Uses NetworkX A* algorithm for optimal pathfinding.

### 4. Swarm Communication
Signals coordinate through decentralized messages:
```
Signal 0 → notifying Signal 4 to prepare green corridor
Signal 4 → notifying Signal 8 to prepare green corridor
```

### 5. Green Wave System
Sequential signal activation creates a moving green corridor for emergency vehicles.

## 📊 Visualization Elements

- **🚦** Traffic signals with red/green states
- **🚗** Regular vehicles with density indicators
- **🚑** Emergency ambulance with glow effect
- **🟢** Green emergency corridor highlighting
- **📈** Real-time traffic statistics

## 🔧 Technical Implementation

### Core Technologies
- **Python 3.7+**
- **NetworkX**: Graph algorithms and network analysis
- **Matplotlib**: Real-time visualization and animation

### Key Algorithms
- **A* Search**: Emergency vehicle routing
- **Swarm Intelligence**: Decentralized signal coordination
- **Priority Scoring**: Traffic flow optimization

### Simulation Loop
1. Update traffic state
2. Move vehicles
3. Update signal agents
4. Simulate swarm communication
5. Update visualization
6. Move ambulance

## 🎮 Demo Scenario

The simulation demonstrates:
1. **Normal Traffic**: Vehicles moving through 4x4 grid
2. **Emergency Alert**: Ambulance spawns at intersection 0
3. **Route Calculation**: AI computes optimal path to intersection 15
4. **Green Wave**: Signals coordinate to create corridor
5. **Success**: Ambulance reaches hospital efficiently

## 📈 Performance Metrics

The system tracks:
- **Swarm Coordination**: Communication messages and signal states
- **Traffic Flow**: Vehicle density and congestion levels
- **Emergency Response**: Route efficiency and delivery time
- **Network Utilization**: Intersection and road usage

## 🚧 Future Enhancements

- **Multi-lane Roads**: More realistic road modeling
- **Machine Learning**: Predictive traffic optimization
- **Multiple Emergencies**: Concurrent emergency vehicle handling
- **Real-world Integration**: GPS and mapping system integration
- **IoT Sensors**: Real traffic data integration

## 🏆 Hackathon Highlights

This project demonstrates:
- **Clean Architecture**: Modular, maintainable code structure
- **AI Integration**: Swarm intelligence and pathfinding algorithms
- **Real-time Visualization**: Interactive traffic simulation
- **Practical Application**: Smart city traffic management solution

## 📝 License

MIT License - Built for hackathon demonstration purposes.

## 👥 Team

Smart City AI Traffic Team

---

**🚨 Ready to revolutionize urban traffic management with AI! 🚨**