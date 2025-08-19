import time
from utility import clamp, map_range, steer
from servo import Servo
from lidar_reader import LidarReader
from motor import Motor
import pigpio

pi = pigpio.pi()
lidar = LidarReader(path="/home/wro/rplidar_sdk/output/Linux/Release/ultra_simple")
servo = Servo(4)
motor = Motor(pi)

rwall = None
lwall = None
while rwall is None or lwall is None:
    rwall = lidar.get(90)   # right side wall
    lwall = lidar.get(270)  # left wall
if rwall <= lwall:
    follow_ang = 60
    print("following right wall")
elif lwall < rwall:
    follow_ang = 300
    print("following left wall")

corner=0
fwall_init = lidar.get(0)
center_dist = lidar.get(follow_ang)
min_dist = 100
max_dist = (2 * center_dist) - min_dist
print(f"rwall={rwall} lwall={lwall} center={center_dist} max_dist={max_dist}")
time.sleep(3)
motor.forward(180)  # forward
try:
    while True:
        dist = lidar.get(follow_ang)
        fwall = lidar.get(0)  # get front dist
        if corner==12 and fwall<fwall_init:
            motor.stop()
        if fwall<1050:
            if flagC:
                corner+=1
                flagC=False
        else:
            flagC=True
        if fwall<600:
            while True:
                fwall=lidar.get(0)
                if fwall > 1200: break
                print(f"fwall={fwall}")
                if follow_ang < 180:
                    steer(servo,-75)
                else:  # left
                    steer(servo,75)
        if dist is not None:
            d = clamp(dist, min_dist, max_dist)
            ang = map_range(d, min_dist, max_dist, -75, 75)
            # ~ ang = ang*2
            if follow_ang < 180:
                steer(servo, ang)
            else:  # left
                steer(servo, -ang)
            print(f"fwall={fwall}, d={dist}, ang={ang}, corner={corner}")
        # ~ time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping LIDAR...")
    lidar.stop()
    motor.stop()
