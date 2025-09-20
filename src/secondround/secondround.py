import cv2 as cv  # Import OpenCV for image processing
import time  # Import time for delays and timing operations
import math  # Import math for mathematical operations
from utility import clamp, map_range, steer  # Import utility functions for clamping values, mapping ranges, and controlling the steering
from line_checks import coords, linearity, are_perpendicular, get_intersection, are_parallel, get_front_line, angle, get_yaw_diff, inside_polygon  # Import line check functions
from servo import Servo  # Import the Servo class for controlling servos
from lidar_reader import LidarReader  # Import LidarReader for handling LIDAR sensor data
from gyro_reader import GyroReader  # Import GyroReader for handling gyroscope data
from motor import Motor  # Import Motor class for controlling motors
import numpy as np  # Import numpy for numerical operations, particularly with arrays
from scipy.stats import linregress, false_discovery_control  # Import statistical functions
from line_plotter import line_show, point_show  # Import line plotting functions
from shapely.geometry import Point, Polygon  # Import Shapely for geometric operations
import pigpio  # Import pigpio for controlling Raspberry Pi GPIO pins
from button import Button  # Import Button class for handling button inputs
from camera_reader import CameraReader  # Import CameraReader class for reading camera frames

default_speed = 165  # Default speed setting for the robot

# Object constants
max_width = 80  # Maximum acceptable width for objects
max_x_delta_change = 177  # Maximum change in x-coordinate for objects
delta_change_ratio = 0.9  # Ratio for delta change in object positions
steering_value = 0  # Initial steering value
steering_limit = 75  # Maximum limit for steering value
obj_steer_err = 20  # Error margin for steering with respect to objects
width_for_constant_distance = 9  # Minimum acceptable width for constant distance detection
minimum_y_for_object = 10  # Minimum y-coordinate for valid object detection
band_height = 300  # Height of the band for object detection
minimum_width_for_object = 28  # Minimum width for valid object detection
obj_steer_boundary = 150  # Boundary for steering based on object distance
obj_steer_limit = 120  # Maximum limit for steering based on objects

# Initialize state variables
last_obj = 0  # Last object detected
last_obj_timer = 1.25  # Timer for last object detection
last_obj_found = -100  # Time when last object was found

direction = 0  # Direction flag (e.g., left or right)
col_flag = 0  # Collision flag (detecting collision)
col_timer = 3.2  # Collision detection timeout
col_yaw_timer = 1  # Yaw change detection timeout
col_yaw_risk_timer = 3.56  # Risk detection timeout for yaw
col_last_timer = -100  # Last time a collision was detected
parking_timer = -100  # Parking timer
col_yaw_update_tolerance = 12  # Tolerance for yaw update during collision
is_col = 0  # Boolean flag for collision state
corner = 0  # Number of corners the robot has completed
lap_cnt = 1  # Number of laps completed
last_err = 0  # Last steering error
speed = 0  # Current speed of the robot

parking_end_flag = False  # Flag for parking end
parking_start_flag = True  # Flag for parking start
too_close = False  # Flag for detecting if an object is too close

too_close_timer = 0  # Timer for too-close state
side_risk_dist = 185  # Side risk distance for avoiding obstacles

# Global variables for object detection boundaries
erre = 40
minimum_x_for_object = 100
maximum_x_for_object = 600
minimum_y_for_object = 230
maximum_y_for_object = 290
minimum_x_for_line = 200
maximum_x_for_line = 440
minimum_y_for_line = 330
maximum_y_for_line = 255

# Exclusion sets for object detection based on color
exclusion_sets = {
    0: (),  # No exclusions for color 0 (blue)
    1: (4,),  # Exclude color 4 (pink) for color 1 (orange)
    2: (),  # No exclusions for color 2 (green)
    3: (0, 1, 2, 4),  # Exclude colors 0 (blue), 1 (orange), 2 (green), and 4 (pink) for color 3 (red)
    4: (),  # No exclusions for color 4 (pink)
}

