# iSARTHI 🚗
### AI-Powered Intelligent Road & Vehicle Safety System

**Transforming vehicles into intelligent, connected road-monitoring units.**

iSARTHI is an AI-powered road intelligence and vehicle safety platform designed to detect road hazards, monitor driving conditions, and enable real-time hazard communication. By combining Computer Vision, Edge AI, IoT sensors, GPS/GIS, and Vehicle-to-Vehicle (V2V) communication, iSARTHI aims to build a smarter, safer, and more connected road ecosystem.

---

## 🌐 Vision

To create a distributed road intelligence network where vehicles continuously collect road-condition data, share critical hazard information, and help authorities make data-driven infrastructure decisions.

## 🚀 Core Capabilities

- **AI-Powered Road Detection:** YOLOv8-based detection of potholes and road hazards.
- **Multi-Sensor Integration:** Integrates LiDAR, MPU6050 IMUs, GPS, and other sensors for environmental and motion data.
- **Real-Time Hazard Alerts:** Transmits structured hazard events to connected devices.
- **V2V Communication:** Enables vehicle-to-vehicle hazard messaging through Wi-Fi and UDP in the current prototype.
- **Live Monitoring Dashboard:** Designed to visualize sensor telemetry, hazard events, and location-based information.
- **Edge AI Architecture:** Supports local inference and processing to reduce dependence on continuous cloud connectivity.
- **Driver Safety Monitoring:** Designed for future integration of driver monitoring and alcohol-sensor data.

## 🏗️ System Architecture

```text
Vehicle A — Raspberry Pi
        │
        ├── Camera + YOLOv8
        ├── LiDAR + MPU6050
        ├── GPS / Sensor Integration
        │
        ▼
   Hazard Event Pipeline
        │
        ├── Dashboard Backend
        │
        └── Wi-Fi / UDP
                 │
                 ▼
          Vehicle B — ESP32
                 │
                 └── LED / Buzzer Alert
```

## 📂 Repository Structure

```text
iSARTHI/
├── Government Dashboard/
│   └── Dashboard application
├── Sensor Integration/
│   ├── unified_sensors.py
│   └── README.md
├── Model Integration/
│   ├── test.py
│   └── README.md
└── README.md
```

*The repository structure may evolve as development progresses.*

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| AI & Computer Vision | Python, Ultralytics YOLOv8, OpenCV |
| Edge Computing | Raspberry Pi |
| Embedded Systems | ESP32 |
| Sensors | LiDAR, MPU6050, NEO-7 GPS |
| Communication | Wi-Fi, UDP, HTTP/REST |
| Data & Mapping | GPS/GIS, structured JSON events |
| Dashboard | Existing web dashboard and backend |

## 📡 Current Prototype

The current development focuses on:

- Running road-hazard detection on a Raspberry Pi.
- Integrating sensor readings through a unified Python module.
- Transmitting hazard events from Vehicle A to an ESP32-based Vehicle B.
- Developing dashboard integration for telemetry and road-hazard visualization.

Some integrations are still under development; capabilities listed as future or planned features should not be considered production-ready.

## 🔮 Future Roadmap

- Multi-hazard detection and road-condition classification.
- Sensor fusion for more reliable hazard verification.
- GPS-tagged road-risk heatmaps.
- Offline-first data storage and synchronization.
- Fleet analytics and predictive road-maintenance insights.
- V2I and broader V2X communication.
- Custom embedded hardware for scalable vehicle retrofitting.

## 🎯 Potential Applications

- Smart cities and municipal road monitoring.
- Highway and road-maintenance authorities.
- Commercial vehicle and logistics fleets.
- Public transport and institutional fleets.
- Connected-vehicle safety systems.

## 🤝 Contributing

Contributions, ideas, testing, and collaboration are welcome. Please open an issue to discuss proposed features or report bugs before submitting major changes.

## ⚠️ Development Status

iSARTHI is an actively developing prototype. Detection accuracy, hardware reliability, communication performance, and deployment readiness require further validation under real-world conditions.

## 📜 License

A license has not yet been specified. Usage, modification, and redistribution permissions should be established before the project is shared for broader collaboration.

---

**iSARTHI — Building Smarter Roads. Enabling Safer Journeys.**
