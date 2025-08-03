
# ⚡ Automated Power Grid Monitor

This repository contains the source code and documentation for an IoT system designed to monitor and visualize power grid fluctuations. The system uses an **Arduino microcontroller** to read data from various sensors (voltage, current, and temperature) and sends this data to a **Python-based dashboard** for real-time visualization.

---

## 📌 Project Overview

The primary goal of this project is to create a **low-cost, real-time monitoring solution** that can be used to:

- 🔍 **Detect Anomalies**: Identify voltage sags, swells, or unusual current draws.  
- 🌡️ **Prevent Overheating**: Monitor ambient and component temperatures to prevent potential failures.  
- 📊 **Visualize Trends**: Provide a live dashboard to observe power usage and grid stability over time.

> This project is ideal for educational purposes, home automation enthusiasts, or for monitoring small-scale power systems.

---

## 🚀 Features

- **Real-time Data Collection**: Continuously reads voltage, current, and temperature data.
- **Serial Communication**: Transmits data from the Arduino to a computer via USB.
- **Live Data Visualization**: A Python script creates a dynamic dashboard with three interactive plots.
- **Modular Design**: Easy to extend with additional sensors or different visualization tools.

---

## 🧰 Getting Started

### ✅ Prerequisites

#### Hardware

- Arduino Uno or ESP32  
- AC Voltage Sensor Module (e.g., ZMPT101B)  
- AC Current Sensor (e.g., SCT-013-000)  
- DS18B20 Temperature Sensor  
- Breadboard and Jumper Wires  
- USB Cable (for Arduino)

#### Software

- Arduino IDE  
- Python 3.x  

#### Python Libraries

```bash
pip install pyserial matplotlib
```

#### Arduino Libraries

- `OneWire`  
- `DallasTemperature`  
(Install via Arduino Library Manager)

---

## 🔧 Installation & Setup

### 🛠️ Hardware Assembly

- Connect the AC Voltage and Current sensors to the Arduino's **analog input pins** (A0 and A1).
- Connect the DS18B20 Temperature sensor to a **digital pin** (e.g., D2).
- Ensure all connections are secure and follow a proper **circuit diagram**, especially for AC components.

### 🔌 Arduino Code

1. Open the `arduino-grid-monitor-cpp` code in your Arduino IDE.  
2. Install the required libraries (`OneWire`, `DallasTemperature`).  
3. Connect your Arduino to your computer via USB.  
4. Select the correct **board** and **port** from the Tools menu.  
5. Upload the code to your Arduino.

### 🐍 Python Dashboard

1. Open the `python-grid-monitor-dashboard.py` script in any text editor or Python IDE.  
2. **Important**: Update the `arduino_port` variable to match your system:
   - Windows: `'COM3'`
   - Linux: `'/dev/ttyACM0'`
   - macOS: `'/dev/cu.usbmodem...'`
3. Run the script:

```bash
python your_script_name.py
```

---

## 📈 Usage

Once the Python script is running, a dashboard window will display **three real-time plots**:

- **Voltage (V)**: Monitors the stability of the input voltage.  
- **Current (A)**: Shows the electrical load over time.  
- **Temperature (°C)**: Tracks the temperature of the monitored environment.

> The plots update automatically as new data is received from the Arduino. Use them to detect anomalies or system instability.

---

## 🔮 Future Improvements

- ☁️ **Cloud Integration**: Connect to platforms like AWS IoT, Google Cloud IoT, or ThingSpeak for remote monitoring and data storage.  
- 🚨 **Alerting System**: Add email, SMS, or push notification alerts when sensor readings exceed thresholds.  
- ⚡ **Power Factor Sensing**: Incorporate power factor monitoring for a more complete view of efficiency.  
- 📡 **Wireless Connectivity**: Use ESP32 for Wi-Fi-based transmission and eliminate USB dependency.

---