# First round setup for hardware components
pi = pigpio.pi()  # Initialize the pigpio library for GPIO control
lidar = LidarReader(path="/home/wro/rplidar_sdk/output/Linux/Release/ultra_simple")  # Initialize LIDAR sensor
gyro = GyroReader(freq=60.0)  # Initialize Gyroscope reader with frequency of 60 Hz
servo = Servo(4)  # Initialize the Servo object for controlling the servo on pin 4
cam_reader = CameraReader(pi, cam_pins=(20, 21), width=640, height=480)  # Initialize CameraReader for reading from camera
motor = Motor(pi)  # Initialize Motor object for controlling the robot's motors
btn = Button(pi, 16)  # Initialize Button object for handling button input on GPIO pin 16

LED_PIN = 9  # Define the pin number for the LED

# Set up the LED pin for output and initialize it to off
pi.set_mode(LED_PIN, pigpio.OUTPUT)
pi.write(LED_PIN, 0)

# Read initial LIDAR values for right and left walls
rwall = None
lwall = None
while rwall is None or lwall is None or lwall == 0 or rwall == 0:
    rwall = lidar.get(150)  # Get LIDAR reading at 150 degrees (right wall)
    lwall = lidar.get(30)   # Get LIDAR reading at 30 degrees (left wall)

print(f"rwall={rwall} lwall={lwall}")

# Function to load HSV color ranges from a file
def load_hsv_ranges(filename):
    hsv_ranges = []  # List to store HSV ranges
    with open(filename, 'r') as f:  # Open the file for reading
        for line in f:  # Read each line in the file
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or line.startswith('#'):  # Skip empty or comment lines
                continue
            parts = line.split(',')  # Split the line by commas
            if len(parts) != 6:  # Check if the line has exactly 6 parts
                print(f"?? Skipping invalid line: {line}")
                continue
            hsv_range = list(map(int, parts))  # Convert the parts to integers
            hsv_ranges.append(hsv_range)  # Add the HSV range to the list
    return hsv_ranges  # Return the list of HSV ranges

# Load all HSV ranges from the file
all_hsv_ranges = load_hsv_ranges('hsv_values.txt')

# Select only lines 3 and 4 (index 2 and 3) from the HSV ranges
if len(all_hsv_ranges) < 4:
    print("? hsv_ranges.txt file must have at least 4 lines with valid HSV ranges.")
    exit()

# Define object and line HSV ranges based on the loaded values
object_hsv_list = [all_hsv_ranges[2], all_hsv_ranges[3]]
line_hsv_list = [all_hsv_ranges[0], all_hsv_ranges[1]]

# Define object colors in BGR format (for OpenCV)
object_colors = [
    (255, 0, 0),     # Blue
    (0, 165, 255),   # Orange
    (0, 255, 0),     # Green
    (0, 0, 255),     # Red
    (255, 0, 255)    # Pink (magenta)
]

# Resize masks helper function (to adjust mask size for frame dimensions)
def resize_mask(mask, width, height):
    return cv.resize(mask, (width, height), interpolation=cv.INTER_NEAREST)

# Function to get contours from a frame based on selected HSV range
def getContours(frame, current_index, draw_color):
    global all_hsv_ranges, exclusion_sets

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert frame to HSV color space

    # Start with full mask (everything allowed initially)
    mask = np.ones(hsv.shape[:2], dtype=np.uint8) * 255

    # Apply exclusions first (exclude certain colors based on the exclusion sets)
    if current_index in exclusion_sets:
        for idx in exclusion_sets[current_index]:
            lower_ex = np.array(all_hsv_ranges[idx][:3])
            upper_ex = np.array(all_hsv_ranges[idx][3:])
            exclusion_mask = cv.inRange(hsv, lower_ex, upper_ex)
            mask[exclusion_mask > 0] = 0  # Black out excluded pixels

    # Apply the selected HSV range for the current object
    lower = np.array(all_hsv_ranges[current_index][:3])
    upper = np.array(all_hsv_ranges[current_index][3:])
    selected_mask = cv.inRange(hsv, lower, upper)

    # Keep only pixels that are in both the allowed area and the selected range
    mask = cv.bitwise_and(selected_mask, mask)
    if current_index == 0:  # If the index is for the blue object, show the mask
        cv.imshow("blue", mask)
    if current_index == 1:  # If the index is for the orange object, show the mask
        cv.imshow("orange", mask)

    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    list = []

    for cnt in contours:  # Iterate through each contour found
        area = cv.contourArea(cnt)  # Calculate the area of the contour
        if area > 100:  # Only process contours with area greater than 100
            peri = cv.arcLength(cnt, True)  # Calculate the perimeter of the contour
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)  # Approximate the contour to a polygon
            x, y, w, h = cv.boundingRect(approx)  # Get the bounding rectangle for the contour
            x = int(x + w / 2)  # Calculate the center x-coordinate
            y = int(y + h / 2)  # Calculate the center y-coordinate

            rect = [x, y, w, h]  # Create a list with bounding box information
            if y > minimum_y_for_object:  # Only include objects below the minimum y threshold
                cv.circle(frame, (x, y), 6, draw_color, -1)  # Draw a circle at the center of the object
                list.append(rect)  # Add the object to the list

    return list  # Return the list of detected objects

