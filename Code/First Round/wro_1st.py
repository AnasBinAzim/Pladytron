import time
from utility import clamp, map_range, steer
from line_checks import coords, linearity, are_perpendicular, get_intersection
from servo import Servo
from lidar_reader import LidarReader
from motor import Motor
import numpy as np
from scipy.stats import linregress, false_discovery_control
from shapely.geometry import Point, Polygon
import pigpio
 
pi = pigpio.pi()
lidar = LidarReader(path="/home/wro/rplidar_sdk/output/Linux/Release/ultra_simple")
servo = Servo(4)
motor = Motor(pi)
 
# constants
rwall = 0
lwall = 0
direction = 0
err = 22
f = 0
checker = 13
last_time = -100
 
angle_groups = {
    "front": [356,357, 358,359, 0,1, 2,3, 4],
    "right": [86, 88, 90, 92, 94],
    "left": [266, 268, 270, 272, 274]
}
 
while True:
    if rwall and lwall:
        break
    rwall = lidar.get(90)  # right side wall
    lwall = lidar.get(270)  # left wall
 
if rwall <= lwall:
    follow_ang = 65
    corner_ang = 270
    print("following right wall")
elif lwall < rwall:
    follow_ang = 295
    corner_ang = 90
    print("following left wall")
 
corner = 0
fwall_init = lidar.get(0)
center_dist = lidar.get(follow_ang)
min_dist = 100
max_dist = (2 * center_dist) - min_dist
print(f"rwall={rwall} lwall={lwall} center={center_dist} max_dist={max_dist}")
time.sleep(3)
motor.forward(255)  # forward
 
 
def get_lidar_points(angles):
    points = []
    for angle in angles:
        r = lidar.get(angle)
        x, y = coords(r, angle)
        points.append([x, y])
    return np.array(points)
 
 
try:
    while True:
        print(direction)
        if direction == 0:
 
            num_groups = len(angle_groups)
            slopes = [None] * num_groups  # None for vertical lines
            intercepts = [None] * num_groups
            R2_values = [None] * num_groups
            f = 1
            cnt = 0
            print("start")
            for name, angs in angle_groups.items():
                pts = get_lidar_points(angs)
                is_line, slope, intercept, r2 = linearity(pts)
                slopes[cnt] = slope
                intercepts[cnt] = intercept
                R2_values[cnt] = r2
                if not is_line:
                    f = 0
                cnt += 1
                if name == "left":
                    print(f)
                    print(slope)
                    print(intercept)
                    print(pts)
                    for angee in angs:
                        print(lidar.get(angee))
                    print()
 
 
            if f == 1:
                if not are_perpendicular(slopes[0], slopes[1]):
                    print("rejected Line")
                    f = 0
                if not are_perpendicular(slopes[0], slopes[2]):
                    print("rejected Line")
                    f = 0
            print("Ned")                        
            print()
            if f == 1:
                xx, yy = get_intersection(slopes[0], intercepts[0] - err, slopes[1], intercepts[1] - err)
                xx2, yy2 = get_intersection(slopes[0], intercepts[0] - err, slopes[2], intercepts[2] + err)
                frnt = lidar.get(0) + err
                xf, yf = coords(frnt, 0)
                rght = lidar.get(90) + err
                xr, yr = coords(rght, 90)
                lft = lidar.get(270) + err
                xl, yl = coords(lft, 270)
                x4 = xr + (xx - xf)
                y4 = yr + (yy - yf)
                x5 = xf + (xx2 - xl)
                y5 = yf + (yy2 - yl)
 
                cnt = 7
                while cnt < 80 and direction == 0:
                    cnt += 1
                    x, y = coords(lidar.get(cnt), cnt)
                    p = Point(x, y)
                    print(x,y)
                    print(xf,yf)
                    print(xr,yr)
                    rect_points = [(xf, yf), (xx, yy), (xr, yr), (x4, y4)]
                    rectangle = Polygon(rect_points)
                    if not rectangle.contains(p):
                        #direction = 1
                        follow_ang = 65
                        corner_ang = 270
                        print(follow_ang)
                        break
 
                cnt = 353
                while cnt > 650 and direction == 0:
                    cnt -= 1
                    x, y = coords(lidar.get(cnt), cnt)
                    p = Point(x, y)
                    rect_points = [(xf, yf), (xx2, yy2), (xl, yl), (x5, y5)]
                    rectangle = Polygon(rect_points)
                    if not rectangle.contains(p):
                        #direction = 1
                        follow_ang = 295
                        corner_ang = 90
                        print(follow_ang)
                        break
 
        if time.perf_counter() - last_time > 1.55:
            points = []
            ange = corner_ang + checker
            cnt = 1
            while cnt <= 5:
                points.append(ange)
                ange += 1
                cnt += 1
            pts = get_lidar_points(points)
            is_line, slope, intercept, r2 = linearity(pts)
 
            points = []
            ange = corner_ang - checker
            cnt = 1
            while cnt <= 5:
                points.append(ange)
                ange -= 1
                cnt += 1
            pts = get_lidar_points(points)
            is_line2, slope2, intercept2, r22 = linearity(pts)
 
            if is_line and is_line2 and are_perpendicular(slope, slope2):
                corner += 1
                last_time = time.perf_counter()
                print(corner)
 
        dist = lidar.get(follow_ang)
        fwall = lidar.get(0)  # get front dist
        time.sleep(1)
        print(1)
 
        if corner == 12 and fwall < 1450 and time.perf_counter() - last_time > 1.35:
            motor.stop()
 
        if fwall < 0:
            while True:
                fwall = lidar.get(0)
                if fwall > 1200:
                    break
                if follow_ang < 180:
                    steer(servo, -75)
                else:  # left
                    steer(servo, 75)
 
        if dist is not None:
            d = clamp(dist, min_dist, max_dist)
            ang = map_range(d, min_dist, max_dist, -75, 75)
            if follow_ang < 180:
                steer(servo, ang)
            else:  # left
                steer(servo, -ang)
 
except KeyboardInterrupt:
    print("Stopping LIDAR...")
    lidar.stop()
    motor.stop()
 
