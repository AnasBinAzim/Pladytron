import subprocess
import threading
import re
import math

# === Global clustering parameters (tune these) ===
MIN_CLUSTER_POINTS = 2    # Minimum number of points to form a cluster
MAX_CLUSTER_POINTS = 100       # Max points (to reject walls)
MIN_CLUSTER_WIDTH = 30        # mm
MAX_CLUSTER_WIDTH = 120       # mm
POINT_DIST_THRESH = 21     # mm (max distance between consecutive points)
scan_range_min = 15
scan_range_max = 165


class LidarReader:
    def __init__(self, path, port="/dev/ttyUSB0", baud="460800"):
        self.data = {}  # Stores {angle: distance_mm}
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
        """Get distance at a specific angle (mm)."""
        return self.data.get(angle, 0)

    def get_all(self):
        """Get full scan dictionary {angle: distance_mm}."""
        return self.data.copy()
    
    def stop(self):
        """Stop Lidar process."""
        self.process.terminate()

    # === Clustering helpers ===
    def _cluster_max_width(self, cluster):
        """Width = distance between first and last point (mm)."""
        x1, y1, *_ = cluster[0]
        x2, y2, *_ = cluster[-1]
        return math.hypot(x2 - x1, y2 - y1)

    def _cluster_centroid(self, cluster):
        """Return centroid (x, y) in meters."""
        xs = [p[0] for p in cluster]
        ys = [p[1] for p in cluster]
        return (sum(xs) / len(xs) / 1000.0, sum(ys) / len(ys) / 1000.0)

    def get_clusters(self):
        clusters = []
        current_cluster = []

        scan = self.get_all()
        prev_x, prev_y = None, None

        for ang in range(scan_range_min, scan_range_max):  # example narrowed FOV
            r = scan.get(ang, 0)
            if r <= 0:
                continue

            a_rad = math.radians(ang)
            x = r * math.cos(a_rad)
            y = r * math.sin(a_rad)

            if prev_x is not None and prev_y is not None:
                dist = math.hypot(x - prev_x, y - prev_y)
                if dist > POINT_DIST_THRESH:
                    if current_cluster:
                        clusters.append(current_cluster)
                        current_cluster = []

            current_cluster.append((x, y))
            prev_x, prev_y = x, y

        if current_cluster:
            clusters.append(current_cluster)

        # --- Process clusters ---
        results = []
        for cluster in clusters:
            if len(cluster) < 2:
                continue

            # width
            first_x, first_y = cluster[0]
            last_x, last_y = cluster[-1]
            width = math.hypot(last_x - first_x, last_y - first_y)

            if MIN_CLUSTER_WIDTH <= width <= MAX_CLUSTER_WIDTH:
                cx = sum(p[0] for p in cluster) / len(cluster)
                cy = sum(p[1] for p in cluster) / len(cluster)

                results.append({
                    "points": cluster,
                    "centroid": (cx, cy),  # mm
                    "width": width
                })

        # --- Find nearest cluster ---
        if not results:
            return (None, None)

        nearest = min(results, key=lambda c: math.hypot(c["centroid"][0], c["centroid"][1]))
        return nearest["centroid"]


