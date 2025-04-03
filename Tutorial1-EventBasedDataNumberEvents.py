"""
Event-Based Vision: Fixed Event Count Visualization

This script processes event-based vision data from a Dynamic Vision Sensor (DVS). 
Unlike traditional frame-based cameras, a DVS captures changes in brightness at 
individual pixels asynchronously, providing high temporal resolution and efficiency.

Instead of using a time-based sliding window, this implementation groups events 
into fixed-size batches (e.g., 1000 events per window) and visualizes them in real time.

Key Concepts:
- **Event-based vision**: A DVS captures changes in the scene asynchronously, storing 
  pixel locations, timestamps, and polarities (ON/OFF events).
- **Fixed event count visualization**: Instead of a time window, the script processes 
  a set number of events at a time for visualization.

Steps:
1. Load event data using the `importIitYarp` function from the Bimvee library.
2. Define camera parameters (resolution, event count window).
3. Process and visualize events in batches, updating the display dynamically.
"""

# Import the function 'importIitYarp' from the 'bimvee' library to load event-based camera data
from bimvee.importIitYarp import importIitYarp

# Import necessary libraries for plotting and numerical operations
import matplotlib
from helpers.helpers import number_events  # Import function to process a fixed number of events

# Set the backend for Matplotlib to 'TkAgg' to enable interactive plotting
matplotlib.use('TkAgg')

# Define the dimensions of the event-based camera (304 pixels width by 240 pixels height)
width = 304
height = 240

# Define the camera from which events will be extracted ('right' camera)
camera_events = 'right'

# Specify the codec format used for decoding the event data ('24bit' format)
codec = '24bit'

# Set the file path where the event data is stored
filePathOrName = 'data/attention-multiobjects/'

# Load the event data using the 'importIitYarp' function
events = importIitYarp(
    filePathOrName=filePathOrName,  # Path to the dataset
    codec=codec  # Codec to decode the event data
)

# Define the number of events per visualization window
num_events = 10

# Process and visualize events in batches of 'num_events'
number_events(events, camera_events, height, width, num_events)
