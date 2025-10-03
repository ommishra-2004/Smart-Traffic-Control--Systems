# Smart Traffic Control System

![Status](https://img.shields.io/badge/status-in--progress-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

An adaptive, Cyber-Physical System designed to alleviate traffic congestion in developing nations using RFID-based vehicle density detection.

---
## 📜 Overview

In developing nations, traffic congestion is a significant obstacle to progress, leading to challenges such as air pollution, fuel wastage, and reduced productivity. Traditional countdown-based traffic management systems are often inefficient in fluctuating traffic conditions.

This project proposes an **adaptive traffic management system** that dynamically adjusts signal timings based on real-time vehicle density. We have developed a Cyber-Physical System prototype that measures vehicle density using **RFID technology**. This approach not only optimizes traffic flow but also enables a suite of smart city features.

---
## ✨ Key Features

* **🚗 Dynamic Signal Timing:** Adjusts green light duration based on the number of vehicles in a lane.
* **🅿️ Smart Parking Integration:** Guides drivers to available parking spots and calculates parking fees based on time.
* **💳 Intelligent Toll System:** Automates toll collection without requiring vehicles to stop.
* **🚑 Emergency Vehicle Prioritization:** Clears a path for emergency vehicles by turning signals green in their direction.

---
## 🚀 Getting Started

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
* Breadboard
* Red, Green, and Yellow LEDs
* Resistors (100 and 1000 Ohms)

#### Software Requirements
* [Arduino IDE](https://www.arduino.cc/en/software)

#### Execution Steps

1.  **Hardware Connection**
    * Connect the MFRC522 RFID module and LEDs to your Arduino board. For standard pinout diagrams and tutorials, refer to this trusted guide:
        * **[Arduino MFRC522 Tutorial by Last Minute Engineers](https://lastminuteengineers.com/mfrc522-rfid-reader-with-arduino/)**
    
    <p align="center">
      <img width="400" alt="Hardware Connection Diagram" src="https://github.com/user-attachments/assets/2529fdc4-f2f0-40f9-957c-2e76451a7d50">
    </p>

    * **Note:** If connecting the 3.3V pin of the MFRC522 to the 3.3V pin of the Arduino doesn't work, try connecting the MFRC522's 3.3V pin to the Arduino's VIN pin instead.
      
2.  **Connect to PC**
    * Connect your Arduino board to your PC using a USB cable.

3.  **Prepare RFID Cards (Write Data)**
    * Before running the main projects, you must write the vehicle data to the memory blocks of your RFID cards.
    * Open the `Read and Write Tags.ino` sketch provided in this repository. This sketch is designed to write all necessary information to the card in one go.
    * Inside the sketch, update the placeholder variables at the top with the data for the first vehicle.

        ```c++
        // ---- UPDATE VEHICLE DETAILS FOR EACH CARD HERE ----
        String vehicleModel    = "Toyota Camry";
        String vehicleNumber   = "MH04AB1234";
        String vehicleColor    = "Blue";
        String aadharNumber    = "1234 5678 9012";
        String emergencyStatus = ""; // Leave blank, or set to "EMERGENCY"
        String ownerName       = "John Doe";
        long   accountBalance  = 2000;
        // ---------------------------------------------------
        ```
    * Upload the sketch to your Arduino.
    * Open the Serial Monitor (`Ctrl+Shift+M`) and bring a blank RFID card near the reader. The sketch will write all the data to the correct blocks.
    * Repeat the process for each vehicle/card, changing the variables in the sketch as needed.

4.  **Run the Main Projects**
    * Once your cards are prepared, open one of the main project sketches (`Traffic Lights.ino`, `Parking System.ino`, or `Tolling System.ino`).
    * Upload the sketch to your Arduino board.
    * Open the **Serial Monitor** to see the output and interact with the system.

---
## 💳 RFID Card Memory Map

The system uses the following memory blocks on the MIFARE Classic 1K cards to store vehicle information (For Refernce) :
+------------------------------------+
|         MIFARE Classic 1K          |
|------------------------------------|
| Block 1:  Vehicle Model            |
|------------------------------------|
| Block 2:  Vehicle Number           |
|------------------------------------|
| Block 4:  Vehicle Color            |
|------------------------------------|
| Block 5:  Aadhar Number            |
|------------------------------------|
| Block 6:  Emergency Status         |
|------------------------------------|
| Block 8:  Owner's Name             |
|------------------------------------|
| Block 10: Account Balance          |
+------------------------------------+

**Note:** you can change the Block No's as per your need while writng data into blocks but don't forget to then change everything in rest of the codes (like Parking systems.ino , Traffic Lights.ino etc)

---
## ⚡ Future Scope

This approach has the potential for diverse future applications, including:
* Integration with Yolo based Algorithms for city-wide traffic data collection and prediction.
* Data collection for urban planning and infrastructure development.
* Automated vehicle tracking for goverment using traffic signal networks.
* Lane optimizations for lanes ahead based on the traffic conditions of previous lanes for overall syncing of all the lanes for smoother traffic flow.

---
## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
