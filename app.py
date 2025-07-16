import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="ADAS Sensor Coverage", layout="wide")
st.title("🚗 ADAS Sensor Coverage Simulator")

# --- Sidebar controls ---
st.sidebar.header("Sensor Settings")
camera_enabled = st.sidebar.checkbox("Enable Camera", True)
radar_enabled = st.sidebar.checkbox("Enable Radar", True)
lidar_enabled = st.sidebar.checkbox("Enable LiDAR", True)

camera_fov = st.sidebar.slider("Camera FOV (°)", 0, 180, 120)
radar_fov = st.sidebar.slider("Radar FOV (°)", 0, 180, 60)
lidar_range = st.sidebar.slider("LiDAR Range (m)", 0, 50, 20)

st.sidebar.subheader("Multiple Obstacles")

# Example predefined obstacles to pick from
predefined_obstacles = [
    {"x": 10, "y": 5, "type": "Pedestrian"},
    {"x": -8, "y": 3, "type": "Vehicle"},
    {"x": 5, "y": -10, "type": "Object"},
    {"x": 15, "y": 15, "type": "Pedestrian"},
    {"x": -12, "y": -7, "type": "Vehicle"},
]

# Allow user to pick multiple from a list
selected_indices = st.sidebar.multiselect(
    "Select Obstacles to Display:",
    options=range(len(predefined_obstacles)),
    format_func=lambda i: f"{predefined_obstacles[i]['type']} at ({predefined_obstacles[i]['x']}, {predefined_obstacles[i]['y']})"
)

obstacle_list = [predefined_obstacles[i] for i in selected_indices]


# --- Plot setup ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.set_title("Top-Down View")

# Draw the car at the origin
car = plt.Rectangle((-1, -2), 2, 4, color='black')
ax.add_patch(car)

# --- Sensor drawing ---
def draw_sector(ax, angle_deg, range_m, color, label):
    angle_rad = np.deg2rad(np.linspace(-angle_deg/2, angle_deg/2, 100))
    x = range_m * np.cos(angle_rad)
    y = range_m * np.sin(angle_rad)
    ax.fill_between(x, y, 0, color=color, alpha=0.3, label=label)

if camera_enabled:
    draw_sector(ax, camera_fov, 25, 'blue', 'Camera')

if radar_enabled:
    draw_sector(ax, radar_fov, 15, 'red', 'Radar')

if lidar_enabled:
    theta = np.linspace(0, 2 * np.pi, 200)
    x = lidar_range * np.cos(theta)
    y = lidar_range * np.sin(theta)
    ax.plot(x, y, color='green', alpha=0.3, label='LiDAR (360°)')

# --- Obstacle Drawing + Distance ---
if add_obstacle:
    if obstacle_type == "Pedestrian":
        obstacle = plt.Circle((obstacle_x, obstacle_y), 0.5, color='orange', label='Pedestrian')
    elif obstacle_type == "Vehicle":
        obstacle = plt.Rectangle((obstacle_x - 1, obstacle_y - 2), 2, 4, color='purple', label='Vehicle')
    else:
        obstacle = plt.Rectangle((obstacle_x - 0.5, obstacle_y - 0.5), 1, 1, color='gray', label='Object')

    ax.add_patch(obstacle)

    # Calculate and show distance
    distance_to_obstacle = np.sqrt(obstacle_x**2 + obstacle_y**2)
    ax.text(obstacle_x + 1, obstacle_y + 1, 
            f"{distance_to_obstacle:.2f} m", 
            fontsize=10, color='black', bbox=dict(facecolor='white', alpha=0.5))

# --- Detection Logic ---
def is_in_fov(x, y, fov, max_range):
    distance = math.sqrt(x**2 + y**2)
    angle = math.degrees(math.atan2(y, x))
    if distance > max_range:
        return False
    return -fov / 2 <= angle <= fov / 2

detected_by = []

if add_obstacle:
    if camera_enabled and is_in_fov(obstacle_x, obstacle_y, camera_fov, 25):
        detected_by.append("Camera")
    if radar_enabled and is_in_fov(obstacle_x, obstacle_y, radar_fov, 15):
        detected_by.append("Radar")
    if lidar_enabled and distance_to_obstacle <= lidar_range:
        detected_by.append("LiDAR")

# --- Plot and UI Output ---
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

st.pyplot(fig)

if add_obstacle:
    st.info(f"📏 Distance from Car to Obstacle: `{distance_to_obstacle:.2f} meters`")

    if detected_by:
        st.success(f"🚨 Obstacle Detected by: {', '.join(detected_by)}")
    else:
        st.warning("⚠️ Obstacle NOT detected by any active sensor.")
