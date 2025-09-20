from utility import map_range, clamp  # Import utility functions for mapping and clamping values
import pigpio  # Import the pigpio library for controlling GPIO pins

class Motor:
    def __init__(self, pi, forward_pin=12, reverse_pin=18, freq=1000):
        """
        Motor class to control a motor with forward and reverse functions using GPIO pins.

        pi          = pigpio.pi() instance (already connected to the Raspberry Pi)
        forward_pin = GPIO pin for forward direction (default: 12)
        reverse_pin = GPIO pin for reverse direction (default: 18)
        freq        = PWM frequency for controlling motor speed (default: 1000 Hz)
        """
        self.pi = pi  # Store the pigpio instance
        self.forward_pin = forward_pin  # Set GPIO pin for forward direction
        self.reverse_pin = reverse_pin  # Set GPIO pin for reverse direction
        self.freq = freq  # Set PWM frequency

        # Setup GPIO pins as OUTPUT
        self.pi.set_mode(self.forward_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.reverse_pin, pigpio.OUTPUT)

        # Ensure motor is stopped initially
        self.stop()

    def forward(self, speed=255):
        """
        Run motor in the forward direction with the specified speed.

        speed = PWM duty cycle (0 to 255)
        """
        speed = clamp(speed, 0, 255)  # Ensure speed is within range (0 to 255)
        self.pi.set_PWM_frequency(self.forward_pin, self.freq)  # Set PWM frequency for forward pin
        self.pi.set_PWM_dutycycle(self.forward_pin, speed)  # Set PWM duty cycle for forward direction
        self.pi.write(self.reverse_pin, 0)  # Ensure reverse direction is off

    def reverse(self, speed=255):
        """
        Run motor in the reverse direction with the specified speed.

        speed = PWM duty cycle (0 to 255)
        """
        speed = clamp(speed, 0, 255)  # Ensure speed is within range (0 to 255)
        self.pi.set_PWM_frequency(self.reverse_pin, self.freq)  # Set PWM frequency for reverse pin
        self.pi.set_PWM_dutycycle(self.reverse_pin, speed)  # Set PWM duty cycle for reverse direction
        self.pi.write(self.forward_pin, 0)  # Ensure forward direction is off

    def stop(self):
        """
        Stop the motor completely by turning off both forward and reverse directions.
        """
        self.pi.set_PWM_dutycycle(self.forward_pin, 0)  # Set forward pin PWM duty cycle to 0
        self.pi.set_PWM_dutycycle(self.reverse_pin, 0)  # Set reverse pin PWM duty cycle to 0
