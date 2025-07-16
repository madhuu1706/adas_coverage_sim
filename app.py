import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="ADAS 360° View", layout="wide")
st.title("🚗 ADAS Sensor Coverage Simulator — 360° Camera + LiDAR")

# --- Sidebar ---
st.sidebar.header("Sensor Settings")
camera_360_enabled = st.sidebar.checkbox("Enable 360° Camera View", True)
lidar_enabled = st.sidebar.checkbox("Enable 360° LiDAR", True)
lidar_range = st.sidebar.slider("LiDAR Range (m)", 5, 50, 20)

st.sidebar.subheader("Obstacles")

# Predefined obstacles
predefined_obstacles = [
    {"x": 10, "y": 5, "type": "Pedestrian"},
    {"x": -8, "y": 3, "type": "Vehicle"},
    {"x": 5, "y": -10, "type": "Object"},
    {"x": 15, "y": 15, "type": "Pedestrian"},
    {"x": -12, "y": -7, "type": "Vehicle"},
]

selected_indices = st.sidebar.multiselect(
    "Select Obstacles to Display:",
    options=range(len(predefined_obstacles)),
    format_func=lambda i: f"{predefined_obstacles[i]['type']} at ({predefined_obstacles[i]['x']}, {predefined_obstacles[i]['y']})"
)

obstacle_list = [predefined_obstacles[i] for i in selected_indices]

# --- Plot Setup ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.set_title("Top-Down 360° View")

# Draw the car
car = plt.Rectangle((-1, -2), 2, 4, color='black')
ax.add_patch(car)

# --- Draw 360° Camera View ---
if camera_360_enabled:
    camera_radius = 10
    camera_circle = plt.Circle((0, 0), camera_radius, color='skyblue', alpha=0.2, label='360° Camera View')
    ax.add_patch(camera_circle)

# --- Draw 360° LiDAR View ---
if lidar_enabled:
    lidar_circle = plt.Circle((0, 0), lidar_range, color='green', alpha=0.2, label='LiDAR (360°)')
    ax.add_patch(lidar_circle)

# --- Obstacle Processing ---
detected_summary = []

for obs in obstacle_list:
    x = obs["x"]
    y = obs["y"]
    label = obs["type"]

    # Draw obstacle
    if label == "Pedestrian":
        patch = plt.Circle((x, y), 0.5, color='orange', label='Pedestrian')
    elif label == "Vehicle":
        patch = plt.Rectangle((x - 1, y - 2), 2, 4, color='purple', label='Vehicle')
    else:
        patch = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', label='Object')
    ax.add_patch(patch)

    # Distance
    distance = np.sqrt(x**2 + y**2)
    ax.text(x + 1, y + 1, f"{distance:.1f} m", fontsize=9,
            bbox=dict(facecolor='white', alpha=0.5), color='black')

    detected_by = []
    if camera_360_enabled:
        detected_by.append("360° Camera")
    if lidar_enabled and distance <= lidar_range:
        detected_by.append("LiDAR")

    detected_summary.append({
        "Obstacle": f"{label} at ({x}, {y})",
        "Detected By": ", ".join(detected_by) if detected_by else "None",
        "Distance": f"{distance:.1f} m"
    })

# --- Legend and Plot ---
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

st.pyplot(fig)

if detected_summary:
    st.subheader("📊 Detection Summary")
    for entry in detected_summary:
        st.write(f"🔹 {entry['Obstacle']}")
        st.write(f" 📏 Distance: {entry['Distance']}")
        st.write(f" 🛰️ Detected by: {entry['Detected By']}")
