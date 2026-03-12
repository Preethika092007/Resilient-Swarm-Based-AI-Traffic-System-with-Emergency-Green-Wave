"""
Configuration constants for the Traffic Signal Optimization module.
"""

# Base green time in seconds
BASE_TIME = 10

# Factor to multiply priority score by to get additional green time
PRIORITY_FACTOR = 2

# Maximum green time allowed for a single lane to prevent starvation
MAX_GREEN_TIME = 90

# Emergency override time
EMERGENCY_GREEN_TIME = 60
