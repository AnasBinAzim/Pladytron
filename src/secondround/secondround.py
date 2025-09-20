import cv2 as cv
import time
import math
from utility import clamp, map_range, steer
from line_checks import coords, linearity, are_perpendicular, get_intersection, are_parallel, get_front_line,angle,get_yaw_diff, inside_polygon
from servo import Servo
from lidar_reader import LidarReader
from gyro_reader import GyroReader
from motor import Motor
import numpy as np
from scipy.stats import linregress, false_discovery_control
from line_plotter import line_show,point_show
from shapely.geometry import Point, Polygon
import pigpio
from button import Button
from camera_reader import CameraReader

default_speed=165
# object constants
max_width = 80
max_x_delta_change = 177
delta_change_ratio = 0.9
# constant
steering_value = 0
steering_limit = 75
obj_steer_err = 20
width_for_constant_distance = 9  # minimum acceptable width
minimum_y_for_object = 10
band_height = 300
minimum_width_for_object = 28
obj_steer_boundary = 150
obj_steer_limit = 120

last_obj = 0
last_obj_timer = 1.25
last_obj_found = -100

direction = 0
col_flag = 0
col_timer = 3.2
col_yaw_timer = 1
col_yaw_risk_timer = 3.56
col_last_timer = -100
parking_timer = -100
col_yaw_update_tolerance = 12
is_col = 0
corner = 0
lap_cnt = 1
last_err=0
speed = 0

parking_end_flag = False
parking_start_flag = True
too_close = False

too_close_timer = 0
side_risk_dist = 185

# Global variables
erre = 40
minimum_x_for_object = 100
maximum_x_for_object = 600
minimum_y_for_object = 230
maximum_y_for_object = 290
minimum_x_for_line = 200
maximum_x_for_line = 440
minimum_y_for_line = 330
maximum_y_for_line = 255

# 0 = blue
# 1 = orange 
# 2 = green
# 3 = red
# 4 = pink

exclusion_sets = {
    0: (),       # nothing excluded
    1: (4,),   # exclude colors 0 and 3
    2: (),       # nothing excluded
    3: (0, 1, 2,4),     # exclude color 1
    4: (),
}

# first round part
pi = pigpio.pi()
lidar = LidarReader(path="/home/wro/rplidar_sdk/output/Linux/Release/ultra_simple")
gyro = GyroReader(freq=60.0)
servo = Servo(4)
cam_reader = CameraReader(pi, cam_pins=(20, 21), width=640, height=480)
motor = Motor(pi)
btn = Button(pi, 16)

LED_PIN = 9

pi.set_mode(LED_PIN, pigpio.OUTPUT)   # Set GPIO25 as output
pi.write(LED_PIN, 0)

rwall = None
lwall = None
while rwall is None or lwall is None or lwall ==0 or rwall ==0:
    rwall = lidar.get(150)
    lwall = lidar.get(30)

print(f"rwall={rwall} lwall={lwall}")

    
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
line_hsv_list = [all_hsv_ranges[0], all_hsv_ranges[1]]

object_colors = [
    (255, 0, 0),     # Blue
    (0, 165, 255),   # Orange
    (0, 255, 0),     # Green
    (0, 0, 255),     # Red
    (255, 0, 255)    # Pink (magenta)
]


# ~ # --- Open any camera from index 0 to 9 ---
# ~ for cam_index in range(10):
    # ~ cam = cv.VideoCapture(cam_index)
    # ~ cam.set(3, 640)
    # ~ cam.set(4, 480)
    # ~ if cam.isOpened():
        # ~ print(f"? Camera opened at index {cam_index}")
        # ~ break
    # ~ cam.release()
# ~ else:
    # ~ print("? No working camera found.")
    # ~ exit()

# --- Resize masks helper ---
def resize_mask(mask, width, height):
    return cv.resize(mask, (width, height), interpolation=cv.INTER_NEAREST)