# Function to get the middle portion of the frame based on y-coordinates
def get_middle_frame(frame):
    mask_pts = np.array([[0, minimum_y_for_object], [640, minimum_y_for_object], [640, maximum_y_for_object + erre], [0, maximum_y_for_object + erre]], np.int32)
    mask = np.zeros((480, 640), dtype=np.uint8)  # Create a mask for the specified region
    cv.fillPoly(mask, [mask_pts], 255)  # Fill the polygon defined by mask_pts with white
    frame = cv.bitwise_and(frame, frame, mask=mask)  # Apply the mask to the frame
    return frame  # Return the cropped frame

yaw = gyro.get_yaw()  # Get the initial yaw (orientation) from the gyroscope
true_yaw = yaw  # Initialize true_yaw as the same as the initial yaw
which_obj = 0  # Flag to track which object is being followed

# Function to handle the end of the parking process
def parking_end():
    global direction, yaw, true_yaw
    motor.go(130)  # Move the motor forward at speed 130
    while lidar.get(90) > 300:  # Check LIDAR data at 90 degrees (front)
        yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        result = get_yaw_diff(true_yaw, yaw)  # Calculate the difference between true_yaw and current yaw
        result = clamp(result, -75, 75)  # Clamp the result within the steering limits
        result = map_range(result, -75, 75, -75, 75)  # Map the result to the steering range
        steer(servo, result)  # Adjust the steering to the calculated value
    motor.go(-130)  # Move the motor backward after parking
    print("first step done")
    if direction == 1:  # If the direction is 1 (left)
        true_yaw -= 90  # Adjust the true yaw by 90 degrees
        true_yaw += 360  # Add 360 to handle negative values
        true_yaw %= 360  # Ensure true_yaw stays within 0-360 degrees
    else:  # If the direction is not 1, assume it's the opposite direction (right)
        true_yaw += 90  # Adjust the true yaw by 90 degrees
        true_yaw += 360  # Add 360 to handle negative values
        true_yaw %= 360  # Ensure true_yaw stays within 0-360 degrees
        
    print(f"ya: {yaw}, true_yaw:{true_yaw}, diff:{abs(get_yaw_diff(true_yaw, yaw))}")  # Print the yaw values and their difference
    while abs(get_yaw_diff(true_yaw, yaw)) >= 7:  # If yaw difference is greater than 7 degrees
        yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        result = get_yaw_diff(true_yaw, yaw)  # Calculate the yaw difference
        result = clamp(result, -75, 75)  # Clamp the result within the steering limits
        result = -map_range(result, -75, 75, -75, 75)  # Map the result to the steering range and invert it
        steer(servo, result)  # Adjust the steering to the calculated value
        print(f"restult = {result}")  # Print the steering result
    motor.go(130)  # Move the motor forward at speed 130
    while lidar.get(90) > 600:  # Keep moving until the LIDAR detects a distance greater than 600
        yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        result = get_yaw_diff(true_yaw, yaw)  # Calculate the yaw difference
        result = map_range(result, -20, 20, -75, 75)  # Map the result to the steering range
        steer(servo, result)  # Adjust the steering to the calculated value
    if direction == 1:  # If the direction is 1 (left)
        true_yaw -= 90  # Adjust the true yaw by 90 degrees
        true_yaw += 360  # Add 360 to handle negative values
        true_yaw %= 360  # Ensure true_yaw stays within 0-360 degrees
    else:  # If the direction is not 1, assume it's the opposite direction (right)
        true_yaw += 90  # Adjust the true yaw by 90 degrees
        true_yaw += 360  # Add 360 to handle negative values
        true_yaw %= 360  # Ensure true_yaw stays within 0-360 degrees
    while abs(get_yaw_diff(true_yaw, yaw)) >= 20:  # If yaw difference is greater than 20 degrees
        yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        result = get_yaw_diff(true_yaw, yaw)  # Calculate the yaw difference
        result = clamp(result, -75, 75)  # Clamp the result within the steering limits
        result = map_range(result, -75, 75, -75, 75)  # Map the result to the steering range
        steer(servo, result)  # Adjust the steering to the calculated value
        print(f"restult = {result}")  # Print the steering result

    while True:  # Start the continuous loop
        if direction == 2:  # If direction is 2 (right wall)
            rwall = lidar.get(180)  # Get LIDAR reading at 180 degrees (right wall)
            steering_value = map_range(rwall, 300, 500, -65, 65)  # Map the LIDAR reading to steering value
            steer(servo, steering_value)  # Adjust the steering to the calculated value
            print("following right wall")  # Print that the robot is following the right wall
            yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        elif direction == 1:  # If direction is 1 (left wall)
            rwall = lidar.get(0)  # Get LIDAR reading at 0 degrees (left wall)
            steering_value = -map_range(rwall, 300, 500, -65, 65)  # Map the LIDAR reading to steering value (inverted)
            steer(servo, steering_value)  # Adjust the steering to the calculated value
            print("following left wall")  # Print that the robot is following the left wall
        if abs(get_yaw_diff(true_yaw, yaw)) < 5:  # If yaw difference is less than 5 degrees
            break  # Break the loop when the yaw difference is small enough
    parking_timer = 1000  # Set parking timer to 1000
    while True:  # Start the continuous loop
        ret, frame9 = cam.read()  # Read a frame from the camera
        if not ret:  # If frame is not successfully captured
            print("? Failed to grab frame.")  # Print an error message
            break  # Exit the loop if the frame capture fails
        frame9 = get_middle_frame(frame9)  # Get the middle portion of the frame
        cv.imshow("parking", frame9)  # Show the frame in the "parking" window
        hisab = getContours(frame9, 4, object_colors[4])  # Get contours for the frame with a specific color
        yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        result = get_yaw_diff(true_yaw, yaw)  # Calculate the yaw difference
        result = clamp(result, -75, 75)  # Clamp the result within the steering limits
        result = map_range(result, -30, 30, -75, 75)  # Map the result to the steering range
        steer(servo, result)  # Adjust the steering to the calculated value
        if len(hisab) == 0:  # If no contours are found
            break  # Exit the loop if no objects are detected

    motor.stop()  # Stop the motor after parking is complete
    time.sleep(30)  # Wait for 30 seconds before exiting
    exit()  # Exit the program

