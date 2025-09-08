
# helper functions

def map_range(x, in_min, in_max, out_min, out_max):
    """Re-maps a number from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def clamp(value, min_val, max_val):
    """Clamps a value between min_val and max_val."""
    return max(min_val, min(max_val, value))

def steer(servo,a):
	a=map_range(a,-75,75,30,180)
	a=clamp(a,30,180)
	servo.set(a)
