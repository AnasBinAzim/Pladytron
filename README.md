# 🤖 ** INTRODUCING TEAM PLADYTRON - WRO 2025 ** 🤖
# UPDATE: We placed 20th on the World Robot Olympiad 2024 (Turkey)
<div align="center">
  <img width="1280" height="568" alt="image" src="https://github.com/user-attachments/assets/930fa959-45ad-4a6b-877a-23a41c0a6785" />

</div>

---

## 👥 **Team PLADYTRON**

- **Anas Bin Azim**  – Software & Hardware Developer | [anas.azim.71@gmail.com](mailto:anas.azim.71@gmail.com)
- **Mohiuddin Sami** – Primary Software Developer | [sm.mohiuddin.sami@gmail.com](mailto:sm.mohiuddin.sami@gmail.com)

**Team Origin**: Bangladesh

---

### 🌟 **The Meaning Behind PLADYTRON**

Our team name, “PLADYTRON,” dances between the realms of play and technology—a symphony of creativity and code. Like sparks igniting in the dark, our ideas come alive through the joyful spirit of discovery and the relentless pulse of innovation. But beyond the screens and circuits, there is an unseen force : our wellspring of strength: the unwavering support of those who walk beside us. Their hopes, whispered like secret blessings, fuel every challenge we embrace. In their quiet faith, we find the courage to dream bigger, to build stronger, and to journey farther. Pladytron is more than a name; it is the heartbeat of a shared dream, where joy and determination intertwine to create something truly extraordinary.

---

# The Team  

## Anas Bin Azim  

<img width="960" height="960" alt="image" src="https://github.com/user-attachments/assets/434a9416-e07d-4d49-8c71-0dfb8161ee08" />


**Age:** 17  

**High School:** Adamjee Cantonment College, Dhaka 

**Description:** [Hi! I’m Anas from Bangladesh and this is my second WRO International season. In 2024, I had the honor of representing Team Mayerdoa Robotics at the World Robot Olympiad in Turkey, where we proudly placed 20th in the Future Engineers category. I’ve been deeply involved in robotics for over 4 years, building autonomous systems and competing in both national and international competitions. Beyond robotics, I’m passionate about programming, innovation, quizzing, traveling, and playing cricket]  

---

## Mohiuddin Sami  

<img width="960" height="960" alt="image" src="https://github.com/user-attachments/assets/223a0c30-3b4c-477a-b101-ca55ee2e311c" />



**Age:** 17  

**High School:** Rajuk Uttara Model College, Dhaka 

**Description:** [.]  


## 🎉 Project Overview
<img align="right" alt="SMOKI" width="350" src="https://github.com/user-attachments/assets/46c38599-e416-42cb-93ba-6f83ff142c18">

This repository includes all files, designs, and code for **SMOKI**, our WRO 2024 robot. Below is the folder structure:

## 📂 Structure
Here’s a breakdown of the project folders:

- **`models`**: Contains 3D models and CAD designs.
- **`others`**: Additional documents and miscellaneous files.
- **`schematic`**: Wiring and circuit design diagrams.
- **`src`**: Source code for robot programming.
- **`system-setup`**: Steps for software and hardware setup.
- **`t-photos`**: Technical images of the robot build.
- **`v-photos`**: Visual photos for aesthetics and showcasing.
- **`video`**: Performance and demo videos of SMOKI.
- **`experiments`**: Documentation of trials and iterations with previous models.
- **`license`**: License information for the project.

---







----

## Table of Contents

