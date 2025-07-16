# ADAS Sensor Coverage Simulator

An interactive simulation built using **Streamlit** and **Matplotlib** to visualize the coverage and detection capabilities of 360° sensors in an autonomous or ADAS-equipped vehicle environment.

![ADAS Simulation Screenshot](demo_image.png)

---

## 🔍 Features

- **360° Camera, Radar, and LiDAR Simulation**
  - Customize sensor ranges and toggle them individually.
- **Real-Time Obstacle Detection**
  - Simulates multiple moving obstacles: vehicles and pedestrians.
  - Detects obstacles using sensor logic and displays distance.
- **Multi-Lane Road Visualization**
  - Central ego vehicle aligned in lane.
  - Dynamic lane markings and realistic road layout.
- **Detection Summary Panel**
  - Real-time breakdown of which sensor detects what obstacle and at what distance.

---

## 🧠 Technologies Used

- [Streamlit](https://streamlit.io/) – for interactive web app.
- [Matplotlib](https://matplotlib.org/) – for 2D visualization.
- [NumPy](https://numpy.org/) – for math and geometry calculations.
- [Python](https://www.python.org/) – base language for simulation logic.

---

## 🚦 Use Cases

- Visualizing sensor blind spots and overlaps.
- Demonstrating how ADAS systems perceive their surroundings.
- Educational tool for teaching sensor fusion concepts.
- Testing sensor performance based on range and angle.

---

## 📦 Installation & Run

```bash
# Clone the repo
git clone https://github.com/yourusername/adas-sensor-simulator.git
cd adas-sensor-simulator

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
