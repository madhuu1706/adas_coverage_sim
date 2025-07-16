import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import math

st.set_page_config(page_title="ADAS Sensor Coverage", layout="wide")
st.title("🚗 ADAS Sensor Coverage with Moving Obstacles")

# --- Sensor Settings ---
st.sidebar.header("Sensor Settings")
camera_enabled = st.sidebar.checkbox("Enable 360° Camera", True)
radar_enabled = st.sidebar.checkbox("Enable Radar (360°)", True)
lidar_enabled = st.sidebar.checkbox("Enable LiDAR (360°)", True)

camera_range = st.sidebar.slider("Camera Range (m)", 0, 50, 25)
radar_range = st.sidebar.slider("Radar Range (m)", 0, 50, 15)
lidar_range = st.sidebar.slider("LiDAR Range (m)", 0, 50, 20)

# --- Simulation settings ---
st.sidebar.header("Simulation Settings")
run_simulation = st.sidebar.checkbox("Run Simulation", value=True)
speed = st.sidebar.slider("Obstacle Speed (m/frame)", 0.1, 2.0, 0.5, 0.1)

# --- Constants ---
LANE_WIDTH = 4
LANE_COUNT = 3
ROAD_WIDTH = LANE_WIDTH * LANE_COUNT
ROAD_LEFT = -ROAD_WIDTH / 2
ROAD_RIGHT = ROAD_WIDTH / 2

# --- Ego Vehicle Position (center lane) ---
ego_x = 0
ego_y = 0

# --- Initial Obstacle Positions ---
obstacles = [
    {"x": -LANE_WIDTH, "y": 20, "type": "Vehicle"},  # Left lane
    {"x": LANE_WIDTH, "y": 30, "type": "Vehicle"},   # Right lane
    {"x": 5, "y": 25, "type": "Pedestrian"},          # Footpath
]

placeholder = st.empty()

while run_simulation:
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-5, 35)
    ax.set_aspect('equal')
    ax.set_title("Top-Down ADAS View")

    # --- Draw Road ---
    ax.axvspan(ROAD_LEFT, ROAD_RIGHT, color='#d3d3d3')  # road background
    for i in range(1, LANE_COUNT):
        x = ROAD_LEFT + i * LANE_WIDTH
        ax.plot([x, x], [-5, 35], color='white', linestyle='--', linewidth=2)

    # --- Draw Ego Car ---
    ego_car = plt.Rectangle((ego_x - 1, ego_y - 2), 2, 4, color='black')
    ax.add_patch(ego_car)

    # --- Sensor Coverage ---
    if camera_enabled:
        circle = plt.Circle((ego_x, ego_y), camera_range, color='blue', alpha=0.1, label='360° Camera')
        ax.add_patch(circle)
    if radar_enabled:
        circle = plt.Circle((ego_x, ego_y), radar_range, fill=False, linestyle='--', linewidth=2, edgecolor='red', label='360° Radar')
        ax.add_patch(circle)
    if lidar_enabled:
        circle = plt.Circle((ego_x, ego_y), lidar_range, color='green', alpha=0.2, label='LiDAR (360°)')
        ax.add_patch(circle)

    # --- Obstacle Movement and Detection ---
    detected_summary = []
    for obs in obstacles:
        obs["y"] -= speed

        x = obs["x"]
        y = obs["y"]
        label = obs["type"]

        if label == "Pedestrian":
            patch = plt.Circle((x, y), 0.4, color='orange')
        else:
            patch = plt.Rectangle((x - 1, y - 2), 2, 4, color='purple')
        ax.add_patch(patch)

        distance = math.sqrt((x - ego_x)**2 + (y - ego_y)**2)
        ax.text(x + 0.5, y + 0.5, f"{distance:.1f} m", fontsize=9,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

        detected_by = []
        if camera_enabled and distance <= camera_range:
            detected_by.append("Camera")
        if radar_enabled and distance <= radar_range:
            detected_by.append("Radar")
        if lidar_enabled and distance <= lidar_range:
            detected_by.append("LiDAR")

        detected_summary.append({
            "Obstacle": f"{label} at ({x:.1f}, {y:.1f})",
            "Distance": f"{distance:.1f} m",
            "Detected By": ", ".join(detected_by) if detected_by else "None"
        })

    # --- Legend and Display ---
    ax.legend(loc='upper right')
    placeholder.pyplot(fig)

    st.subheader("📊 Obstacle Detection Summary")
    for d in detected_summary:
        st.write(f"🔹 {d['Obstacle']} → {d['Distance']} → Detected by: {d['Detected By']}")

    time.sleep(1)