def last_parking():
    global direction, yaw, true_yaw
    # This function is meant for handling last parking actions, but it is not defined yet

def start_from_parking(d):
    global yaw, true_yaw

    motor.go(-60)  # Move the motor backward at speed -60
    while lidar.get(270) > 160:  # Continue moving until LIDAR detects a distance less than 160 at 270 degrees (back)
        print(f"backwall={lidar.get(270)}")  # Print the back wall distance
    motor.stop()  # Stop the motor

    if d == 'L':  # If direction is left
        steer(servo, 75)  # Steer the robot left
        motor.go(100)  # Move the motor forward at speed 100
        while get_yaw_diff(true_yaw, yaw) > -30:  # If yaw difference is greater than -30 degrees
            yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        while get_yaw_diff(true_yaw, yaw) > -60:  # If yaw difference is greater than -60 degrees
            yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
            print(f"true_yaw = {true_yaw}, yaw = {yaw}")  # Print the yaw values
    else:  # If direction is not left (right direction)
        steer(servo, -75)  # Steer the robot right
        motor.go(100)  # Move the motor forward at speed 100
        while get_yaw_diff(true_yaw, yaw) < 30:  # If yaw difference is less than 30 degrees
            yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
        while get_yaw_diff(true_yaw, yaw) < 60:  # If yaw difference is less than 60 degrees
            yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
    steer(servo, 0)  # Set the steering to 0 (straight)
    motor.go(speed)  # Move the motor forward at the set speed
    time.sleep(0.25)  # Wait for 0.25 seconds

