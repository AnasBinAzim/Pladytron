import subprocess
import threading
import re

class LidarReader:
    def __init__(self, path, port="/dev/ttyUSB0", baud="460800"):
        self.data = {}  # Stores {angle: distance}
        self.process = subprocess.Popen(
            [path, "--channel", "--serial", port, baud],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.thread = threading.Thread(target=self._read_sensor_output)
        self.thread.daemon = True
        self.thread.start()

    def _parse_line(self, line):
        match = re.match(r"([\d.]+)\s+([\d.]+)", line)
        if match:
            return {
                "ang": int(float(match.group(1))),
                "dist": int(float(match.group(2))),
            }
        return None

    def _read_sensor_output(self):
        for line in iter(self.process.stdout.readline, b''):
            decoded = line.decode('utf-8').strip()
            if decoded:
                parsed = self._parse_line(decoded)
                if parsed:
                    degree = parsed["ang"]
                    self.data[degree] = parsed["dist"]

    def get(self, angle):
        return self.data.get(angle, None)

    def get_all(self):
        return self.data.copy()

    def stop(self):
        self.process.terminate()

