import pigpio
import utility


class Servo:
    def __init__(self, gpio_pin):
        self.servo_pin = gpio_pin
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpio daemon not running!")

    def set(self, angle):
        pulse = utility.map_range(angle, 0, 180, 1000, 2000)
        pulse = max(1000, min(2000, pulse))
        self.pi.set_servo_pulsewidth(self.servo_pin, pulse)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        self.pi.stop()
