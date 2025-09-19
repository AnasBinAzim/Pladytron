import subprocess
import threading
import re

class LidarReader:
    def __init__(self, path, port="/dev/ttyUSB0", baud="460800"):
        # Dictionary to store lidar readings {angle: distance}
        self.data = {}  
        
        # Launch external lidar binary as a subprocess
        # Example: ./lidar_driver --channel --serial /dev/ttyUSB0 460800
        self.process = subprocess.Popen(
            [path, "--channel", "--serial", port, baud],
            stdout=subprocess.PIPE,   # Capture standard output (lidar data)
            stderr=subprocess.PIPE    # Capture error messages
        )

        # Start a background thread to continuously read lidar output
        self.thread = threading.Thread(target=self._read_sensor_output)
        self.thread.daemon = True   # Daemon so it stops when main program ends
        self.thread.start()

    def _parse_line(self, line):
        # Match lines with two numeric values: angle and distance
        match = re.match(r"([\d.]+)\s+([\d.]+)", line)
        if match:
            return {
                "ang": int(float(match.group(1))),   # angle in degrees
                "dist": int(float(match.group(2))), # distance in mm (or cm)
            }
        return None  # Ignore malformed lines

    def _read_sensor_output(self):
        # Continuously read output from lidar process line by line
        for line in iter(self.process.stdout.readline, b''):
            decoded = line.decode('utf-8').strip()  # Convert from bytes to string
            if decoded:
                parsed = self._parse_line(decoded)  # Extract angle & distance
                if parsed:
                    degree = parsed["ang"]
                    # Store distance value mapped by its angle
                    self.data[degree] = parsed["dist"]

    def get(self, angle):
        # Get distance at a specific angle
        return self.data.get(angle, None)

    def get_all(self):
        # Return a snapshot copy of all current lidar readings
        return self.data.copy()

    def stop(self):
        # Stop the lidar process
        self.process.terminate()
