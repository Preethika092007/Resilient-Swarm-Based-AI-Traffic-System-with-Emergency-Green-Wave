import streamlit as st
import pandas as pd
import time
import random
import signal_optimizer
import config

# Set page configuration
st.set_page_config(
    page_title="AI Traffic Optimization",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Theme CSS with Precision Alignment
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #06061a 0%, #1a1a3a 50%, #06061a 100%);
        color: #ffffff;
    }
    
    /* Global alignment for containers */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Header centering and spacing */
    .title-container {
        text-align: center;
        padding: 3rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Container for standardized cards */
    .main-section {
        background: rgba(255, 255, 255, 0.02);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
    }
    
    .signal-card {
        padding: 20px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 200px;
        margin: 10px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .signal-card:hover {
        background: rgba(255, 255, 255, 0.07);
        transform: translateY(-5px);
        border-color: rgba(0, 210, 255, 0.3);
    }
    
    .signal-indicator {
        height: 65px;
        width: 65px;
        border-radius: 50%;
        margin: 15px 0;
        border: 4px solid rgba(255,255,255,0.05);
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    .signal-green {
        background: radial-gradient(circle at 30% 30%, #00ff87, #00a859);
        box-shadow: 0 0 30px rgba(0, 255, 135, 0.6), 0 0 60px rgba(0, 255, 135, 0.3);
    }
    
    .signal-red {
        background: radial-gradient(circle at 30% 30%, #ff416c, #a8002d);
        box-shadow: 0 0 15px rgba(255, 65, 108, 0.3);
        opacity: 0.35;
    }
    
    .priority-highlight {
        background: linear-gradient(90deg, rgba(0, 210, 255, 0.15), rgba(0, 210, 255, 0.02));
        padding: 18px;
        border-left: 4px solid #00d2ff;
        border-radius: 12px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .status-badge {
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .badge-active { background: #00ff87; color: #000; }
    .badge-standby { background: rgba(255, 255, 255, 0.1); color: #fff; }

    /* Button alignment */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        padding: 0.75rem;
        font-size: 1rem;
        background: linear-gradient(45deg, #3a7bd5, #00d2ff);
        border: none;
        box-shadow: 0 4px 15px rgba(58, 123, 213, 0.3);
    }
    
    /* Sidebar Input Alignment */
    .stSlider > div {
        padding-bottom: 1rem;
    }
    
    /* Metrics block alignment */
    .metric-container {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state (same as before)
if 'simulation_active' not in st.session_state:
    st.session_state.simulation_active = False

if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = {
        "Lane A": {"vehicle_count": 15, "waiting_time": 20, "emergency": False},
        "Lane B": {"vehicle_count": 5, "waiting_time": 10, "emergency": False},
        "Lane C": {"vehicle_count": 8, "waiting_time": 12, "emergency": False},
        "Lane D": {"vehicle_count": 3, "waiting_time": 5, "emergency": False}
    }

# Simulation Logic Update at Top (keep it for synchronicity)
if st.session_state.simulation_active:
    for lane in ["Lane A", "Lane B", "Lane C", "Lane D"]:
        st.session_state.traffic_data[lane]["vehicle_count"] = random.randint(1, 45)
        st.session_state.traffic_data[lane]["waiting_time"] = random.randint(1, 80)

# 1. Page Header (Styled & Centered)
st.markdown("""
    <div class="title-container">
        <h1 style='margin:0; font-size: 3rem; background: linear-gradient(to right, #00d2ff, #92fe9d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🚦 AI TRAFFIC COMMAND</h1>
        <p style='margin-top:0.5rem; font-size: 1.2rem; opacity: 0.8; letter-spacing: 2px;'>RESILIENT SWARM-BASED OPTIMIZATION ENGINE</p>
    </div>
""", unsafe_allow_html=True)

# 2. Traffic Input Panel (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛰 INTERFACE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    lanes = ["Lane A", "Lane B", "Lane C", "Lane D"]
    
    for lane in lanes:
        with st.expander(f"📍 {lane} Control", expanded=True):
            v_val = st.session_state.traffic_data[lane]["vehicle_count"]
            w_val = st.session_state.traffic_data[lane]["waiting_time"]
            
            st.session_state.traffic_data[lane]["vehicle_count"] = st.slider(
                f"Vehicles", 0, 60, value=v_val, key=f"v_{lane}_sc"
            )
            st.session_state.traffic_data[lane]["waiting_time"] = st.slider(
                f"Wait Time (ms)", 0, 120, value=w_val, key=f"w_{lane}_sc"
            )
    
    st.markdown("---")
    st.markdown("### 🚑 EMERGENCY MODE")
    emergency_b = st.toggle("Enable Lane B Priority", value=st.session_state.traffic_data["Lane B"]["emergency"])
    st.session_state.traffic_data["Lane B"]["emergency"] = emergency_b

    st.markdown("---")
    sim_label = "⏹ STOP SIMULATION" if st.session_state.simulation_active else "▶ START LIVE FEED"
    if st.button(sim_label, type="primary" if not st.session_state.simulation_active else "secondary"):
        st.session_state.simulation_active = not st.session_state.simulation_active
        st.rerun()

# Logic to get optimization
def get_optimization_results():
    ranked_lanes = signal_optimizer.rank_lanes(st.session_state.traffic_data)
    results = []
    for lane_id, score in ranked_lanes:
        green_time = signal_optimizer.calculate_green_time(score)
        results.append({
            "Lane": lane_id,
            "Vehicles": st.session_state.traffic_data[lane_id]["vehicle_count"],
            "Waiting Time": st.session_state.traffic_data[lane_id]["waiting_time"],
            "Priority": score,
            "Green Time (s)": green_time
        })
    return results

# Process data
results = get_optimization_results()
top_lane = results[0]
active_lane = top_lane["Lane"]

# Main Layout
col_left, col_right = st.columns([3, 1], gap="large")

with col_left:
    # Top Section: Junction Visualizer (Moved to top for better impact)
    st.markdown("### 🗺️ Junction Visualizer")
    sig_cols = st.columns(4, gap="medium")
    
    for i, lane in enumerate(lanes):
        with sig_cols[i]:
            is_active = (lane == active_lane)
            indicator_class = "signal-green" if is_active else "signal-red"
            status_text = "PROCEED" if is_active else "WAITING"
            badge_class = "badge-active" if is_active else "badge-standby"
            st.markdown(f"""
                <div class='signal-card'>
                    <div style='font-size: 1.2rem; font-weight: 800;'>{lane}</div>
                    <div class='signal-indicator {indicator_class}'></div>
                    <div class='status-badge {badge_class}'>{status_text}</div>
                </div>
            """, unsafe_allow_html=True)

    # Middle Section: Sequence
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛣️ Optimized Signal Sequence")
    for i, res in enumerate(results):
        is_first = (i == 0)
        label = "NOW ACTIVE" if is_first else f"QUEUED #{i+1}"
        opacity = 1.0 if is_first else 0.6
        st.markdown(f"""
            <div class='priority-highlight' style='opacity: {opacity};'>
                <div>
                    <span style='font-weight: 800; font-size: 1.1rem;'>{res['Lane']}</span> 
                    &nbsp;&nbsp;&nbsp; 
                    <small style='opacity: 0.7;'>Priority Score: {int(res['Priority']) if res['Priority'] < 1000 else '1000+'}</small>
                </div>
                <div style='text-align: right;'>
                    <span style='font-weight: 600; color: #00d2ff;'>{res['Green Time (s)']}s Allocated</span>
                    &nbsp;&nbsp;
                    <span style='background: rgba(255,255,255,0.1); padding: 4px 10px; border-radius: 5px; font-size: 0.8rem;'>{label}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

with col_right:
    # Metrics and Simulation Info
    st.markdown("### 📊 Status Monitor")
    
    with st.container(border=False):
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Primary Lane", top_lane["Lane"])
        st.metric("Duration", f"{top_lane['Green Time (s)']}s")
        st.metric("Total Load", sum(d['vehicle_count'] for d in st.session_state.traffic_data.values()))
        
        st.markdown("<br><b>Resource Usage</b>", unsafe_allow_html=True)
        progress = min(top_lane['Green Time (s)'] / config.MAX_GREEN_TIME, 1.0)
        st.progress(progress)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.simulation_active:
        st.markdown("<div class='metric-container' style='border-color: #ff9a9e;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #ff9a9e; font-weight: 800; margin-bottom: 0;'>LIVE SYNC READY</p>", unsafe_allow_html=True)
        countdown_placeholder = st.empty()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📝 Optimization Table")
    df = pd.DataFrame(results)
    # Simplify for the small column
    df_small = df[["Lane", "Green Time (s)", "Vehicles"]]
    st.dataframe(df_small, hide_index=True, use_container_width=True)

# Simulation Loop at the bottom
if st.session_state.simulation_active:
    for i in range(5, 0, -1):
        countdown_placeholder.markdown(f"<h1 style='text-align: center; color: #ff9a9e; margin: 0;'>{i}s</h1>", unsafe_allow_html=True)
        time.sleep(1)
    st.rerun()

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; opacity: 0.5;'>AI TRAFFIC COMMAND CENTER | SWARM INTELLIGENCE | 2026</div>", unsafe_allow_html=True)
