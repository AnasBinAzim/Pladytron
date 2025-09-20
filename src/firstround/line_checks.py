import numpy as np  # Importing numpy for numerical operations
from scipy.stats import linregress  # Importing linregress for linear regression
from shapely.geometry import Point, Polygon  # Importing shapely for geometric shapes (though not used in the code)

# Constants
threshold = 0.83  # R-squared value threshold for determining if points lie on a line
tol = 0.85  # Tolerance for checking perpendicularity (slopes of lines)

def coords(r, theta_deg):
    """
    Convert polar coordinates (r, theta) to Cartesian coordinates (x, y).
    
    r: Radius (distance from the origin)
    theta_deg: Angle in degrees
    
    Returns the Cartesian coordinates (x, y)
    """
    theta = np.deg2rad(theta_deg)  # Convert angle from degrees to radians
    x = r * np.cos(theta)  # Calculate x coordinate
    y = r * np.sin(theta)  # Calculate y coordinate
    return x, y  # Return the Cartesian coordinates

def linearity(points):
    """
    Checks if the given set of points lie on a straight line using linear regression.
    
    points: A 2D numpy array where each row is a point (x, y)
    
    Returns a tuple with:
    - A boolean indicating if the points are approximately linear (R-squared >= threshold)
    - The slope of the line (None for vertical lines)
    - The intercept of the line
    - R-squared value
    """
    x = points[:, 0]  # Extract x-coordinates from the points
    y = points[:, 1]  # Extract y-coordinates from the points
    
    # Handle vertical line case separately (when all x values are the same)
    if np.allclose(x, x[0], atol=1e-3):  # Check if all x values are the same
        return True, None, x[0], 1.0  # Return that it's a vertical line with x = constant

    # Perform linear regression to calculate slope, intercept, and R-squared value
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    r2 = r_value ** 2  # Calculate R-squared value (coefficient of determination)
    
    # Return if the line is linear (R-squared >= threshold) and the line parameters
    return (r2 >= threshold, slope, intercept, r2)


def are_perpendicular(m1, m2):
    """
    Check if two lines with slopes m1 and m2 are perpendicular.
    
    m1: Slope of the first line
    m2: Slope of the second line
    
    Returns True if the lines are perpendicular, False otherwise.
    """
    # Handle vertical lines (slope=None)
    if m1 is None and m2 == 0:  # One line is vertical and the other is horizontal
        return True
    if m2 is None and m1 == 0:  # One line is horizontal and the other is vertical
        return True
    if m1 is None or m2 is None:  # Cannot determine perpendicularity if one line is vertical and the other is not
        return False

    # Check if the product of the slopes is approximately -1 (for perpendicular lines)
    return abs(m1 * m2 + 1) < tol  # If the slopes' product is -1 within tolerance, they are perpendicular

def get_intersection(m0, b0, m1, b1):
    """
    Calculate the intersection point of two lines given their slopes and intercepts.
    
    m0, b0: Slope and intercept of the first line
    m1, b1: Slope and intercept of the second line
    
    Returns the (x, y) coordinates of the intersection point.
    """
    # Handle vertical lines (m=None means vertical)
    if m0 is None:  # Line 0 is vertical
        x_int = b0  # x-coordinate is the intercept (constant)
        y_int = m1 * x_int + b1  # Use line 1's equation to calculate y
    elif m1 is None:  # Line 1 is vertical
        x_int = b1  # x-coordinate is the intercept (constant)
        y_int = m0 * x_int + b0  # Use line 0's equation to calculate y
    else:
        # Regular case for non-vertical lines
        x_int = (b1 - b0) / (m0 - m1)  # Calculate x-coordinate of intersection
        y_int = m0 * x_int + b0  # Calculate y-coordinate of intersection using line 0's equation

    return x_int, y_int  # Return the intersection point as (x, y)
