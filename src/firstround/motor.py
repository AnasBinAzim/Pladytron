from utility import map_range, clamp
import pigpio

class Motor:
    def __init__(self, pi, forward_pin=12, reverse_pin=18, freq=1000):
        self.pi = pi
        self.forward_pin = forward_pin
        self.reverse_pin = reverse_pin
        self.freq = freq

        # Setup pins
        self.pi.set_mode(self.forward_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.reverse_pin, pigpio.OUTPUT)

        # Ensure stopped initially
        self.stop()

    def forward(self, speed=255):
        speed = clamp(speed,0,255)
        """Run motor forward with given speed (0?255)."""
        self.pi.set_PWM_frequency(self.forward_pin, self.freq)
        self.pi.set_PWM_dutycycle(self.forward_pin, speed)  
        self.pi.write(self.reverse_pin, 0)

    def reverse(self, speed=255):
        speed = clamp(speed,0,255)
        """Run motor reverse with given speed (0?255)."""
        self.pi.set_PWM_frequency(self.reverse_pin, self.freq)
        self.pi.set_PWM_dutycycle(self.reverse_pin, speed)
        self.pi.write(self.forward_pin, 0)

    def stop(self):
        """Stop motor completely."""
        self.pi.set_PWM_dutycycle(self.forward_pin, 0)
        self.pi.set_PWM_dutycycle(self.reverse_pin, 0)
