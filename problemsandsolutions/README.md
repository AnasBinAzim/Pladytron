# Problems Faced and Solutions Implemented :
1. One of the first challenges we encountered was with the SJCAM C200 action camera. Our goal was to use it as the primary vision system for the robot, automatically starting up in action camera mode at power-on so that it could immediately begin capturing video. However, the camera’s firmware design posed a significant obstacle: in order to activate recording mode, the user is required to press two buttons in sequence. Since our robot’s physical interface only allows automation of a single power or trigger button, this created a serious limitation. In a robotics application where everything should initialize seamlessly on startup, having to manually press multiple buttons was simply not acceptable. After repeated trials and attempts to work around this behavior, it became clear that the SJCAM C200 could not meet our requirements in its default form.
The solution was drastic but effective: we removed the action camera role entirely and repurposed the device to function strictly as a PC camera on startup. By rewiring the system and bypassing the dual-button activation sequence, we ensured that the camera would automatically initialize in webcam mode as soon as power was applied. This change eliminated the need for manual intervention and brought the system into alignment with the principle of full automation. Although it meant giving up native onboard recording features, the trade-off was worthwhile because it provided reliable, hands-free video capture directly integrated with the rest of the robot’s processing pipeline. This decision not only streamlined startup but also reduced potential points of failure in field deployment.

# CAMERA BEFORE AND AFTER :



| **Before (SJCAM C200 Action Camera Mode)** | **After (Rewired for Auto PC Camera Mode)** |
|---------------------------------------------|---------------------------------------------|
|<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/9dba0dc6-bd10-484f-b9a8-f090cf1020c0" /> | <img width="202" height="321" alt="image" src="https://github.com/user-attachments/assets/09362b7b-ded8-45f0-9df3-c3d53b894797" />|



2. A second major issue arose from our initial reliance on ultrasonic sonar sensors for distance measurement and obstacle detection. Sonar modules are attractive because they are inexpensive, lightweight, and widely available. However, during testing we discovered several critical shortcomings. Low-cost sonar sensors proved to be highly unreliable, with inconsistent readings that were easily disrupted by soft materials, angled surfaces, or environmental noise. Furthermore, using multiple sonar units in parallel introduced cross-interference, leading to false echoes and data corruption. The wiring complexity increased with each additional module, and integrating them into the PCB led to higher chances of error, noise coupling, and troubleshooting overhead. For a robot that demands precision, these limitations quickly became unacceptable.
To address this, we transitioned from sonar sensors to a LiDAR-based solution. Unlike sonar, LiDAR provides much greater coverage with a single sensor, reducing both hardware complexity and software overhead. With LiDAR, the robot was able to generate accurate distance measurements over a wide field of view, allowing it to map its environment with higher confidence and fewer blind spots. This not only simplified the PCB layout by removing multiple unreliable sonar channels but also improved system reliability by eliminating the issues of echo interference and inconsistent readings. The result was a cleaner, more efficient sensing system that required less debugging while dramatically improving environmental awareness and navigation capabilities.
Together, these problem-solving decisions reflect the iterative engineering process behind the robot. Each limitation encountered — from the camera’s startup logic to the sonar sensor unreliability — forced us to rethink the design and implement more robust alternatives. By replacing manual-dependent hardware with automated solutions and swapping error-prone sensors for advanced LiDAR technology, we made the robot more reliable, maintainable, and capable of performing in real-world conditions.
<img width="960" height="1092" alt="image" src="https://github.com/user-attachments/assets/38ceee90-687d-409c-8e0a-09ea321bbc57" />






---
---


Another major advantage is range and density of data. Cheap sonar sensors typically measure reliably only within 2–4 meters, and often with wide, imprecise beams that blur object edges. The RPLIDAR C1, on the other hand, provides coverage up to 12 meters with thousands of distance points per second, creating a detailed map of the robot’s environment. This higher density of data not only improves navigation but also enables advanced behaviors such as path planning, obstacle avoidance, and dynamic re-routing in real time. For robotics projects that require autonomy and reliability, these differences are critical.
Finally, the use of RPLIDAR reduces design complexity. Instead of wiring and calibrating multiple sonar units, the robot only needs a single LiDAR sensor connected via USB or UART. This simplifies the PCB layout, minimizes error sources, and improves overall system reliability. While the upfront cost of RPLIDAR C1 is higher than a set of cheap sonars, the trade-off in performance, reliability, and maintainability makes it a far better choice for serious robotics applications.
In summary, while sonar sensors are useful for very simple distance measurements, they quickly become a bottleneck in robotics projects due to unreliability and complexity. The RPLIDAR C1 provides accurate, wide-range, 360° scanning with minimal wiring and maximum reliability, making it vastly superior for autonomous navigation and mapping in our robot.

---

3. # Raspberry pi 5 startup issue:
   One of the most frustrating challenges we faced during development was with the Raspberry Pi 5. Our intention was to use the Pi 5 as the main controller for the robot since it offers more processing power, faster I/O, and overall better hardware capabilities compared to the Pi 4. However, despite its advantages, we ran into a critical issue: we could not get our startup automation to work properly on the Pi 5.
We initially configured crontab (@reboot) entries to run our control scripts automatically as soon as the Pi booted. This is a standard and reliable method that works flawlessly on earlier Raspberry Pi models, including the Pi 3 and Pi 4. Unfortunately, on the Pi 5, the scripts would not execute at startup no matter how many times we adjusted the configuration. We tested different approaches:
Using crontab -e with the @reboot directive.
Adding startup commands to rc.local.
Creating and enabling systemd service files to ensure the scripts launched during the boot sequence.
Testing both root-level and user-level crontab entries.
Delaying script execution with sleep commands in case the services were loading too early.
Despite all these attempts, the Pi 5 consistently refused to launch the scripts on startup. The behavior was puzzling because manual execution of the same scripts after boot worked perfectly, proving that the problem was tied specifically to the initialization process. To rule out OS-related issues, we tried multiple operating system images, including Raspberry Pi OS Lite, Raspberry Pi OS with desktop, and even different kernel updates. Each attempt produced the same result: startup automation simply failed on the Pi 5.
After spending significant time troubleshooting, we made the decision to switch back to the Raspberry Pi 4B, which has a well-tested ecosystem. On the Pi 4, crontab worked immediately without any issues, and our scripts ran at startup exactly as expected. This confirmed that the problem was not with our code or configuration, but likely with the Raspberry Pi 5’s still-evolving software support or OS compatibility at the time of testing. While the Pi 5 hardware is superior, the lack of reliable startup automation meant it was not viable for this project, where seamless initialization is critical for autonomous operation.
In the end, moving to the Pi 4B provided stability and reliability, even if it meant sacrificing some of the performance gains of the Pi 5. For robotics, dependability during startup proved to be far more important than raw computing power, and until Raspberry Pi OS matures further for the Pi 5, the Pi 4 remains the safer and more practical choice.
<img width="661" height="427" alt="image" src="https://github.com/user-attachments/assets/48f6173f-8697-4f6b-b2ba-afecb2e0a870" />

