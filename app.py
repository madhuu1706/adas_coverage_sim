import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="ADAS Road Layout Simulator", layout="wide")
st.title("🚗 ADAS Sensor Coverage on 2-Lane Road")

# === Sidebar Controls ===
st.sidebar.header("Sensors")
camera_360_enabled = st.sidebar.checkbox("Enable 360° Camera", True)
lidar_enabled = st.sidebar.checkbox("Enable LiDAR (360°)", True)
lidar_range = st.sidebar.slider("LiDAR Range (m)", 5, 50, 20)

st.sidebar.subheader("Select Obstacles")

# Define obstacles on road & footpath
predefined_obstacles = [
    {"x": -4, "y": 8, "type": "Vehicle"},     # left lane
    {"x": 4, "y": 14, "type": "Vehicle"},      # right lane
    {"x": 4, "y": -13, "type": "Vehicle"},     # right lane
    {"x": -12, "y": 11, "type": "Pedestrian"}, # left footpath
    {"x": 12, "y": 11, "type": "Pedestrian"},  # right footpath
    {"x": 10, "y": 21, "type": "Object"},      # far object
]

# Let user pick what to show
selected_indices = st.sidebar.multiselect(
    "Show Obstacles:",
    options=range(len(predefined_obstacles)),
    format_func=lambda i: f"{predefined_obstacles[i]['type']} at ({predefined_obstacles[i]['x']}, {predefined_obstacles[i]['y']})"
)

obstacle_list = [predefined_obstacles[i] for i in selected_indices]

# === Plot Setup ===
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-20, 20)
ax.set_ylim(-25, 25)
ax.set_aspect('equal')
ax.set_title("Top-Down ADAS Road View")

# === Road Background ===
# Road width = 16m (two 4m lanes + margins), centered at x=0
road = plt.Rectangle((-8, -25), 16, 50, color='lightgray', zorder=0)
ax.add_patch(road)

# Footpaths (green zones on sides)
footpath_left = plt.Rectangle((-20, -25), 12, 50, color='#ddf4d2', zorder=0)
footpath_right = plt.Rectangle((8, -25), 12, 50, color='#ddf4d2', zorder=0)
ax.add_patch(footpath_left)
ax.add_patch(footpath_right)

# Lane markings (dashed white lines)
for x in [-4, 0, 4]:
    ax.plot([x, x], [-25, 25], linestyle='--', color='white', linewidth=2, zorder=1)

# === Car at center ===
car = plt.Rectangle((-1, -2), 2, 4, color='black', zorder=5)
ax.add_patch(car)

# === 360° Camera View ===
if camera_360_enabled:
    camera_circle = plt.Circle((0, 0), 10, color='skyblue', alpha=0.2, label='360° Camera', zorder=2)
    ax.add_patch(camera_circle)

# === LiDAR View ===
if lidar_enabled:
    lidar_circle = plt.Circle((0, 0), lidar_range, color='green', alpha=0.2, label='LiDAR (360°)', zorder=2)
    ax.add_patch(lidar_circle)

# === Detection Logic ===
detected_summary = []

for obs in obstacle_list:
    x = obs["x"]
    y = obs["y"]
    label = obs["type"]

    # Draw obstacle
    if label == "Pedestrian":
        patch = plt.Circle((x, y), 0.5, color='orange', label='Pedestrian', zorder=4)
    elif label == "Vehicle":
        patch = plt.Rectangle((x - 1, y - 2), 2, 4, color='purple', label='Vehicle', zorder=4)
    else:
        patch = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', label='Object', zorder=4)
    ax.add_patch(patch)

    # Distance
    distance = np.sqrt(x**2 + y**2)
    ax.text(x + 0.5, y + 0.5, f"{distance:.1f} m", fontsize=8,
            bbox=dict(facecolor='white', alpha=0.6), color='black', zorder=6)

    # Detection
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

# === Legend & Output ===
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # remove duplicates
ax.legend(by_label.values(), by_label.keys(), loc='lower right')

st.pyplot(fig)

if detected_summary:
    st.subheader("📊 Detection Summary")
    for entry in detected_summary:
        st.write(f"🔹 **{entry['Obstacle']}**")
        st.write(f" 📏 Distance: `{entry['Distance']}`")
        st.write(f" 🛰️ Detected by: `{entry['Detected By']}`")
