"""

Giulia D'Angelo, giulia.dangelo@fel.cvut.cz

Event-Based Vision: Sliding Window Visualization

This script processes event-based vision data from a Dynamic Vision Sensor (DVS).
It loads event data, applies a sliding time window, and visualizes positive and
negative events separately.

Key Concepts:
- **Event-based vision**: Unlike conventional cameras, a DVS captures changes
  in the scene asynchronously, storing pixel locations, timestamps, and polarities.
- **Sliding time window**: A fixed-duration window of events is displayed,
  continuously updating over time to show the most recent activity.

Steps:
1. Load event data from the Bimvee library.
2. Initialize matrices for tracking positive and negative events.
3. Process events within an initial time window.
4. Apply a sliding window to continuously update the visualization.
5. Display the processed events in real time using OpenCV.
"""

from bimvee.importIitYarp import importIitYarp
import matplotlib
from helpers.helpers import sliding_window

# Set the backend for Matplotlib to 'TkAgg' to enable interactive plotting
matplotlib.use('TkAgg')

# Define camera parameters (resolution of the sensor)
width = 304
height = 240
initial_window_period = 300  # Initial time window in milliseconds
sliding_wdw = 100          # Sliding window duration in milliseconds
time_buff = sliding_wdw # Buffer for managing event updates

# Load event data from the specified file
camera_events = 'right'  # Specify the camera side ('left' or 'right')
codec = '24bit'  # Codec format for event data
filePathOrName = 'data/attention-multiobjects/'  # Path to event dataset
events = importIitYarp(filePathOrName=filePathOrName, codec=codec)

sliding_window(events, camera_events, height, width, initial_window_period, sliding_wdw, time_buff)