def getContours(framde, current_index, draw_color):
    global all_hsv_ranges, exclusion_sets

    hsv = cv.cvtColor(framde, cv.COLOR_BGR2HSV)

    # --- Start with full mask (everything allowed initially) ---
    mask = np.ones(hsv.shape[:2], dtype=np.uint8) * 255

    # --- Apply exclusions first ---
    if current_index in exclusion_sets:
        for idx in exclusion_sets[current_index]:
            lower_ex = np.array(all_hsv_ranges[idx][:3])
            upper_ex = np.array(all_hsv_ranges[idx][3:])
            exclusion_mask = cv.inRange(hsv, lower_ex, upper_ex)
            mask[exclusion_mask > 0] = 0  # black out excluded pixels

    # --- Now apply the selected HSV range ---
    lower = np.array(all_hsv_ranges[current_index][:3])
    upper = np.array(all_hsv_ranges[current_index][3:])
    selected_mask = cv.inRange(hsv, lower, upper)

    # Keep only pixels that are BOTH in the allowed area and in the selected range
    mask = cv.bitwise_and(selected_mask, mask)
    if current_index == 0:
        cv.imshow("blue",mask)
    if current_index == 1:
        cv.imshow("orange",mask)
    # --- Find contours ---
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    list = []

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 100:
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv.boundingRect(approx)
            x = int(x + w / 2)
            y = int(y + h / 2)

            rect = [x, y, w, h]
            if y > minimum_y_for_object:
                cv.circle(frame, (x, y), 6, draw_color, -1)  # <- use passed color
                list.append(rect)

    return list



def get_middle_frame(frame):
    mask_pts = np.array([[0, minimum_y_for_object], [640, minimum_y_for_object], [640, maximum_y_for_object+erre], [0, maximum_y_for_object+erre]], np.int32)
    mask = np.zeros((480, 640), dtype=np.uint8)
    cv.fillPoly(mask, [mask_pts], 255)
    frame = cv.bitwise_and(frame, frame, mask=mask)                                       
    return frame
    
yaw = gyro.get_yaw()
true_yaw = yaw
which_obj = 0

def parking_end():
    global direction,yaw,true_yaw
    motor.go(130)
    while lidar.get(90) > 300:
        yaw = gyro.get_yaw()
        result = get_yaw_diff(true_yaw, yaw)
        result = clamp(result,-75,75)
        result = map_range(result,-75,75,-75,75)
        steer(servo,result)
        print(f"restult = {result}")
    motor.go(-130)
    print("first step done")
    if direction==1:
        true_yaw -= 90
        true_yaw += 360
        true_yaw %= 360
    else:
        true_yaw += 90
        true_yaw += 360
        true_yaw %= 360
        
    print(f"ya: {yaw}, true_yaw:{true_yaw}, diff:{abs(get_yaw_diff(true_yaw, yaw))}")
    while abs(get_yaw_diff(true_yaw, yaw)) >= 7:
        yaw = gyro.get_yaw()
        result = get_yaw_diff(true_yaw, yaw)
        result = clamp(result,-75,75)
        result = -map_range(result,-75,75,-75,75)
        steer(servo,result)
        print(f"restult = {result}")
    motor.go(130)
    while lidar.get(90) > 600:
        yaw = gyro.get_yaw()
        result = get_yaw_diff(true_yaw, yaw)
        # ~ result = clamp(result,-40,75)
        result = map_range(result,-20,20,-75,75)
        steer(servo,result)
    if direction==1:
        true_yaw -= 90
        true_yaw += 360
        true_yaw %= 360
    else:
        true_yaw += 90
        true_yaw += 360
        true_yaw %= 360
    while abs(get_yaw_diff(true_yaw, yaw)) >= 20:
        yaw = gyro.get_yaw()
        result = get_yaw_diff(true_yaw, yaw)
        result = clamp(result,-75,75)
        result = map_range(result,-75,75,-75,75)
        steer(servo,result)
        print(f"restult = {result}")
    while True:
        if direction==2: # right wall
            rwall=lidar.get(180)
            steering_value = map_range(rwall, 300, 500, -65,65)
            steer(servo,steering_value)
            print("following right wall")
            yaw=gyro.get_yaw()
        elif direction==1: # left wall
            rwall=lidar.get(0)
            steering_value = -map_range(rwall, 300, 500, -65,65)
            steer(servo,steering_value)
            print("following left wall")
        if abs(get_yaw_diff(true_yaw,yaw)) < 5:
                break
    parking_timer = 1000
    while True:
        ret, frame9 = cam.read()
        if not ret:
            print("? Failed to grab frame.")
            break       
        frame9 = get_middle_frame(frame9)
        cv.imshow("parking",frame9)
        hisab = getContours(frame9,4,object_colors[4])
        yaw = gyro.get_yaw()
        result = get_yaw_diff(true_yaw, yaw)
        result = clamp(result,-75,75)
        result = map_range(result,-30,30,-75,75)
        steer(servo,result)
        if len(hisab) == 0:
            break
        
    motor.stop()
    time.sleep(30)
    exit()
        
def last_parking():
    global direction, yaw, true_yaw

