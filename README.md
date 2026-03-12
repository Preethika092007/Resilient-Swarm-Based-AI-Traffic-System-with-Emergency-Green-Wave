# Urban Swarm - AI Traffic Management System

## 🚦 Project Overview

Urban Swarm is an AI-powered traffic management system that integrates multiple modules to create an intelligent traffic control solution.

## 📁 Project Structure

```
urban-swarm/
│
├── backend/
│   ├── detection/          # Vehicle detection module
│   ├── analytics/          # Traffic analysis module
│   ├── signal_control/     # Signal optimization module
│   ├── emergency/          # Emergency vehicle detection
│   ├── green_wave/         # Green corridor activation
│   ├── main.py            # ✨ Main integration pipeline
│   └── system_state.json  # Real-time system state
│
├── frontend/
│   └── dashboard.py       # Streamlit dashboard
│
└── datasets/              # Training datasets
```

## 🎯 Features

1. **Vehicle Detection** - Real-time vehicle detection using YOLOv8
2. **Traffic Analytics** - Lane-wise traffic analysis and density calculation
3. **Signal Optimization** - Dynamic signal timing based on traffic load
4. **Emergency Detection** - Ambulance and police vehicle detection
5. **Green Wave** - Automatic green corridor for emergency vehicles
6. **Live Dashboard** - Real-time visualization using Streamlit

## 🚀 Quick Start

### Prerequisites

```bash
pip install ultralytics opencv-python streamlit pandas
```

### Running the System

#### Option 1: Backend Only (with video display)

```bash
cd backend
python main.py
```

This will:
- Start webcam capture
- Run all detection and analysis modules
- Display annotated video feed
- Save system state to `system_state.json`
- Press 'q' to quit

#### Option 2: Dashboard (recommended for presentation)

**Step 1:** Start the backend in one terminal

```bash
cd backend
python main.py
```

**Step 2:** Start the dashboard in another terminal

```bash
streamlit run frontend/dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 System Pipeline

```
Video Input (Webcam/File)
    ↓
Vehicle Detection (YOLO)
    ↓
Traffic Analysis (Lane Distribution)
    ↓
Signal Optimization (Timing Calculation)
    ↓
Emergency Detection (Ambulance/Police)
    ↓
Green Wave Activation (If Emergency)
    ↓
Dashboard Visualization
```

## 🎛️ Dashboard Features

- **Real-time Metrics**: Vehicle count, density, priority lane
- **Emergency Alerts**: Visual alerts for emergency vehicles
- **Green Wave Status**: Active corridor visualization
- **Lane Distribution**: Bar chart showing vehicles per lane
- **Signal Timings**: Optimized green signal durations
- **Auto-refresh**: Configurable refresh rate

## 🔧 Configuration

### Video Source

Edit `backend/main.py`:

```python
# Use webcam
run_traffic_system(video_source=0)

# Use video file
run_traffic_system(video_source='path/to/video.mp4')
```

### Number of Lanes

Edit `backend/main.py`:

```python
self.traffic_analyzer = TrafficAnalyzer(num_lanes=4)  # Change to 2, 3, 4, etc.
```

### Signal Timings

Edit `backend/main.py` in `SignalOptimizer` class:

```python
self.base_time = 10        # Base green time (seconds)
self.max_time = 60         # Maximum green time
self.emergency_time = 90   # Emergency vehicle green time
```

## 📈 System Output

The system generates a JSON file (`system_state.json`) with:

```json
{
  "vehicle_count": 18,
  "traffic_density": "High",
  "lane_distribution": {
    "Lane A": 5,
    "Lane B": 4,
    "Lane C": 6,
    "Lane D": 3
  },
  "signal_timings": {
    "Lane A": {"green_time": 35, "is_priority": false},
    "Lane B": {"green_time": 28, "is_priority": false},
    "Lane C": {"green_time": 42, "is_priority": true},
    "Lane D": {"green_time": 22, "is_priority": false}
  },
  "priority_lane": "Lane C",
  "emergency_detected": true,
  "emergency_type": "ambulance",
  "green_wave_active": true,
  "green_wave_route": ["Lane C", "Intersection-1", "Intersection-2"]
}
```

## 🎥 Demo Tips

1. **Use pre-recorded traffic video** for consistent demo results
2. **Test emergency detection** by showing ambulance/police images to webcam
3. **Dashboard auto-refresh** - Enable for live updates during presentation
4. **Multiple lanes** - Position camera to capture multiple traffic lanes

## 🐛 Troubleshooting

### Webcam not working
- Check if another application is using the webcam
- Try `video_source=1` for external webcam

### Emergency model not found
- The system will use pretrained YOLO as fallback
- Train emergency model first: `cd backend/emergency && python train_emergency_model.py`

### Dashboard shows "No data"
- Ensure `backend/main.py` is running first
- Check if `backend/system_state.json` exists

## 👥 Team Members

- **Member 1**: Vehicle Detection (YOLO)
- **Member 2**: Traffic Analytics
- **Member 3**: Signal Optimization
- **Member 4**: Emergency Detection
- **Member 5**: Green Wave System
- **Member 6**: Dashboard Visualization

## 📝 License

Hackathon Project - Urban Swarm Team

## 🏆 Hackathon Presentation

For best presentation results:
1. Run dashboard on projector/screen
2. Use pre-recorded traffic video with emergency vehicles
3. Show real-time metrics updating
4. Demonstrate green wave activation
5. Explain the AI pipeline and integration

---

**Built with ❤️ for Smart City Solutions**
