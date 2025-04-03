# In this script, we will load and visualize event-based data captured by an event camera.
# The event camera records changes in the scene over time, allowing us to capture dynamic events
# with high temporal resolution. We will utilize the 'importIitYarp' function from the 'bimvee'
# library to load the event data, and then extract the x and y coordinates, timestamps, and
# polarities of the events. Finally, we will visualize the events in an interactive manner,
# displaying them in real-time within specified time windows.

# Import the function 'importIitYarp' from the 'bimvee' library to load event-based camera data
from bimvee.importIitYarp import importIitYarp

# Import necessary libraries for plotting and numerical operations
import matplotlib
import numpy as np
import cv2
from collections import deque
from helpers.helpers import time_window

# Set the backend for Matplotlib to 'TkAgg' to enable interactive plotting
matplotlib.use('TkAgg')

# Define the dimensions of the event-based camera (304 pixels width by 240 pixels height)
width = 304
height = 240
# Define the fixed time window for event visualization (in milliseconds)
window_period = 10  # ms
# Define the camera from which events will be extracted ('right' camera)
camera_events = 'right'
# Specify the codec format used for decoding the event data ('24bit' format)
codec = '24bit'
# Set the file path where the event data is stored
filePathOrName = 'data/attention-multiobjects/'
# Load the event data using the 'importIitYarp' function
events = importIitYarp(
    filePathOrName=filePathOrName,  # Path to the dataset
    codec=codec)  # Codec to decode the event data

time_window(events, camera_events,height, width,window_period)
