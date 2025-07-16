import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import time

st.set_page_config(page_title="ADAS Simulator with Road", layout="wide")
st.title("🚗 ADAS Sensor Coverage Simulator with Moving Road")

# --- Sidebar controls ---
st.sidebar.header("Sensor Settings")
camera_enabled = st.sidebar.checkbox("Enable Camera", True)
radar_enabled = st.sidebar.checkbox("Enable Radar", True)
lidar_enabled = st.sidebar.checkbox("Enable LiDAR", True)

camera_fov = st.sidebar.slider("Camera FOV (°)", 0, 180, 120)
radar_fov = st.sidebar.slider("Radar FOV (°)", 0, 180, 60)
lidar_range = st.sidebar.slider("LiDAR Range (m)", 0, 50, 20)

# Obstacle Selection
st.sidebar.subheader("Obstacles (will move toward car)")

initial_obstacles = [
    {"x": 10, "y": 25, "type": "Pedestrian"},
    {"x": -8, "y": 30, "type": "Vehicle"},
    {"x": 5, "y": 40, "type": "Object"},
]

selected_indices = st.sidebar.multiselect(
    "Select Obstacles:",
    options=range(len(initial_obstacles)),
    format_func=lambda i: f"{initial_obstacles[i]['type']} at x={initial_obstacles[i]['x']}"
)

obstacle_list = [initial_obstacles[i].copy() for i in selected_indices]  # Copy so we can move them

# --- Function ---
def is_in_fov(x, y, fov, max_range):
    distance = math.sqrt(x**2 + y**2)
    angle = math.degrees(math.atan2(y, x))
    if distance > max_range:
        return False
    return -fov / 2 <= angle <= fov / 2

def draw_sector(ax, angle_deg, range_m, color, label):
    angle_rad = np.deg2rad(np.linspace(-angle_deg/2, angle_deg/2, 100))
    x = range_m * np.cos(angle_rad)
    y = range_m * np.sin(angle_rad)
    ax.fill_between(x, y, 0, color=color, alpha=0.3, label=label)

# --- Live Animation ---
frame_placeholder = st.empty()
road_scroll = 0

for t in range(100):  # 100 frames of animation
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_aspect('equal')
    ax.set_title("ADAS Top-Down View")

    # --- Draw moving road lines ---
    for i in range(-40, 80, 5):
        y_line = (i + road_scroll) % 80 - 30
        ax.plot([-5, 5], [y_line, y_line], color='gray', linestyle='--', linewidth=0.5)

    road_scroll += 0.5  # Move road

    # --- Draw Car ---
    car = plt.Rectangle((-1, -2), 2, 4, color='black')
    ax.add_patch(car)

    # --- Draw Sensors ---
    if camera_enabled:
        draw_sector(ax, camera_fov, 25, 'blue', 'Camera')
    if radar_enabled:
        draw_sector(ax, radar_fov, 15, 'red', 'Radar')
    if lidar_enabled:
        theta = np.linspace(0, 2 * np.pi, 200)
        x = lidar_range * np.cos(theta)
        y = lidar_range * np.sin(theta)
        ax.plot(x, y, color='green', alpha=0.3, label='LiDAR (360°)')

    # --- Animate Obstacles ---
    detected_summary = []
    for obs in obstacle_list:
        obs['y'] -= 0.5  # Move toward car
        x, y = obs["x"], obs["y"]
        label = obs["type"]

        # Skip if out of bounds
        if y < -30:
            continue

        # Draw obstacle
        if label == "Pedestrian":
            patch = plt.Circle((x, y), 0.5, color='orange', label='Pedestrian')
        elif label == "Vehicle":
            patch = plt.Rectangle((x - 1, y - 2), 2, 4, color='purple', label='Vehicle')
        else:
            patch = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', label='Object')
        ax.add_patch(patch)

        # Distance and Detection
        distance = np.sqrt(x**2 + y**2)
        ax.text(x + 0.8, y + 0.8, f"{distance:.1f}m", fontsize=7)

        detected_by = []
        if camera_enabled and is_in_fov(x, y, camera_fov, 25):
            detected_by.append("Camera")
        if radar_enabled and is_in_fov(x, y, radar_fov, 15):
            detected_by.append("Radar")
        if lidar_enabled and distance <= lidar_range:
            detected_by.append("LiDAR")

        detected_summary.append({
            "Obstacle": f"{label} at ({x:.1f}, {y:.1f})",
            "Detected By": ", ".join(detected_by) if detected_by else "None",
            "Distance": f"{distance:.1f}m"
        })

    # --- Show Legend + Plot ---
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), fontsize=8)

    frame_placeholder.pyplot(fig)
    time.sleep(0.1)  # Control frame rate

# --- After Simulation Ends ---
if detected_summary:
    st.subheader("📊 Final Detection Summary")
    for entry in detected_summary:
        st.write(f"🔹 {entry['Obstacle']}")
        st.write(f" 📏 Distance: {entry['Distance']}")
        st.write(f" 🛰️ Detected by: {entry['Detected By']}")
