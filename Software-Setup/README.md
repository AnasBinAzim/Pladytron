# 🛠️ Software & Tools Used  

Our project required a wide range of software for **3D design, circuit simulation, PCB layout, coding, and system setup**. Each tool was chosen for its specific strengths, ensuring that every part of the robot — from the mechanical design to the embedded software — was well-supported. Below is a detailed overview of the software stack we used:  

---

### ⚙️ Onshape (Mechanical CAD Design)  
Onshape was used to design the **mechanical parts and assemblies** of the robot. Being a cloud-based CAD tool, it allowed for real-time collaboration and easy access from multiple devices. We modeled the robot chassis, servo holders, camera mounts, and other 3D-printable parts directly in Onshape, ensuring precision and proper fit before manufacturing. The parametric modeling features helped us quickly adjust dimensions when we iterated through multiple versions of the chassis.  

---

### ⚙️ Tinkercad (Circuit Prototyping & Simulation)  
Before moving into PCB manufacturing, we used Tinkercad’s easy-to-use **circuit simulator** to prototype the wiring of sensors, motors, and LEDs. This was especially useful during the early stages of development to quickly validate logic, check pinouts, and test simple behaviors without needing to solder or breadboard everything. While limited compared to professional EDA software, Tinkercad gave us a fast way to visualize and debug small subsystems before moving to a full schematic.  

---

### ⚙️ KiCad (PCB Design & Schematic Capture)  
KiCad was the main software used to design our **custom PCB**. We created full schematics for power management, motor drivers, and signal routing, then laid out the PCB with proper traces, vias, and ground planes. KiCad’s ERC (Electrical Rule Check) and DRC (Design Rule Check) ensured that our design was valid before manufacturing. The ability to generate **Gerber files** directly from KiCad made it easy to send our board for fabrication. Over time, we revised multiple PCB versions in KiCad, improving power regulation and simplifying wiring complexity with each iteration.  

---

### ⚙️ Raspberry Pi OS & Setup Tools  
For the main controller, we used **Raspberry Pi OS** on both Raspberry Pi 4B and Raspberry Pi 5. The OS was set up with Python libraries such as OpenCV, RPi.GPIO, smbus2 (for I²C communication with sensors like the MPU-6050), and pyserial for UART. We configured **crontab** and **systemd services** for startup automation, although we faced issues with Pi 5 where startup scripts wouldn’t execute properly. We also installed development tools such as `git`, `pip`, and `ssh` for remote management. The OS environment provided a stable platform to integrate sensing, motor control, and computer vision tasks.  

---
---

### ⚙️ Python (Core Robotics Control)  
Python served as the **primary programming language** for the project. We used it for motor control logic, servo positioning, sensor data processing, and integrating LiDAR input with navigation algorithms. Libraries like **OpenCV** were critical for handling camera input, while **matplotlib** was used during experiments to visualize sensor data. Python scripts were also linked with the PCB’s power logic and motor drivers to allow for full software-based control.  

---

### ⚙️ OpenCV (Computer Vision)  
OpenCV was employed for image capture and processing from the SJCAM (in PC camera mode) and later integrated into navigation routines. It enabled real-time frame acquisition, preprocessing (grayscale conversion, edge detection), and served as the foundation for potential object detection tasks. Even though the final implementation leaned more on LiDAR for reliable mapping, OpenCV gave us the framework to expand into visual-based navigation if needed.  

---

### ⚙️ GitHub (Version Control & Collaboration)  
All project files — from code and schematics to models and reports — were maintained in a **GitHub repository**. This ensured that every iteration was tracked through commits, and multiple collaborators could work on the same project without conflicts. GitHub Actions also gave us CI/CD capability, and the README served as the central documentation hub for all hardware and software.  

---

### ⚙️ Additional Tools & Utilities  
- **VS Code**: Main IDE for Python and embedded development, with extensions for Git integration.  
- **Inkscape / Figma**: For creating diagrams, flowcharts, and refining visuals for the README.  
- **CoolTerm / Serial Monitor**: For debugging UART communication with microcontrollers.  
- **Jupyter Notebooks**: Used during experiments to log and visualize data from sensors.  

---

## 🧩 Summary  
This stack of tools allowed us to cover every aspect of the robot: **Onshape and Tinkercad for physical and virtual prototyping, KiCad for electronics design, Raspberry Pi OS and Arduino IDE for firmware, Python and OpenCV for intelligence, and GitHub for collaboration**. Each tool played a specific role in ensuring that our design was not only functional but also well-documented and reproducible.  