prev_btn_state = 1  # Initialize the previous button state
btn_cnt = 0  # Initialize the button press count
status = 0  # Initialize the robot status
yaw_cnt = 0  # Initialize the yaw counter
pi.write(LED_PIN, 1)  # Turn the LED on
parking = 0  # Initialize parking flag

# Main loop
while True:
    state = btn.state()  # Get the current button state
    yaw = gyro.get_yaw()  # Get the current yaw from the gyroscope
    if state == 1 and prev_btn_state == 0:  # If button is pressed
        print("Button pressed")  # Print a message when the button is pressed
        btn_cnt += 1  # Increment the button press count
        corner = 0  # Reset corner count
        direction = 0  # Reset direction
        yaw_cnt = 0  # Reset yaw counter
        true_yaw = yaw  # Reset true_yaw to the current yaw
        col_last_timer = -100  # Reset collision timer
        parking_timer = -100  # Reset parking timer
        too_close_timer = -100  # Reset too-close timer
        if (btn_cnt % 2) == 1 and parking_start_flag is True:  # If button pressed an odd number of times and parking is allowed
            steer(servo, 0)  # Set steering to 0 (straight)
            print("pressed")
            time.sleep(1)  # Wait for 1 second
            if lidar.get(0) < 200:  # If left-side LIDAR detects an object closer than 200
                start_from_parking('L')  # Start parking from the left
            elif lidar.get(180) < 200:  # If right-side LIDAR detects an object closer than 200
                start_from_parking('R')  # Start parking from the right
        if speed > 0:  # If speed is greater than 0
            status = 0  # Set status to 0
            speed = 0  # Stop the motor by setting speed to 0
            pi.write(LED_PIN, 1)  # Turn the LED on
        else:
            status = 1  # Set status to 1
            speed = default_speed  # Set speed to default speed
            pi.write(LED_PIN, 0)  # Turn the LED off
    if btn_cnt >= 8:  # If button has been pressed 8 or more times
        print("Stopping LIDAR and motors...")  # Print message indicating the stopping of the robot
        lidar.stop()  # Stop the LIDAR sensor
        motor.stop()  # Stop the motors
        servo.stop()  # Stop the servo
        break  # Exit the loop
    
    prev_btn_state = state  # Update previous button state
    motor.go(speed)  # Move the motor at the current speed
    fwall = lidar.get(0)  # Get LIDAR reading at 0 degrees (front)
    if corner >= lap_cnt:  # If corner count reaches lap count
        if parking_end_flag == True:  # If parking has ended
            parking_end()  # Call the parking end function
        print("1")
        speed = 0  # Stop the robot by setting speed to 0

    frame = cam_reader.get_frame()  # Capture a frame from the camera
    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:  # If the frame is valid
        cv.imshow("Raw Frame", frame)  # Display the raw frame
    else:
        print("?? No valid frame yet...")  # Print a message if no valid frame is captured
        continue  # Skip the rest of the loop and continue to the next iteration
    
    if col_flag == 1 and time.perf_counter() - col_last_timer > col_yaw_timer:  # If collision flag is 1 and collision timer expired
        col_flag = 2  # Change collision flag to 2
        pi.write(LED_PIN, 0)  # Turn the LED off
        yaw_cnt += 1  # Increment the yaw counter
        if direction == 1:  # If direction is 1 (left)
            true_yaw += 90  # Adjust the true yaw by 90 degrees
            true_yaw += 360  # Add 360 to handle negative values
            true_yaw %= 360  # Ensure true_yaw stays within 0-360 degrees
        elif direction == 2:  # If direction is 2 (right)
            true_yaw -= 90  # Adjust the true yaw by 90 degrees
            true_yaw += 360  # Add 360 to handle negative values
            true_yaw %= 360  # Ensure true_yaw stays within 0-360 degrees
    elif col_flag == 2 and time.perf_counter() - col_last_timer > col_timer:  # If collision flag is 2 and collision timer expired
        col_flag = 0  # Reset collision flag to 0
        corner += 1  # Increment the corner count
    elif col_flag == 0 and corner < lap_cnt:  # If no collision and lap is not complete
        blue = 0  # Reset blue object flag
        orange = 0  # Reset orange object flag
        mask_pts = np.array([[minimum_x_for_line, minimum_y_for_line], [maximum_x_for_line, minimum_y_for_line], [maximum_x_for_line, 480], [minimum_x_for_line, 480]], np.int32)  # Define mask for the line
        mask = np.zeros((480, 640), dtype=np.uint8)  # Create a blank mask
        cv.fillPoly(mask, [mask_pts], 255)  # Fill the mask with white
        line_frame = cv.bitwise_and(frame, frame, mask=mask)  # Apply the mask to the frame
        cv.imshow("line", line_frame)  # Display the masked frame

        # Detect contours in the line frame
        hisab = []
        for i, hsv_range in enumerate(line_hsv_list):  # Loop through the line HSV ranges
            color = object_colors[i] if i < len(object_colors) else (255, 255, 255)  # Choose object color for drawing
            list_contours = getContours(line_frame, i, color)  # Get contours for the line
            for obj in list_contours:  # Iterate through detected objects
                hisab.append([-obj[1], obj[0], obj[2], i, obj[3]])  # Add object data to the list
        hisab.sort()  # Sort the objects based on position
        if len(hisab) > 0:  # If objects are detected
            x = hisab[0][1]  # Get x-coordinate of the first object
            y = -hisab[0][0]  # Get y-coordinate of the first object
            w = hisab[0][2]  # Get width of the first object
            h = hisab[0][4]  # Get height of the first object
            x1 = int(x - w / 2)  # Calculate top-left x-coordinate
            y1 = int(y - h / 2)  # Calculate top-left y-coordinate
            x2 = int(x + w / 2)  # Calculate bottom-right x-coordinate
            y2 = int(y + h / 2)  # Calculate bottom-right y-coordinate
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)  # Draw a bounding rectangle around the detected object
            print(f"x = {x}, y = {y}, w = {w}, h = {h}")  # Print object coordinates and size

            if hisab[0][3] == 0:  # If the object is green
                blue = 1  # Set blue flag to true
                if direction == 0:  # If no direction set yet
                    direction = 1  # Set direction to 1 (left)
            elif hisab[0][3] == 1:  # If the object is red
                orange = 1  # Set orange flag to true
                if direction == 0:  # If no direction set yet
                    direction = 2  # Set direction to 2 (right)
        if direction == 1 and blue == 1:  # If the direction is left and a blue object is detected
            col_flag = 1  # Set collision flag to 1
            pi.write(LED_PIN, 1)  # Turn the LED on
            col_last_timer = time.perf_counter()  # Reset the collision timer
        if direction == 2 and orange == 1:  # If the direction is right and an orange object is detected
            col_flag = 1  # Set collision flag to 1
            pi.write(LED_PIN, 1)  # Turn the LED on
            col_last_timer = time.perf_counter()  # Reset the collision timer

    # Further processing to track objects and steer the robot based on detected objects...
    # Process the middle section of the frame for object detection
    frame = get_middle_frame(frame)  # Crop the frame to focus on the middle section
    # Display the processed frame for visual inspection
    cv.imshow("Masks", hsv)  # Show the HSV image (for debugging purposes)

    # Loop through the object detection ranges to detect objects in the frame
    hisab = []
    for i, hsv_range in enumerate(object_hsv_list):  # Loop through object HSV ranges (Green and Red objects)
        color = object_colors[i + 2] if i + 2 < len(object_colors) else (255, 255, 255)  # Set the color for drawing
        list_contours = getContours(frame, i + 2, color)  # Get contours based on HSV range and color
        for obj in list_contours:  # Iterate over detected objects
            x = obj[0]  # Get x-coordinate of the detected object
            y = obj[1]  # Get y-coordinate of the detected object
            w = obj[2]  # Get width of the detected object
            h = obj[3]  # Get height of the detected object
            hisab.append([-(y + h / 2), x, y, i, w, h])  # Append object data to the list

    hisab.sort()  # Sort the objects based on their positions

    steering_value = 0  # Reset steering value to 0
    desired = 960  # Define desired value for object detection
    obj = False  # Initialize object flag
    obj_x = -1  # Initialize x-coordinate of the object
    which_obj = 0  # Initialize which object is being tracked (0 = none)
    last_obj = 0  # Initialize last object type (0 = none)

    # If objects are detected
    if len(hisab) > 0:
        x = hisab[0][1]  # Get the x-coordinate of the first object
        y = hisab[0][2]  # Get the y-coordinate of the first object
        bottom = -hisab[0][0]  # Get the bottom position of the object (inverted y-coordinate)
        w = hisab[0][4]  # Get the width of the first object
        h = hisab[0][5]  # Get the height of the first object

        # Calculate bounding box coordinates
        x1 = int(x - w / 2)  # Calculate the top-left x-coordinate
        y1 = int(y - h / 2)  # Calculate the top-left y-coordinate
        x2 = int(x + w / 2)  # Calculate the bottom-right x-coordinate
        y2 = int(y + h / 2)  # Calculate the bottom-right y-coordinate

        print(f"width = {w}, height = {h}")  # Print the width and height of the object

        # Check if the object is green (index 0) and meets the size and position criteria
        if hisab[0][3] == 0 and w >= minimum_width_for_object and y >= minimum_y_for_object and y <= maximum_y_for_object:
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)  # Draw a rectangle around the green object
            # Calculate steering adjustment based on width and x position of the object
            res1 = (w - minimum_width_for_object) / (max_width - minimum_width_for_object)
            res1 = clamp(res1, 0, 1.0)  # Clamp the result to the range [0, 1]
            res2 = (640 - 90 - x) / (640 - 90)  # Calculate the relative position of the object in the frame
            res2 = clamp(res2, 0, 1.0)  # Clamp the result to the range [0, 1]
            rest = res1 * res2  # Multiply the results for combined effect
            rest = math.sqrt(rest)  # Take the square root to reduce the effect
            rest = clamp(rest, 0, 1.0)  # Clamp the result to the range [0, 1]
            rest = rest ** 0.33  # Apply a power function for finer control
            rest = clamp(rest, 0, 1.0)  # Clamp again
            print(f"res1 = {res1}, res2 = {res2}, rest = {rest}")  # Print intermediate values for debugging
            # Adjust steering based on calculated value
            steering_value = 0 - (steering_limit * rest)
            if steering_value != 0:  # If steering value is not zero, mark object detected
                obj = True
            last_obj = 1  # Mark the object as green (index 1)
            last_obj_found = time.perf_counter()  # Update the last object found time
            if w >= 70:  # If the object is large enough, set obj_x to its x position
                obj_x = x
        # Check if the object is red (index 1) and meets the size and position criteria
        elif hisab[0][3] == 1 and w >= minimum_width_for_object and y >= minimum_y_for_object and y <= maximum_y_for_object:
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)  # Draw a rectangle around the red object
            # Calculate steering adjustment based on width and x position of the object
            res1 = (w - minimum_width_for_object) / (max_width - minimum_width_for_object)
            res1 = clamp(res1, 0, 1.0)  # Clamp the result to the range [0, 1]
            res2 = (x - 90) / (640 - 90)  # Calculate the relative position of the object in the frame
            res2 = clamp(res2, 0, 1.0)  # Clamp the result to the range [0, 1]
            rest = res1 * res2  # Multiply the results for combined effect
            rest = math.sqrt(rest)  # Take the square root to reduce the effect
            rest = clamp(rest, 0, 1.0)  # Clamp the result to the range [0, 1]
            rest = rest ** 0.33  # Apply a power function for finer control
            rest = clamp(rest, 0, 1.0)  # Clamp again
            print(f"res1 = {res1}, res2 = {res2}, rest = {rest}")  # Print intermediate values for debugging
            # Adjust steering based on calculated value
            steering_value = 0 + (steering_limit * rest)
            if steering_value != 0:  # If steering value is not zero, mark object detected
                obj = True
            last_obj = 2  # Mark the object as red (index 2)
            last_obj_found = time.perf_counter()  # Update the last object found time
            if w >= 70:  # If the object is large enough, set obj_x to its x position
                obj_x = x

    # Detect objects for parking
    hisab = getContours(frame, 4, object_colors[4])  # Get contours for parking object detection
    parking = 0  # Initialize parking flag
    if len(hisab) > 0:  # If parking objects are detected
        parking = 1  # Set parking flag to 1
        parking_timer = time.perf_counter()  # Set parking timer to current time

    # Handle movement and steering based on the object detected
    if obj is False and time.perf_counter() - last_obj_found <= last_obj_timer:
        res = clamp(get_yaw_diff(true_yaw, yaw), -63, 63)  # Calculate yaw difference and clamp it
        steering_value = map_range(res, -63, 63, -75, 75)  # Map the yaw difference to the steering range
        print(f"steering = {steering_value}, yaw diff = {get_yaw_diff(true_yaw, yaw)}")  # Print the steering value and yaw difference
    elif obj is False:  # If no object is detected
        res = 0  # Reset the result
        sm = 0  # Initialize sum
        for i in range(0, 180, 3):  # Loop through LIDAR angles from 0 to 180 degrees
            res += i * lidar.get(i)  # Sum the weighted distances
            sm += lidar.get(i)  # Sum the distances
        res /= sm  # Calculate the weighted average
        res = clamp(res, 0, 180)  # Clamp the result to the range [0, 180]
        steering_value = map_range(res, 25, 155, -65, 65)  # Map the result to the steering range

    err = steering_value  # Set the steering error to the current steering value
    if obj is True:  # If an object is detected
        steering_value = err * 1.19 + (err - last_err) * 0  # Apply proportional control for steering
    else:  # If no object is detected
        steering_value = err * 1.9 + (err - last_err) * 5  # Apply higher proportional control

    last_err = err  # Update the last error value

    # Additional safety checks for objects being too close
    if speed == 1 and too_close is False:
        for i in range(50, 130, 1):  # Check LIDAR data for objects within a certain range
            if inside_polygon(lidar.get(i), i) is True:  # If an object is too close
                too_close = True  # Set the too-close flag to true
                print("Too close True")
                pi.write(LED_PIN, 1)  # Turn the LED on
                speed = 0  # Stop the robot by setting speed to 0
                too_close_timer = time.perf_counter()  # Start the too-close timer
                break  # Exit the loop when an object is too close
    print(f"cnt = {yaw_cnt}, steer = {steering_value}, yaw = {yaw}, true_yaw = {true_yaw}, corner = {corner}")  # Print debug information
    cv.putText(frame, f"Steering: {steering_value}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)  # Display the steering value on the frame

    steering_value = clamp(steering_value, -75, 75)  # Clamp the steering value to the range [-75, 75]
    steer(servo, steering_value)  # Adjust the servo based on the steering value
    cv.imshow("frame", frame)  # Display the frame with the object detection and steering visualizations

    # Exit condition for the loop (e.g., pressing a key)
    if cv.waitKey(1) & 0xFF == ord('p'):  # If 'p' is pressed
        break  # Exit the loop

# Cleanup after the main loop ends
cam.release()  # Release the camera
cv.destroyAllWindows()  # Close all OpenCV windows
motor.stop()  # Stop the motor
