# 🏢 Evacuation Simulator

**Web3D Evacuation Simulator with AI**

A professional platform for simulating building evacuations during emergencies (fires, earthquakes, etc.).

---

## 🎯 Project Goals

- Upload a floorplan (image/PDF)
- Automatically extract walls, rooms, and exits
- Generate a 3D model of the building
- Simulate evacuation with realistic agent behavior
- Provide reports (evacuation time, bottlenecks, recommendations)

---

## 🏗️ Architecture

evacuation-simulator/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── config.py
│   ├── data/
│   ├── simulation/
│   ├── visualization/
│   └── utils/
├── data/
│   ├── floorplans/
│   └── outputs/
├── tests/
└── docs/

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Image Processing | OpenCV |
| 3D Visualization | Plotly |
| Data Handling | Pandas, NumPy |
| Deployment | Streamlit Cloud |

---

## 🚀 Getting Started

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/evacuation-simulator.git
cd evacuation-simulator

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the app
streamlit run app.py

---

## 📅 Roadmap

- [x] Week 1: Project structure + data models
- [ ] Week 2-3: Floorplan parsing (OpenCV)
- [ ] Week 4-5: 3D visualization (Plotly)
- [ ] Week 6-8: Simulation engine
- [ ] Week 9: Reports and recommendations

---

## 📄 License

MIT License