def start_from_parking(d):
    global yaw,true_yaw

    motor.go(-60)
    while lidar.get(270) > 160:
        print(f"backwall={lidar.get(270)}")
    motor.stop()

    if d == 'L':
        steer(servo, 75)
        motor.go(100)
        while get_yaw_diff(true_yaw, yaw) > -30:
            yaw = gyro.get_yaw()
        while get_yaw_diff(true_yaw, yaw) > -60:
            yaw = gyro.get_yaw()
            print(f"true_yaw = {true_yaw}, yaw = {yaw}")
    else:
        steer(servo, -75)
        motor.go(100)
        while get_yaw_diff(true_yaw, yaw) < 30:
            yaw = gyro.get_yaw()
        while get_yaw_diff(true_yaw, yaw) < 60:
            yaw = gyro.get_yaw()
    steer(servo, 0)
    motor.go(speed)
    time.sleep(0.25)
    

prev_btn_state = 1
btn_cnt = 0
status = 0
yaw_cnt = 0
pi.write(LED_PIN, 1)
parking = 0

# --- Main loop ---
while True:
    state = btn.state()
    yaw = gyro.get_yaw()
    if state == 1 and prev_btn_state == 0:
        print("Button pressed")
        btn_cnt += 1
        corner = 0
        direction = 0
        yaw_cnt = 0
        true_yaw = yaw
        col_last_timer = -100
        parking_timer = -100
        too_close_timer = -100
        if (btn_cnt%2) == 1 and parking_start_flag is True:
        
            steer(servo,0)
            print("pressed")
            time.sleep(1)
            if lidar.get(0) < 200: # leftside parking
                start_from_parking('L')
            elif lidar.get(180) < 200: # rightside parking
                start_from_parking('R')
        if speed > 0:
            status = 0
            speed = 0
            pi.write(LED_PIN, 1)
        else:
            status = 1
            speed = default_speed
            pi.write(LED_PIN,0)
    if btn_cnt >= 8:
        print("Stopping LIDAR and motors...")
        lidar.stop()
        motor.stop()
        servo.stop()
        break
    
    

    prev_btn_state = state
    motor.go(speed)        
    fwall = lidar.get(0)
    if corner >= lap_cnt:
        if parking_end_flag == True:
            parking_end()
        print("1")
        speed = 0
        
    
    frame = cam_reader.get_frame()
    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
        cv.imshow("Raw Frame", frame)
    else:
        print("?? No valid frame yet...")
        continue
    # ~ cv.imshow("Raw Frame", frame)
    if col_flag == 1 and  time.perf_counter() - col_last_timer > col_yaw_timer:
        col_flag = 2
        pi.write(LED_PIN,0)
        yaw_cnt += 1
        if direction == 1:
            true_yaw += 90
            true_yaw += 360
            true_yaw %= 360
        elif direction == 2:
            true_yaw -= 90
            true_yaw += 360
            true_yaw %= 360
    elif col_flag == 2 and  time.perf_counter() - col_last_timer > col_timer:
        col_flag = 0
        corner += 1
    elif col_flag == 0 and corner < lap_cnt:
        blue = 0
        orange = 0
        mask_pts = np.array([[minimum_x_for_line, minimum_y_for_line], [maximum_x_for_line, minimum_y_for_line], [maximum_x_for_line, 480], [minimum_x_for_line, 480]], np.int32)
        mask = np.zeros((480, 640), dtype=np.uint8)
        cv.fillPoly(mask, [mask_pts], 255)
        
        line_frame = cv.bitwise_and(frame, frame, mask=mask)                                 
        cv.imshow("line" ,line_frame)
        hisab = []
        for i, hsv_range in enumerate(line_hsv_list):
            color = object_colors[i] if i < len(object_colors) else (255, 255, 255)
            list_contours = getContours(line_frame, i, color)
            for obj in list_contours:
                hisab.append([-obj[1], obj[0], obj[2], i, obj[3]])
        hisab.sort()
        if len(hisab) > 0:
            x = hisab[0][1]
            y = -hisab[0][0]
            w = hisab[0][2]
            h = hisab[0][4]
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            print(f"x = {x}, y = {y}, w = {w}, h = {h}")
            if hisab[0][3] == 0:
                blue = 1
                if direction == 0:
                    direction = 1
            elif hisab[0][3] == 1:
                orange = 1
                if direction == 0:
                    direction = 2
        if direction == 1 and blue == 1:
            col_flag = 1
            # ~ corner += 1
            pi.write(LED_PIN, 1)
            col_last_timer = time.perf_counter()
        if direction == 2 and orange == 1:
            col_flag = 1
            # ~ corner += 1
            pi.write(LED_PIN, 1)
            col_last_timer = time.perf_counter()               
    frame = get_middle_frame(frame)
    # cv.imshow("Masks", hsv)
    
    hisab = []
    for i, hsv_range in enumerate(object_hsv_list):
        color = object_colors[i+2] if i+2 < len(object_colors) else (255, 255, 255)
        list_contours = getContours(frame, i+2, color)
        for obj in list_contours:
            x = obj[0]
            y = obj[1]
            w = obj[2]
            h = obj[3]
            hisab.append([-(y+h/2),x,y,i,w,h])
        
    hisab.sort()
    steering_value = 0
    desired = 960
    obj = False
    obj_x = -1
    which_obj = 0
    last_obj = 0
    if len(hisab) > 0:
        x = hisab[0][1]
        y = hisab[0][2]
        bottom = -hisab[0][0]
        w = hisab[0][4]
        h = hisab[0][5]
        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)
        
        print(f"width = {w}, height = {h}")
        
        if hisab[0][3] == 0 and w >= minimum_width_for_object and y >= minimum_y_for_object and y <= maximum_y_for_object:  # green obj
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            res1 = (w - minimum_width_for_object) / (max_width - minimum_width_for_object)
            res1 = clamp(res1,0,1.0)
            res2 = (640-90-x) / (640-90)
            res2 = clamp(res2,0,1.0)
            rest = res1 * res2
            rest = math.sqrt(rest)
            rest = clamp(rest,0,1.0)
            rest = rest ** 0.33
            rest = clamp(rest,0,1.0)
            print(f"res1 = {res1}, res2 = {res2}, rest = {rest}")
            steering_value = 0 - (steering_limit * rest)
            if steering_value != 0:
                obj = True
            last_obj = 1
            last_obj_found = time.perf_counter()
            if w >= 70:
                obj_x = x
        elif hisab[0][3] == 1 and w >= minimum_width_for_object and y >= minimum_y_for_object and y <= maximum_y_for_object:   # red obj
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            res1 = (w - minimum_width_for_object) / (max_width - minimum_width_for_object)
            res1 = clamp(res1,0,1.0)
            res2 = (x-90) / (640 - 90)
            res2 = clamp(res2,0,1.0)
            rest = res1 * res2
            rest = math.sqrt(rest)
            rest = clamp(rest,0,1.0)
            rest = rest ** 0.33
            rest = clamp(rest,0,1.0)
            print(f"res1 = {res1}, res2 = {res2}, rest = {rest}")
            steering_value = 0 + (steering_limit * rest)
            if steering_value != 0:
                obj = True
            last_obj = 2
            last_obj_found = time.perf_counter()
            if w >= 70:
                obj_x = x
     
                
                
            
    hisab = getContours(frame,4,object_colors[4])
    parking = 0
    if len(hisab) > 0:
        parking = 1
        parking_timer = time.perf_counter()
        '''
        if parking == 1 and which_obj == 1:
            obj = True
            x = xx + obj_x
            print(f"x={x}, obj_x={obj_x}")
            x /= 2
            print(f"x={x}, obj_x={obj_x}")
            x = clamp(x,90,550)
            steering_value = map_range(x,40,600,-75,75)
        '''
    # ~ half_width = frame.shape[1] // 2
    
    # ~ half_height = frame.shape[0] // 2

    # ~ resized_masks = [resize_mask(m, half_width, half_height) for m in masks]
    # ~ resized_masks_color = [cv.cvtColor(m, cv.COLOR_GRAY2BGR) for m in resized_masks]

    # ~ bottom_row = cv.hconcat(resized_masks_color)
    # ~ top_row = cv.resize(frame, (frame.shape[1], half_height))
    '''
    if status == 1 and too_close is True:
        if obj_x == -1: # No obj in frame
            res = clamp(get_yaw_diff(true_yaw,yaw),-75,75)
            steering_value = -map_range(res, -75, 75, -75, 75)
            steer(servo,steering_value)
            motor.go(-120)
            print(f"-------No object too close = {steering_value}")
            while too_close is True:
                flag = 0
                for i in range(50,130,1):
                    if inside_polygon(lidar.get(i),i) is True:
                        flag = 1
                if flag == 0:
                    too_close = False
                    col_last_timer -= time.perf_counter() - too_close_timer
        else: # object present in frame
            if last_obj == 1: # green object
                steer(servo, 75)    # steer left
            elif last_obj == 2: # red object
                steer(servo, -75)   # steer left
            motor.go(-120)
            print(f"-------Has object too close = {steering_value}")
            while too_close is True:
                flag = 0
                for i in range(50,130,1):
                    if inside_polygon(lidar.get(i),i) is True:
                        flag = 1
                if flag == 0:
                    too_close = False
                    col_last_timer -= time.perf_counter() - too_close_timer
        
        # ~ if time.perf_counter() - too_close_timer >= 0.6 or lidar.get(270) < 180:
            # ~ too_close = False
            # ~ col_timer -= time.perf_counter() - too_close_timer
            # ~ pi.write(LED_PIN,0)
        if status == 1:
            speed = default_speed 
        cv.imshow("frame",frame)
    '''
         
    if obj is False and time.perf_counter() - last_obj_found <= last_obj_timer:
        res = clamp(get_yaw_diff(true_yaw,yaw),-63,63)
        steering_value = map_range(res, -63, 63, -75, 75) 
        
        print(f"steering = {steering_value}, yaw diff = {get_yaw_diff(true_yaw,yaw)}")
    elif obj is False:
        res = 0
        sm = 0
        for i in range(0,180,3):
            res += i * lidar.get(i)
            sm += lidar.get(i)   
        res /= sm     
        res = clamp(res,0,180)
        steering_value = map_range(res, 25, 155, -65, 65)  
              
    err = steering_value
    if obj is True:
        steering_value = err * 1.19 + (err - last_err) * 0
    else:
        steering_value = err * 1.9 + (err - last_err) * 5    
    last_err = err
    '''
    
    if speed == 1 and too_close is False:
        for i in range(50,130,1):
            if inside_polygon(lidar.get(i),i):
                too_close = True
                print("Too close True")
                pi.write(LED_PIN,1)
                speed = 0
                # ~ time.sleep(10)
                too_close_timer = time.perf_counter()
                break
       '''         
    
    print(f"cnt = {yaw_cnt}, steer = {steering_value}, yaw = {yaw}, true_yaw = {true_yaw},corner = {corner} ")
    cv.putText(frame, f"Steering: {steering_value}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)

    steering_value = clamp(steering_value,-75,75)
    # ~ left_risk_dist = 2500
    # ~ right_risk_dist = 2500
    # ~ for i in range (10,25,5):
        # ~ left_risk_dist = min(left_risk_dist,abs(lidar.get(i) * math.cos(math.radians(i))))
    # ~ for i in range (160,175,5):
        # ~ right_risk_dist = min(right_risk_dist,abs(lidar.get(i) * math.cos(math.radians(i))))
    # ~ if left_risk_dist <= side_risk_dist:
        # ~ side_risk = map_range(left_risk_dist,57,side_risk_dist,0,30)
        # ~ side_risk = 30 - clamp(side_risk,0,30)
        # ~ steering_value = max(side_risk,steering_value)
        # ~ print(f"side_risk = {side_risk}, steering_value = {steering_value}")
        # ~ print("1")
    # ~ if right_risk_dist <= side_risk_dist:
        
        # ~ side_risk = map_range(right_risk_dist,57,side_risk_dist,0,30)
        # ~ side_risk = 30 - clamp(side_risk,0,30)
        # ~ steering_value = min(-side_risk,steering_value)
        # ~ print(f"side_risk = {side_risk}, steering_value = {steering_value}")
        # ~ print("22")
    
    '''left_risk_dist = 2500
    right_risk_dist = 2500
    for i in range (0,15,5):
        left_risk_dist = min(left_risk_dist,abs(lidar.get(i) * math.cos(math.radians(i))))
    for i in range (165,180,5):
        right_risk_dist = min(right_risk_dist,abs(lidar.get(i) * math.cos(math.radians(i))))
    if left_risk_dist <= side_risk_dist:
        side_risk = map_range(left_risk_dist,57,side_risk_dist,0,60)
        side_risk = clamp(side_risk,0,60)
        steering_value = max(side_risk,steering_value)
    print(f"right_risk_dist = {right_risk_dist}")
    if right_risk_dist <= side_risk_dist:
        
        side_risk = map_range(right_risk_dist,57,side_risk_dist,0,50)
        side_risk = clamp(side_risk,0,60)
        steering_value = min(-side_risk,steering_value)
    '''
    steer(servo, steering_value)    
    cv.imshow("frame",frame)
    # ~ combined = cv.vconcat([top_row, bottom_row])
    # ~ text = f"Steering: {steering_value}"
    # ~ cv.putText(combined, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    # ~ cv.imshow("Detection and Masks", combined)

    
    
    # ~ print(f"steering = {steering_value}, elapsed = {time.perf_counter()-prev_time}")
    

    if cv.waitKey(1) & 0xFF == ord('p'):
        break

# --- Cleanup ---
cam.release()
cv.destroyAllWindows()
motor.stop()
