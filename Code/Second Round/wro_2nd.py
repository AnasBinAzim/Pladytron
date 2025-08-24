import cv2 as cv
import time
from utility import clamp, map_range, steer
from line_checks import coords, linearity, are_perpendicular, get_intersection, are_parallel, get_front_line,angle
from servo import Servo
from lidar_reader import LidarReader
from motor import Motor
import numpy as np
from scipy.stats import linregress, false_discovery_control
from line_plotter import line_show,point_show
from shapely.geometry import Point, Polygon
import pigpio

# constants
steering_value = 90
width_for_constant_distance = 9  # minimum acceptable width
minimum_y_for_object = 360
x_boundary_for_red = 360
x_boundary_for_green = 920
band_height = 470

# first round part
pi = pigpio.pi()
lidar = LidarReader(path="/home/wro/rplidar_sdk/output/Linux/Release/ultra_simple")
servo = Servo(4)
motor = Motor(pi)

rwall = None
lwall = None
while rwall is None or lwall is None or lwall == 0 or rwall == 0:
    rwall = lidar.get(60)   # right side wall
    lwall = lidar.get(300)  # left wall
print(f"rwall={rwall} lwall={lwall}")
corner=0
last_err=0
time.sleep(3)
motor.forward(220)  # forward

# --- Function to read HSV ranges from a txt file ---
def load_hsv_ranges(filename):
    hsv_ranges = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # skip empty or comment lines
            parts = line.split(',')
            if len(parts) != 6:
                print(f"?? Skipping invalid line: {line}")
                continue
            hsv_range = list(map(int, parts))
            hsv_ranges.append(hsv_range)
    return hsv_ranges

# --- Load all HSV ranges from the file ---
all_hsv_ranges = load_hsv_ranges('hsv_values.txt')

# --- Select only lines 3 and 4 (index 2 and 3) ---
if len(all_hsv_ranges) < 4:
    print("? hsv_ranges.txt file must have at least 4 lines with valid HSV ranges.")
    exit()

object_hsv_list = [all_hsv_ranges[2], all_hsv_ranges[3]]

object_colors = [
    (0, 255, 0),   # Green
    (0, 0, 255)    # Red
]

# --- Open any camera from index 0 to 9 ---
for cam_index in range(10):
    cam = cv.VideoCapture(cam_index)
    cam.set(3, 1280)
    cam.set(4, 720)
    if cam.isOpened():
        print(f"? Camera opened at index {cam_index}")
        break
    cam.release()
else:
    print("? No working camera found.")
    exit()

# --- Resize masks helper ---
def resize_mask(mask, width, height):
    return cv.resize(mask, (width, height), interpolation=cv.INTER_NEAREST)

def getContours(mask, frame, draw_color, label):
    contours, meow = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    list = []
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 220:
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv.boundingRect(approx)
            x = int(x + w / 2)
            y = int(y + h / 2)
            if w > h:
                w,h = h,w
            rect = [x, y, w, h]
            if y > minimum_y_for_object:
                cv.circle(frame, (x, y), 6, draw_color, -1)
                list.append(rect)
    return list

def get_middle_frame(frame):    
    if not ret:
        return None
    
    h, w = frame.shape[:2]
    start_y = (h - band_height) // 2
    end_y = start_y + band_height
    
    # Crop middle band only
    cropped = frame[start_y:end_y, :]
    return cropped

# --- Main loop ---
while True:
    ret, frame = cam.read()
    frame = get_middle_frame(frame)
    if not ret:
        print("? Failed to grab frame.")
        break
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # cv.imshow("Masks", hsv)
    masks = []
    hisab = []
    for i, hsv_range in enumerate(object_hsv_list):
        lower = np.array(hsv_range[:3])
        upper = np.array(hsv_range[3:])
        mask = cv.inRange(hsv, lower, upper)
        color = object_colors[i] if i < len(object_colors) else (255, 255, 255)
        list_contours = getContours(mask, frame, color, f"Object {i+1}")
        for obj in list_contours:
            hisab.append([-obj[2],obj[0],obj[1],i,obj[3]])
        masks.append(mask)
    hisab.sort()
    steering_value = 90
    desired = 360
    if len(hisab) > 0:
        x = hisab[0][1]
        y = hisab[0][2]
        w = -hisab[0][0]
        h = hisab[0][4]
        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)
        cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
        if hisab[0][3] == 0:
            res = w / 180
            res = res * 360
            res = res ** 1.17
            desired = int(x - res)
            desired = max(desired, 0)
            desired = min(desired, 1280)
            cv.circle(frame, (desired, y), 6, (255, 255, 0), -1)
            ratio = x_boundary_for_green - desired
            ratio = ratio / x_boundary_for_green
            ratio = ratio * 70
            steering_value = int(90 - ratio)
        elif hisab[0][3] == 1:
            res = w / 180
            res = res * 360
            res = res ** 1.17
            desired = int(x + res)
            desired = max(desired, 0)
            desired = min(desired, 1280)
            cv.circle(frame, (desired, y), 6, (255, 255, 0), -1)
            ratio = desired - x_boundary_for_red
            ratio = ratio / (1280 - x_boundary_for_red)
            ratio = ratio * 70
            steering_value = int(90 + ratio)
    print(steering_value)

    half_width = frame.shape[1] // 2
    half_height = frame.shape[0] // 2

    resized_masks = [resize_mask(m, half_width, half_height) for m in masks]
    resized_masks_color = [cv.cvtColor(m, cv.COLOR_GRAY2BGR) for m in resized_masks]

    bottom_row = cv.hconcat(resized_masks_color)
    top_row = cv.resize(frame, (frame.shape[1], half_height))

    combined = cv.vconcat([top_row, bottom_row])
    text = f"Steering: {steering_value}"
    cv.putText(combined, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv.imshow("Detection and Masks", combined)

    fwall = lidar.get(0)
    if fwall < 480:
        motor.stop()
        print("stopped")

    rwall = lidar.get(60)
    lwall = lidar.get(300)
    diff = rwall - lwall
    diff = map_range(diff, -2800, 2800, -75, 75)
    diff = clamp(diff, -75, 75)

    err = diff
    ang = err * 1 + (err - last_err) * 5
    ang = clamp(ang, -75, 75)
    steer(servo, ang)
    # print(f"fwall={rwall}, lwall={lwall}, ang={ang}, corner={corner}")
    last_err = err

    if cv.waitKey(1) & 0xFF == ord('p'):
        break

# --- Cleanup ---
cam.release()
cv.destroyAllWindows()
