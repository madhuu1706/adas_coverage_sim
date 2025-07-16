import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ADAS Sensor Coverage", layout="wide")

st.title("🚗 ADAS Sensor Coverage Simulator")

# Sidebar controls
st.sidebar.header("Sensor Settings")

camera_enabled = st.sidebar.checkbox("Enable Camera", True)
radar_enabled = st.sidebar.checkbox("Enable Radar", True)
lidar_enabled = st.sidebar.checkbox("Enable LiDAR", True)

camera_fov = st.sidebar.slider("Camera FOV (°)", 0, 180, 120)
radar_fov = st.sidebar.slider("Radar FOV (°)", 0, 180, 60)
lidar_range = st.sidebar.slider("LiDAR Range (m)", 0, 50, 20)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.set_title("Top-Down View")

# Draw the car at the origin
car = plt.Rectangle((-1, -2), 2, 4, color='black')
ax.add_patch(car)

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

ax.legend()
st.pyplot(fig)
