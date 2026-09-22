"""
Configuration and constants for the Evacuation Simulator.
"""

# ============================================
# GRID SETTINGS
# ============================================
GRID_SIZE = 100          # Grid dimensions (100x100 cells)
CELL_SIZE = 0.5          # Cell size in meters (0.5m x 0.5m)

# ============================================
# SIMULATION SETTINGS
# ============================================
SIMULATION_TIMESTEP = 0.1    # Seconds per simulation step
MAX_SIMULATION_TIME = 600    # Maximum simulation time (10 minutes)
PERSON_SPEED = 1.2           # Average walking speed (m/s)
PERSON_SPEED_PANIC = 1.8     # Speed when panicking (m/s)

# ============================================
# FIRE SETTINGS
# ============================================
FIRE_SPREAD_RATE = 0.05      # Fire spread probability per step
SMOKE_SPREAD_RATE = 0.08     # Smoke spread probability per step
FIRE_DANGER_RADIUS = 5       # Cells around fire that are dangerous

# ============================================
# FILE PATHS
# ============================================
FLOORPLAN_DIR = "data/floorplans/"
OUTPUT_DIR = "data/outputs/"

# ============================================
# COLORS (for visualization)
# ============================================
COLOR_FLOOR = "#F5F5F5"
COLOR_WALL = "#333333"
COLOR_EXIT = "#00AA00"
COLOR_FIRE = "#FF0000"
COLOR_SMOKE = "#888888"
COLOR_PERSON = "#0066CC"
