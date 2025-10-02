# Smart Traffic Control System

![Status](https'://img.shields.io/badge/status-in--progress-yellow') ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

An adaptive, Cyber-Physical System designed to alleviate traffic congestion in developing nations using RFID-based vehicle density detection.

---
## 📜 Overview

In developing nations, traffic congestion is a significant obstacle to progress, leading to challenges such as air pollution, fuel wastage, and reduced productivity. Traditional countdown-based traffic management systems are often inefficient in fluctuating traffic conditions.

This project proposes an **adaptive traffic management system** that dynamically adjusts signal timings based on real-time vehicle density. We have developed a Cyber-Physical System prototype that measures vehicle density using **RFID technology**. This approach not only optimizes traffic flow but also enables a suite of smart city features.

---
## ✨ Key Features

* **🚗 Dynamic Signal Timing:** Adjusts green light duration based on the number of vehicles in a lane.
* **🅿️ Smart Parking Integration:** Guides drivers to available parking spots and calculates parking fees time based.
* **💳 Intelligent Toll System:** Automates toll collection without requiring vehicles to stop.
* **🚑 Emergency Vehicle Prioritization:** Clears a path for emergency vehicles by turning signals green in their direction.

---
## Getting Started

This project is divided into two main components: a Python-based simulation and an Arduino-based hardware prototype.

### 1. Traffic Simulation (Python)

The simulation visualizes the adaptive traffic control algorithm in action.

#### Requirements
* Python 3.x
* Pygame library
    ```bash
    pip install pygame
    ```

#### Execution
1.  Ensure the `images` folder is in the same directory as the Python script.
2.  Run the simulation file from your terminal:
    ```bash
    python smart_traffic_cntrl_sim.py
    ```

### 2. Hardware Prototype (Arduino)

The hardware prototype demonstrates the RFID functionality for traffic, parking, and tolling systems.

#### Hardware Requirements
* Arduino Board (e.g., Uno, Nano)
* MFRC522 RFID Reader/Writer Module
* RFID Cards/Tags (13.56MHz)
* Jumper Wires
* bread board
* red and green lights
* resistors

#### Software Requirements
* [Arduino IDE](https://www.arduino.cc/en/software)

#### Execution Steps

1.  **Hardware Connection**
    * Connect the MFRC522 RFID module to your Arduino board. For standard pinout diagrams and tutorials, refer to the official documentation or trusted guides:
        * **[Arduino MFRC522 Tutorial by Last Minute Engineers](https://lastminuteengineers.com/mfrc522-rfid-reader-with-arduino/)**

2.  **Connect to PC**
    * Connect your Arduino board to your PC using a USB cable.

3.  **Prepare RFID Cards (Write Data)**
    * Before running the main projects, you must write unique identifiers to your RFID cards.
    * Open a utility sketch designed for writing data (e.g., `WriteDataToCard.ino` if you have one).
    * In the sketch, modify the data to be written to the card. It should follow the format below, which you can update as needed:
        ```c++
        // ---- UPDATE YOUR DATA FORMAT HERE ----
        // Example: A unique vehicle ID like "KA01MJ1234"
        String cardData = "xyz"; 
        // ------------------------------------
        ```
    * Upload this sketch to your Arduino.
    * Bring each RFID card near the reader one by one to write the unique data onto it. You can monitor the progress in the Serial Monitor.

4.  **Run the Main Projects**
    * Once your cards are prepared, you can run the main applications.
    * Open one of the main project sketches (e.g., `Smart_Traffic.ino`, `Smart_Parking.ino`, or `Smart_Toll.ino`).
    * Upload the sketch to your Arduino board.
    * Open the **Serial Monitor** (`Tools > Serial Monitor` or `Ctrl+Shift+M`) to see the output and interact with the system.

---
## ⚡ Future Scope

This approach has the potential for diverse future applications, including:
* Integration with GPS for city-wide traffic prediction.
* Data collection for urban planning and infrastructure development.
* Automated vehicle tracking and management for logistics companies.

---
## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
