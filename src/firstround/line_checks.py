import numpy as np
from scipy.stats import linregress
from shapely.geometry import Point, Polygon
#constants
threshold = 0.83
tol = 0.85

def coords(r, theta_deg):
    theta = np.deg2rad(theta_deg)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def linearity(points):
    x = points[:, 0]
    y = points[:, 1]
    # Handle vertical line case separately
    if np.allclose(x, x[0], atol=1e-3):
        return True, None, x[0], 1.0  # Line is x = constant

    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    r2 = r_value ** 2
    return (r2 >= threshold, slope, intercept, r2)


def are_perpendicular(m1, m2):
    # Handle vertical lines (slope=None)
    if m1 is None and m2 == 0:
        return True
    if m2 is None and m1 == 0:
        return True
    if m1 is None or m2 is None:
        return False  # cannot determine other combinations

    # Check product of slopes
    return abs(m1 * m2 + 1) < tol

def get_intersection(m0, b0, m1, b1):
    # Handle vertical lines
    if m0 is None:  # line 0 vertical
        x_int = b0
        y_int = m1 * x_int + b1
    elif m1 is None:  # line 1 vertical
        x_int = b1
        y_int = m0 * x_int + b0
    else:
        # regular case
        x_int = (b1 - b0) / (m0 - m1)
        y_int = m0 * x_int + b0
    return x_int, y_int

