import time
from utility import clamp, map_range, steer  # Import utility functions for clamping, mapping values, and steering the servo
from line_checks import coords, linearity, are_perpendicular, get_intersection  # Import geometric functions for line checks and intersections
from servo import Servo  # Import Servo control class
from lidar_reader import LidarReader  # Import LidarReader for reading Lidar sensor data
from motor import Motor  # Import Motor control class
import numpy as np  # Import numpy for array handling and calculations
from scipy.stats import linregress, false_discovery_control  # Import statistical functions (though only `linregress` is used)
from shapely.geometry import Point, Polygon  # Import for geometric operations and handling polygons
import pigpio  # Import the pigpio library for GPIO control

pi = pigpio.pi()  # Initialize pigpio instance for controlling GPIO pins
lidar = LidarReader(path="/home/wro/rplidar_sdk/output/Linux/Release/ultra_simple")  # Initialize LidarReader
servo = Servo(4)  # Initialize Servo on pin 4
motor = Motor(pi)  # Initialize motor with pigpio instance

# Constants for wall distances and directions
rwall = 0
lwall = 0
direction = 0
err = 22  # Error margin for distance calculations
f = 0
checker = 13  # Angle check increment
last_time = -100  # Variable to store the last time for periodic actions

# Define angle groups for Lidar data
angle_groups = {
    "front": [356, 357, 358, 359, 0, 1, 2, 3, 4],
    "right": [86, 88, 90, 92, 94],
    "left": [266, 268, 270, 272, 274]
}

# Main loop that continues until both right and left walls are detected
while True:
    if rwall and lwall:
        break
    rwall = lidar.get(90)  # Get right wall distance from Lidar
    lwall = lidar.get(270)  # Get left wall distance from Lidar

# Decide which wall to follow based on which is closer
if rwall <= lwall:
    follow_ang = 65  # Follow the right wall
    corner_ang = 270  # Corner angle for turning
    print("following right wall")
elif lwall < rwall:
    follow_ang = 295  # Follow the left wall
    corner_ang = 90  # Corner angle for turning
    print("following left wall")

corner = 0  # Initialize corner counter
fwall_init = lidar.get(0)  # Get initial front distance
center_dist = lidar.get(follow_ang)  # Get center distance based on follow angle
min_dist = 100  # Minimum distance threshold
max_dist = (2 * center_dist) - min_dist  # Maximum distance threshold
print(f"rwall={rwall} lwall={lwall} center={center_dist} max_dist={max_dist}")
time.sleep(3)
motor.forward(255)  # Move forward at maximum speed

# Function to get Lidar data for specified angles
def get_lidar_points(angles):
    points = []
    for angle in angles:
        r = lidar.get(angle)
        x, y = coords(r, angle)  # Convert polar coordinates to Cartesian
        points.append([x, y])
    return np.array(points)

# Main loop for Lidar-based navigation
try:
    while True:
        print(direction)
        if direction == 0:
            num_groups = len(angle_groups)
            slopes = [None] * num_groups  # Initialize list for slopes (None for vertical lines)
            intercepts = [None] * num_groups
            R2_values = [None] * num_groups
            f = 1  # Flag for indicating if lines are valid
            cnt = 0
            print("start")
            for name, angs in angle_groups.items():
                pts = get_lidar_points(angs)  # Get points for the current group of angles
                is_line, slope, intercept, r2 = linearity(pts)  # Check if points form a line
                slopes[cnt] = slope
                intercepts[cnt] = intercept
                R2_values[cnt] = r2
                if not is_line:
                    f = 0  # If any group is not a line, set flag to 0
                cnt += 1
                if name == "left":
                    print(f, slope, intercept, pts)
                    for angee in angs:
                        print(lidar.get(angee))
                    print()

            # Check for perpendicular lines
            if f == 1:
                if not are_perpendicular(slopes[0], slopes[1]):
                    print("rejected Line")
                    f = 0
                if not are_perpendicular(slopes[0], slopes[2]):
                    print("rejected Line")
                    f = 0

            #