- [Team MAYERDOA - "Mothers' Prayers"](#team-mayerdoa---mothers-prayers)
- [Mission Overview for WRO Future Engineers Rounds](#mission-overview-for-wro-future-engineers-rounds)
- [Components and Hardware](#components-and-hardware)
- [Assembly Instructions](#assembly-instructions)
- [Project Objective](#project-objective)
- [Mobility Management](#mobility-management)
- [Power and Sense Management](#power-and-sense-management)
- [Program Infrastructure and Explanation of Algorithm](#program-infrastructure-and-explanation-of-algorithm)
- [Software Setup](#software-setup)





Our bot, **SMOKI**, is built for excellence in the **World Robot Olympiad 2024** in the Future Engineers category. From its structural core using LEGO Technic elements to its computing capabilities powered by the **Raspberry Pi 5** and **ESP32 microcontroller**, SMOKI is crafted to handle the nuanced challenges of autonomous navigation and obstacle handling.

---

### Mission Overview for WRO Future Engineers Rounds

<table>
  <tr>
    <td width="50%" valign="top" align="left">
      <h3>🏁 Round 1: Lap Completion</h3>
      <p>In <strong>Round 1</strong>, the robot must autonomously complete <strong>three laps</strong> on a pre-defined track. The goal of this round is for the bot to demonstrate stable navigation and precise lap tracking without any obstacle avoidance requirements.</p>
      <ul>
        <li><strong>Objective</strong>: Complete three laps on the track within the allotted time.</li>
        <li><strong>Key Tasks</strong>: Accurate path-following, speed control, and lap counting.</li>
      </ul>
      <div align="center">
        <br><br><br><br><br>
        <img src="https://github.com/user-attachments/assets/823b29fa-8c92-479e-a78a-9fc96c407858" alt="Round 1 WRO Track" width="250" height="180" />
      </div>
    </td>
    <td width="50%" valign="top" align="left">
      <h3>🏆 Round 2: Lap Completion with Obstacle Avoidance and Parking</h3>
      <p>In <strong>Round 2</strong>, the bot must complete <strong>three laps</strong> while avoiding green and red obstacles:</p>
      <ul>
        <li><strong>Green Obstacles</strong>: The bot should move <strong>left</strong> to avoid.</li>
        <li><strong>Red Obstacles</strong>: The bot should move <strong>right</strong> to avoid.</li>
      </ul>
      <p>After completing the laps, the bot must accurately park within a designated zone.</p>
      <ul>
        <li><strong>Objective</strong>: Complete three laps, avoid obstacles, and park in the designated area.</li>
        <li><strong>Tasks</strong>: Obstacle detection, color-based avoidance, and precision parking.</li>
      </ul>
      <div align="center">
        <img src="https://github.com/user-attachments/assets/b578392d-b443-4315-8fe3-f03af828c39a" alt="Round 2 WRO Track" width="250" height="180" />
      </div>
    </td>
  </tr>
</table>

---
>[!IMPORTANT]
>**Important: WRO Future Engineers Rulebook**
>* **Thorough Reading:** Ensure that you thoroughly read the **WRO Future Engineers 2024 Rulebook** to understand all rules and guidelines.
>* **Official Link:** Access the rulebook here: [🔗 WRO Future Engineers 2024 Rulebook](https://wro-association.org/competitions/future-engineers/).

---
---


## 🧩 Components and Hardware
Our bot is equipped with various components that support its autonomous functionality. Here is a breakdown of the key hardware elements used in this project:

| Component                  | Description                                                                                      | Image                          | Purchase Link                                                                                  |
|----------------------------|------------------------------------------------------------------------------------------------|--------------------------------|-----------------------------------------------------------------------------------------------|
| **Chassis - Custom Made**   | Custom-designed chassis tailored to fit all components and optimize stability and movement.    | <div align="center"><img src="" alt="Chassis Custom Made" width="100"></div>         | N/A                                                                                           |
| **RPLIDAR C1**             | 360-degree laser scanner used for mapping and obstacle detection.                              | <div align="center"><img src="" alt="RPLIDAR C1" width="100"></div>                   | [Purchase RPLIDAR C1](https://www.mybotshop.de/SLAMTEC-RPLIDAR-C1-360-Laser-Scanner-12-m)     |
| **Servo Motor SG90**       | Small, lightweight servo motor used for precise control of angles and positioning.             | <div align="center"><img src="" alt="Servo Motor SG90" width="100"></div>             | [Purchase SG90](https://bongotech.ai/product/sg90-micro-servo-motor-180-degree)                |
| **SJ CAM C200**            | Captures visual data, supporting navigation and obstacle detection tasks.                      | <div align="center"><img src="" alt="SJ CAM C200" width="100"></div>                  | [Purchase SJ CAM C200](https://amzn.to/3SJCAM) (From previous knowledge)                      |
| **Buck Module XL4016**     | Provides stable voltage regulation for power management.                                      | <div align="center"><img src="" alt="Buck Module XL4016" width="100"></div>           | [Purchase XL4016](https://amzn.to/4xl4016) (From previous knowledge)                          |
| **Motor Driver L293D**     | Dual H-Bridge motor driver for controlling DC motors and stepper motors.                       | <div align="center"><img src="" alt="Motor Driver L293D" width="100"></div>           | [Purchase L293D](https://electropeak.com/l293d-motor-drive-shield)                            |
| **Booster Module 5V to 40V** | Voltage booster module to step up power supply from 5V to 40V, supporting high-voltage requirements. | <div align="center"><img src="" alt="Booster Module 5V to 40V" width="100"></div>       | [Purchase Booster Module](https://robu.in/product-category/electronic-modules/electronic-module/buck-boost-converter/boost-converter/) |





##  Assembly Instructions

### 🏗️Chassis Assembly 

≠

#### 🛠️ Chassis Assembly Process

Here’s a step-by-step overview of the chassis assembly process using the LEGO 45560 Expansion Set:

1. **Base Frame Construction**: Start by assembling the base frame using 5x11 and 5x7 beams for structural stability. These beams provide a strong foundation for mounting additional components.
2. **Motor and Axle Integration**: Utilize the LEGO Technic beams and axle connectors to securely attach the motors. Ensure proper alignment to enable smooth and controlled movement.
3. **Reinforcing with Angular Beams**: Use the 4x6 and 3x5 angular beams to reinforce corners and support areas where weight and stress are concentrated.
4. **Mounting Sensors and Electronics**: Attach sensor mounts and electronic components using cross blocks and bushings, making sure they are aligned for efficient data capture and processing.
5. **Gear Assembly for Differential Drive**: Assemble gears (8, 16, and 24-tooth gears) to create a differential drive system, allowing independent rotation of wheels for smooth turns.

---

## CHASSIS FIRST FLOOR : 

<img width="1422" height="732" alt="image" src="https://github.com/user-attachments/assets/a67bffe7-39af-4c0c-b009-ef4beefd3101" />

This is the first floor of the robot chassis, designed to serve as the primary structural layer of the bot. The STL model shows a flat base plate with multiple precisely positioned mounting holes and slots for components.

Key Features:

Steering Shaft Mount: The elongated slot at the top center is designed to hold the steering shaft, ensuring smooth and stable movement.

Servo Motor Mount: Dedicated mounting holes allow the servo motor to be securely attached for steering control.

Camera Holder: The central cut-out and surrounding structure provide space for installing a camera for vision-based navigation.

Wheel Mounts: Side holes are aligned to support the wheels, making them properly fixed to the frame.

Base Support: This floor acts as the foundation of the robot, supporting the upper floors and ensuring stability during operation.

Dimensions:

Width (X): 101.5 mm

Length (Y): 185.0 mm

Thickness (Z): 10.0 mm

---
---





### CHASSIS STEERING :
<img width="1390" height="721" alt="image" src="https://github.com/user-attachments/assets/5bf6bf24-4169-486a-9a18-3f7ea01eafa4" />



This is the steering plate of the robot chassis, designed to integrate with the first floor and provide precise steering control. The central rectangular gap is a servo clearance slot, which allows the servo horn and linkage to move freely during steering. The smaller holes around the center are meant for mounting the servo securely, while the larger side holes provide attachment points to connect the steering plate with the rest of the chassis. The plate is compact yet durable, ensuring stability during turns, and it directly connects the servo motor to the steering shaft and wheels, making it an essential component for controlling the robot’s movement.

Dimensions:

Width (X): 96.2 mm

Height (Y): 35.55 mm

Thickness (Z): 10 mm

---
---

### STEERING SHAFT :

<img width="1394" height="725" alt="image" src="https://github.com/user-attachments/assets/270cb784-abef-46f4-95c1-31577cfeb1a9" />

This part is the steering shaft of the robot chassis. It connects directly to the steering plate and transmits the motion from the servo motor to the wheels, enabling controlled directional movement. The design includes a central body with mounting cut-outs and side holes that allow it to be fixed securely to the chassis while maintaining free rotational movement where needed. Its sturdy build ensures that torque from the servo is effectively transferred to the wheels without bending or slipping, making it a key component for precise steering.

Dimensions:

Width (X): 

Height (Y): 

Thickness (Z): 


---
---


## CHASSIS SECOND FLOOR :
<img width="1381" height="718" alt="image" src="https://github.com/user-attachments/assets/816acdff-af66-435c-bd58-89c1de20a055" />


This is the second floor of the robot chassis, designed to mount the following components:

RPLIDAR C1 (with a 10 cm clearance ensured by floor orientation)

LiPo 1500mAh 9A 3S battery

STL Dimensions: 131.27 mm × 101.50 mm × 10.00 mm

The plate includes cutouts for weight reduction and cable management, along with mounting holes for secure installation. Its orientation was carefully adjusted to provide the RPLIDAR with optimal clearance for unobstructed 360° scanning.

---


## CHASSIS TOP FLOOR:
<img width="1420" height="720" alt="image" src="https://github.com/user-attachments/assets/9e55ee47-a77b-4c2a-9d98-42b5f0e091a5" />

Top & 3rd Floor – Electronics Section

This floor of the chassis holds the core electronic components required for power regulation and motor control.

Components

Raspberry Pi 4B – Acts as the main controller, handling computation, control logic, and communication.

XL4016 Buck Converter – Steps down the LiPo battery voltage to the levels required by the Raspberry Pi and other electronics.

L293D Motor Driver – Provides motor control by supplying the necessary current and voltage to the DC motors.

Power Switch – Allows safe shutdown and startup of the electronics.

Veroboard – Serves as the wiring platform, connecting the Raspberry Pi, buck converter, motor driver, and switch.

Functionality

The LiPo battery powers the system.

The buck converter regulates the voltage for stable Raspberry Pi operation.

The L293D motor driver interfaces between the Raspberry Pi and the motors, enabling directional control.

The veroboard ensures secure and organized wiring between all components.

The switch provides overall power control for the floor.

---
---


>[!IMPORTANT]
> ALL THE STL AND DXF FILES ARE PROVIDED IN THE MODEL SECTION AND A PREVIEW OF THE WHOLE THING COMBINED IS GIVEN BELOW.
---

# TOTAL PREVIEW:

## Model Views

<table>
  <tr>
    <td align="center"><b>Top</b></td>
    <td align="center"><b>Bottom</b></td>
  </tr>
  <tr>
    <td><img width="544" height="831" alt="rsz_iwo" src="https://github.com/user-attachments/assets/3c0d04ae-508e-48ff-982b-fbca49025b40" />

</td>
    <td><img width="544" height="831" alt="bottomviewbot" src="https://github.com/user-attachments/assets/36fe9b4a-93c7-4e48-aeeb-8a4c9824f216" />
</td>
  </tr>
  <tr>
    <td align="center"><b>Left</b></td>
    <td align="center"><b>Right</b></td>
  </tr>
  <tr>
    <td><img width="1481" height="842" alt="leftviewbot" src="https://github.com/user-attachments/assets/a1a89225-2e90-49f4-a9f2-a159ed0b6e42" />
</td>
    <td><img width="1445" height="814" alt="rightviewbot" src="https://github.com/user-attachments/assets/48038688-0663-4524-9830-18823f7520f6" />
</td>
<tr>
    <td align="center"><b>Tilt1</b></td>
    <td align="center"><b>Tilt2</b></td>
  </tr>
  <tr>
    <td><img width="750" height="803" alt="TILTEDIMAGE" src="https://github.com/user-attachments/assets/34c8f2c8-1b38-43ea-bd9b-fc0961c088fa" />
</td>
    <td><img width="750" height="803" alt="TILTEDIMAGE" src="https://github.com/user-attachments/assets/b37f2262-4a0d-4781-af76-2328b026c4da" />

</td>
  </tr>

</table>



### Mobility Management:

The mobility system of our robot has been meticulously designed to ensure smooth, efficient, and reliable movement, addressing both power distribution and maneuverability. This section outlines the evolution of our robot's mobility systems, including upgrades to the steering and gear systems.

---

#### **16GA 800 RPM DC Gear Motor**

<table>
<tr>
<td width="50%">
<div align="center">
  <img width="600" height="597" alt="image" src="https://github.com/user-attachments/assets/5a446791-2e61-4f52-b6ba-a0e01f6ba39b" />

</div>
</td>
<td width="50%">

A **16GA DC gear motor** is a DC motor with an integrated gearbox. It provides controlled shaft rotation with increased output torque through gearbox reduction.

##### **How the Motor Works**
- The DC motor converts electrical input into rotational motion of the armature and shaft.  
- The gearbox stages reduce output speed and increase torque at the output shaft.  
- The D-flat on the shaft provides a positive mechanical interface for gears, pulleys, or couplings.

##### **Specifications**
- **Rated Speed:** 800 RPM  
- **Shaft Diameter:** 3.0 mm (D-flat: 2.5 mm)  
- **Gearbox Diameter:** 16 mm  
- **Gearbox Length:** 14 mm  
- **Motor Body Length:** 26.5 mm  
- **Shaft Length (protruding):** 11.2 mm

##### **Advantages**
1. **Compact Design**: Small gearbox diameter and short overall length for tight assemblies.  
2. **Increased Torque**: Gear reduction delivers higher torque at the output shaft for loaded conditions.  
3. **Positive Shaft Interface**: D-flat prevents rotary slip when fitted with set-screws or couplings.

</td>
</tr>
</table>

---

### **Rear Axle Power Distribution**

Initially, the rear wheels were powered through a **Bevel Gear**, but we later upgraded to a **Differential Gearbox** to improve efficiency and performance during turns.

---

#### **Bevel Gear**

<table>
<tr>
<td width="50%">
<div align="center">
  <img src="https://github.com/user-attachments/assets/9e19661f-b921-4bea-9028-4e0274306ced" width="300"/>
</div>
</td>
<td width="50%">

A **bevel gear** is a type of gear where the axes of the two shafts intersect, and the tooth-bearing faces of the gears are conical. Bevel gears are commonly used to transfer motion between intersecting shafts at an angle, typically 90°.

##### **How Bevel Gears Work**
- A driver gear transfers motion to a driven gear, which rotates an output shaft.
- The teeth of the gears are designed to mesh smoothly, transferring torque efficiently between the shafts.

##### **Advantages of Bevel Gears**
1. **Compact Design**: Suitable for space-constrained applications.
2. **Efficient Torque Transfer**: Provides reliable power transmission at angles.
3. **Versatility**: Can operate at angles other than 90° if needed.

</td>
</tr>
</table>

---
>[!IMPORTANT]
> Bevel gears were essential in the initial stages of our design, but they had limitations in terms of energy efficiency during turns.
---

#### **Differential Gearbox**

<table>
<tr>
<td width="50%">

A **differential gearbox** allows the wheels on the same axle to rotate at different speeds while receiving power from a single motor. This is crucial for smooth turning, where the outer wheel must travel a larger distance than the inner wheel.

##### **Advantages of Differential Gearbox**
1. **Smooth Turns**: Adapts to varying wheel speeds, ensuring efficient cornering.
2. **Energy Efficiency**: Reduces energy wastage by minimizing wheel slippage.
3. **Component Longevity**: Minimizes wear on tires and axles.

##### **How Differential Gears Work**
- Power from the motor is delivered to an input shaft.
- The differential splits the torque between the two wheels via bevel or spider gears inside the housing.
- During turns, the differential allows one wheel to spin faster than the other, ensuring smooth movement.

</td>
<td width="50%">
<div align="center">
  <img src="https://github.com/user-attachments/assets/4bd7f40f-d350-4215-8cf4-2bf46d3cc779" width="300"/>
</div>
</td>
</tr>
</table>

---

### **Servo Motor with L293D Motor Driver**

<table>
<tr>
<td width="30%">
<div align="center">
  <img src="https://github.com/user-attachments/assets/ffcfa0ae-2682-4199-8c0b-4bcbff421d08" width="150"/>
</div>
</td>
<td width="70%">

We used the **L293D Motor Driver** in combination with a **Servo Motor** to control the robot's wheels effectively. The L293D is a dual H-Bridge motor driver that is perfectly suited for the LEGO motor, which operates at **750mA** current.

##### **Why L293D?**
- **Optimal Current Capacity**: Can handle up to **1A** peak current, suitable for the LEGO motor’s 750mA requirement.
- **Bidirectional Control**: Facilitates forward and backward motion of the wheels.
- **Compact and Lightweight**: Ideal for small-scale robotic systems.
- **PWM Support**: Enables smooth speed control of the motors.

##### **Advantages of the Servo Motor with L293D**
1. **Accurate Steering**: The servo motor ensures precise angle adjustments.
2. **Smooth Speed Control**: PWM functionality provides variable speed control.
3. **Efficient Current Management**: Matches the LEGO motor's current needs, ensuring reliable operation.

</td>
</tr>
</table>

---

#### **Comparison: Bevel Gear vs. Differential Gearbox**

| **Feature**                | **Bevel Gear**                            | **Differential Gearbox**                |
|----------------------------|-------------------------------------------|-----------------------------------------|
| **Turning Efficiency**     | Limited; fixed wheel speeds.             | Superior; wheels rotate independently. |
| **Energy Usage**           | Higher due to slippage during turns.     | Lower; optimized for dynamic turns.    |
| **Durability**             | Higher strain on components.             | Reduced strain; longer component life. |

---

### **Steering Systems**

Our robot initially used the **Ackermann Steering System**, known for its efficiency in real-world vehicles. However, we later transitioned to the **LEGO Steering System** to simplify the design and improve modularity while maintaining effective steering control.

---

#### **What is Ackermann Steering System?**

The **Ackermann Steering System** ensures that the wheels of a vehicle turn at different angles during a corner. The inner wheels turn more sharply than the outer wheels, reducing tire slippage and allowing smooth, efficient turning.

##### **How Ackermann Steering Works**
- The front wheels are connected via a set of steering arms.
- These arms are angled so that their lines meet at the center of the turn’s radius, ensuring concentric paths for all wheels.

##### **Advantages of Ackermann Steering**
1. **Efficient Turning**: Minimizes tire slippage.
2. **Energy Savings**: Reduces power loss caused by wheel drag.
3. **Realistic Simulation**: Mirrors real-world vehicle steering.



# ⚡ Electronics and Power System

- **Power Module**: Ensures consistent power to the Raspberry Pi and ESP32.
- **Wiring**: Organized to minimize interference.

----
----
----



# ⚡ Power and Sense Management

The **Power and Sense Management** system of our robot has been meticulously designed to optimize performance while ensuring reliable power delivery, precise sensing, and efficient communication between components.

---
## 🔋 Power Distribution

Our robot's power system has been engineered for stability and efficiency, addressing all unique voltage and current requirements:
1. **🔋 Two Lithium-Ion Cells**: Each rated at **4.2V**, providing a total of **8.4V**.
2. **⚙️ XL4016 Buck Converter**: Steps down **8.4V** to a stable **5V** for powering the Raspberry Pi 5 and other components.
3. **🔌 Buck Modules**:
   - One module supplies **6V** for the servo motor.
   - Another module provides **5V** for the ESP32 microcontroller.
4. **⚡ 12V Power for Motors**: Delivered using a **Buck-Boost Converter** to ensure consistent motor performance.

---

### 🎥 Camera Placement and Functionality

The robot's main camera is positioned at the top and angled slightly downwards. This setup enhances object detection capabilities by providing:
- **🔍 Close-Range Detection**: The camera can identify objects in close proximity with high accuracy.
- **🌐 Extended-Range Detection**: Ensures objects further away are detected effectively.

The camera feeds data to the **Raspberry Pi 5**, which processes image recognition algorithms to detect towers and corner lines. The processed data is then transmitted to the **ESP32 microcontroller** for real-time navigation and obstacle avoidance.

---

### 📡 Sonar Mount Design

### 🛠️ Previous Design
In our earlier design, we used **HC-SR04 sonar sensors** placed at **45-degree angles**, mounted horizontally on two sides of the robot, with one sensor placed vertically in the middle. This configuration provided basic obstacle detection but had limitations:
- **🚫 Blind Spots**: The horizontal placement created gaps in detection range at certain angles.
- **⚠️ Inconsistent Readings**: The 45-degree angle sometimes caused inaccuracies due to signal reflections.

### 🔄 Why We Switched
After analyzing performance during testing, we made significant improvements:
- Replaced the 45-degree sensors with sensors mounted at **15 degrees**.
- Mounted the sensors **vertically on all sides**, ensuring:
  - **🛑 Improved Obstacle Detection**: Enhanced accuracy and coverage around the robot.
  - **📏 Better Range Consistency**: Reduced signal reflection issues for more reliable readings.

### 🚀 Current Design
The new configuration leverages **HC-SR04 sonar sensors**, chosen for their **wide availability** and **affordable price**. The updated design provides:
- **360° Coverage**: Vertical mounting eliminates blind spots.
- **Early Detection**: Enhanced obstacle sensing allows for quicker decision-making.

---


>[!IMPORTANT]
> **Power Highlights:**
> - The XL4016 Buck Converter ensures stable voltage regulation, critical for protecting the Raspberry Pi and ESP32 microcontroller during operation.
> - Independent buck modules handle the servo motor and ESP32 power needs, optimizing energy usage across all components.

---
---

## 🛠️ PCB Design

We have developed a **custom hand-designed PCB** to streamline the robot's power distribution and sensor integration. The PCB offers:
- **📐 Optimized Layout**: Minimizing signal interference for reliable performance.
- **🎯 Compact Design**: Saving space within the robot's chassis.
- **💪 Enhanced Durability**: Ensuring longevity during competitive operation.

---

## 🖼️ System Visuals

| **Top View of PCB** | **Bottom View of PCB** | **Power Management Diagram** |
|----------------------|------------------------|-------------------------------|
| <img src="https://github.com/user-attachments/assets/be051834-2c23-495e-9aa1-83d9620e1524" width="400"/> | <img src="https://github.com/user-attachments/assets/45d68411-f99a-4ef4-8aef-c63eb856a8e1" width="400"/> | <img src="https://github.com/user-attachments/assets/0f01372c-1cff-4ff7-b65b-5e5a5ca5f" />

---
---
---


# 🧠 Program Infrastructure and Explanation ## 🏁 Round 1 Algorithm - Lap Completion

In **Round 1**, our robot **SMOKI** must autonomously complete **three laps** on a predefined track without the need for obstacle avoidance. To achieve precise navigation and lap counting, we have developed a robust algorithm that integrates image processing with control systems.

---

### 🌐 Algorithm Overview

1. **📸 Image Acquisition**:
   - The robot captures real-time images of the track using its onboard camera.

2. **🎨 Color Space Conversion**:
   - Captured images are converted from the **RGB** color space to the **HSV (Hue, Saturation, Value)** color space.
   - The HSV color space is chosen for its effectiveness in color segmentation, as it is less sensitive to lighting variations.

3. **🔍 Color Segmentation and Orientation Determination**:
   - Using predetermined HSV ranges, the algorithm isolates the **blue** and **orange** line segments on the track.
   - During the first run, the robot checks whether the blue line appears before the orange line or vice versa.
   - **Orientation Determination**:
     - If the blue line comes before the orange line, the robot sets its orientation accordingly.
     - This initial orientation check ensures the robot follows the track in the correct direction.

4. **📏 Line Detection and Lap Counting**:
   - The **Hough Line Transform** method is applied to detect lines within the segmented images.
   - The robot counts the detected lines to keep track of laps.
   - **Lap Completion**:
     - After counting **12 lines** (corresponding to three laps), the robot initiates a predetermined delay and then stops.

5. **⚙️ Position Correction Using PID Control**:
   - Before setting the orientation, a **PID (Proportional-Integral-Derivative) controller** calculates the error.
   - **Error Calculation**:
     - The error is determined by the difference between the distances measured by sensors on the left and right sides of the robot (i.e., `error = left_distance - right_distance` or vice versa).
   - **Distance Maintenance**:
     - If the orientation is **right-based**, the robot maintains a **25 cm** distance from the right side.
     - If the orientation is **left-based**, it maintains a **25 cm** distance from the left side.
   - The PID controller adjusts the robot's steering to minimize the error, helping it stay centered on the track.

---

## 📖 Detailed Explanation

### 1. 📸 Image Acquisition and Preprocessing
- **Camera Input**: High-resolution images are captured at regular intervals to ensure up-to-date visual data.
- **HSV Conversion**: Conversion to HSV allows for more effective color thresholding. HSV separates image intensity (Value) from color information (Hue and Saturation), making it easier to detect specific colors under varying lighting conditions.

### 2. 🎨 Color Segmentation
- **HSV Thresholding**: 
  - **Blue Line Detection**: Pixels within the blue HSV range are extracted.
  - **Orange Line Detection**: Pixels within the orange HSV range are extracted.
- **Orientation Check**: By analyzing the sequence of color segments (blue vs. orange), the robot determines its starting orientation. This prevents incorrect lap counting due to starting in the wrong direction.

### 3. 📏 Line Detection with Hough Transform
- **Edge Detection**: Preprocessing steps like Gaussian blur and Canny edge detection are applied to enhance line features.
- **Hough Line Transform**: Detects straight lines by transforming points in image space to a parameter space. Lines are identified based on the accumulation of intersecting points in the parameter space.
- **Lap Counting Logic**: Each detected line crossing increments a counter. The robot recognizes lap completion after counting **12** line crossings, accounting for both blue and orange lines over three laps.

<div align="center">
  <!-- Placeholder for Hough Line Transform Image -->

  <img src="https://github.com/user-attachments/assets/24ef6a2d-ce3d-4522-8181-7e811d370d6b" alt="Hough Line Transform" width="600">
  <p><em>Figure: Visualization of Hough Line Transform applied to track image.</em></p>
</div>

#### 🔗 **Hough Line Transform Tutorial**

For a comprehensive understanding of the Hough Line Transform method, you can watch this detailed tutorial:

- [🔗 Hough Line Transform Tutorial by DigitalSreeni](https://www.youtube.com/watch?v=5zAT6yTHvP0&ab_channel=DigitalSreeni)

### 4. ⚙️ PID Control for Position Correction
- **Sensor Input**: Distance sensors on both sides provide real-time measurements of the robot's position relative to the track edges.
- **Error Calculation**: The error signal is the difference between the left and right distance measurements, ensuring the robot stays in the middle of the track by minimizing this difference to zero.
- **PID Controller**: 
  - **Proportional Term (P)**: Reacts to the current error.
  - **Integral Term (I)**: Accounts for past errors to eliminate steady-state offset.
  - **Derivative Term (D)**: Predicts future error based on the rate of change.
- **Steering Adjustment**: The PID output adjusts the steering angle to minimize the error. This ensures the robot maintains the desired position centered between the track edges.
- **Orientation-Based Behavior**:
  - **Right-Based Orientation**: The robot favors the right side of the track.
  - **Left-Based Orientation**: The robot favors the left side of the track.

## 📦 Project Structure

## 📊 Round 1 Algorithm - Corner Detection Navigation
## 📖 Detailed Algorithm Description

In Round 1 of the **Future Engineers** category, our robot follows a structured pipeline to complete a lap, detect corners, and terminate correctly at the finish line. The algorithm is designed to balance **robust line tracking** with **precise stopping conditions**.

---

### 🔹 Step 1 – Image Acquisition
- Capture live frames using the Pi Camera.
- Convert the frames from **BGR to HSV** for better color segmentation.

---

### 🔹 Step 2 – Line Detection
- Apply masking to detect the black line on the arena.
- Use contour/moments to find the line’s centroid.
- If the line is detected:
  - Increment the **line counter**.
  - Reset the **last line timestamp**.

---

### 🔹 Step 3 – Orientation and Corner Detection
- If a corner is detected (sharp angle/edge in the line):
  - Increment the **corner counter**.
- Orientation is adjusted automatically based on the line’s slope and direction.

---

### 🔹 Step 4 – Obstacle / Missing Line Handling
- If the line is missing:
  - Scan using LiDAR/adjacent frame data.
  - Calculate slopes of adjacent left and right boundaries.
  - If **perpendicular slope** detected → count as a line.
  - Otherwise → apply **weighted average** to determine the best path.

---

### 🔹 Step 5 – PID Steering
- Use a **PID controller** to calculate steering corrections.
- Maintain smooth navigation while keeping the robot centered on the track.

---

### 🔹 Step 6 – Termination Condition
The robot stops when all three conditions are met:
1. **Line Count ≥ 12**  
2. **Last Line Detected > 1500 ms ago**  
3. **Floor Distance < 1500 mm** (from ultrasonic/LiDAR sensor)  

If these conditions are true:
- Stop all motors.
- Terminate the run.

Otherwise:
- Continue navigation using the **Weighted Average path selection**.

---
**Flowchart:**

```mermaid
flowchart TD
    A[Start] --> B[Capture Image]
    B --> C{Line Detected?}
    
    %% Line Detected Branch
    C -->|Yes| D{Orientation Set?}
    D -->|Yes| E[Line Count ++]
    D -->|No| F[Fix Orientation for Next Run and Line Count ++]
    E --> G{LineCount >= 12 AND LastLine > 1500ms AND FloorDist < 1500?}
    F --> G
    G -->|Yes| H[Stop Bot and Terminate Code]
    G -->|No| K[Use Weighted Average from LIDAR to Find Best Path]
    
    %% No Line Detected Branch
    C -->|No| I[LIDAR Scan Image]
    I --> J{Slope of Adjacent Lines?}
    J -->|Perpendicular| L[Line Count ++]
    J -->|Not Perpendicular| K
    L --> G
    
    %% Common Path
    K --> M[PID Calculates Steering Value]
    M --> N[Continue Navigation]


```



---


# 🏆 Round 2 Algorithm - Lap Completion with Obstacle Avoidance and Object Detection

Round 2 involves an enhanced version of our robot SMOKI, which autonomously completes three laps, avoiding obstacles and calculating the steering value based on object prioritization and boundary detection. Below is an in-depth look at the step-by-step algorithm implemented for this round.

## 🌟 Step-by-Step Algorithm Overview

### 📸 Image Acquisition:
- The camera captures real-time images of the track and surroundings.

### 🎨 HSV Color Conversion:
- Convert the captured image from RGB to HSV (Hue, Saturation, Value) scale.
- Store all relevant line and object colors for further use.

### 💨 Gaussian Blur:
- Apply Gaussian Blur to the frame to reduce noise.
- Based on predetermined HSV range, isolate the black border portion.

### ⚫ Black Border Detection:
- Use Canny Edge Detection to identify the black border walls.
- Apply Hough Line Probabilistic Transformation to determine acceptable border walls.

### 🛑 Border Masking:
- Create a border in the frame based on the detected lines.
- Mask out everything beyond the border to eliminate unnecessary information for the rest of the algorithm.

### 🔍 Line Detection (Blue or Orange):
- Identify lines using the predetermined HSV color range.
- Check for the blue or orange line in the frame.

### 📐 Slope Calculation:
- If a line is found, calculate the minimum and maximum slopes for both the blue and orange lines (if both are present).

### ↩️ Orientation Determination:
- If both blue and orange lines are detected, compare their slopes.
- Determine the clockwise or anti-clockwise orientation and store this in a variable for future reference.

### 📊 Object Detection and Prioritization:
- Detect acceptable objects within the boundary wall.
- Assign a priority value to each object based on distance, orientation, and coordinates.
- Register only one object based on predetermined mathematical calculations.
- Calculate the steering value for navigation using a quadratic function based on the object's distance and position along the x-axis.

### 📡 Serial Communication:
- Send the calculated steering value to the ESP32 via serial communication to adjust the robot's movement accordingly.

---

## Algorithm Explanation

- **HSV Conversion** allows for effective color segmentation, making it easier to distinguish between track lines and other features regardless of lighting conditions.
- **Gaussian Blur** helps to reduce noise, making the detection of borders and lines more reliable.
- Using **Hough Line Transform** and **Canny Edge Detection** enables accurate identification of boundaries, which is crucial for masking irrelevant parts of the frame.
- **Slope Comparison** provides the robot with information about its current orientation, enabling it to differentiate between clockwise and anti-clockwise directions based on the detected lines.
- The **Object Prioritization** mechanism ensures that the robot only reacts to the most relevant obstacle, improving navigation efficiency.
- Finally, the calculated steering value is sent to the ESP32 for precise movement control, ensuring that the robot maintains its intended path while avoiding obstacles effectively.

## Video Tutorial for Hough Line Transform

For a better understanding of how the Hough Line Transform method is used in our algorithm, you can watch this detailed video tutorial:

- [🔗 Hough Line Transform Tutorial by DigitalSreeni](https://www.youtube.com/watch?v=6-3HgNZkDGA)

## Next Steps

- Test the algorithm in various track conditions to ensure robustness.
- Fine-tune the HSV color ranges and quadratic function for steering to achieve optimal performance.
- Collect data on the robot's performance to further refine the object prioritization logic.

Feel free to reach out if you need more insights or help with further tuning the algorithm!




## **Flowchart**

```mermaid

flowchart TD
    A[Start] --> B[Capture Image]
    B --> O{Object Detected?}

    %% Object Detected Branch
    O -->|Red Object| P[Steer Right with PID]
    O -->|Green Object| Q[Steer Left with PID]
    P --> N[Continue Navigation]
    Q --> N

    %% No Object Detected Branch → Round 1 Logic
    O -->|No| C{Line Detected?}
    
    %% Line Detected = Yes
    C -->|Yes| D{Orientation Set?}
    D -->|Yes| E[Line Count ++]
    D -->|No| F[Fix Orientation for Next Run and Line Count ++]
    E --> G{LineCount >= 12 AND LastLine > 1500ms AND FloorDist < 1500?}
    F --> G
    G -->|Yes| H[Initiate Parking Maneuver]
    G -->|No| K[Use Weighted Average from LIDAR to Find Best Path]

    %% Line Detected = No
    C -->|No| X{LineCount >= 12 AND LastLine > 1500ms AND FloorDist < 1500?}
    X -->|Yes| H
    X -->|No| I[LIDAR Scan Image]
    I --> K
    
    %% Common Path
    K --> M[PID Calculates Steering Value]
    M --> N[Continue Navigation]
```
<p align="center">
  # THATS ALL FROM US
</p>


<img src="https://github.com/user-attachments/assets/3c4eb0aa-37f5-4255-a176-253f5ae422f5" />
