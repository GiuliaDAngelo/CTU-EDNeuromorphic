"""

Giulia D'Angelo, giulia.dangelo@fel.cvut.cz

This script implements a saliency-based attention mechanism using event-driven data.
It processes a series of events representing two objects, visualizing their spatial attention
through a saliency map. The attention mechanism is designed to highlight the most significant
features of the scene, using configurable parameters that define the characteristics of the
attention arcs and kernels.

The script leverages PyTorch for efficient tensor operations and OpenCV for real-time visualization
of the saliency maps. The primary steps include loading event data, initializing the attention
network, and iterating through the events to update and visualize the saliency map in response
to incoming data.

Key components:
- `Config`: A class that holds the parameters for the attention mechanism.
- `initialise_attention`: A helper function to set up the attention network.
- `run_attention`: A function that computes the saliency map based on the current window of events.

This implementation aims to demonstrate how attention mechanisms can be applied to dynamic
visual data, enabling robots and systems to focus on relevant features in real-time.
"""

import numpy as np
from helpers.helpers import initialise_attention, run_attention
import torch
import cv2


# Configuration class to store attention parameters
class Config:
    # Attention Parameters
    ATTENTION_PARAMS = {
        'size_krn': 16,  # Size of the kernel used in the attention mechanism
        'r0': 14,  # Radius shift from the center for the attention arc
        'rho': 0.05,  # Scale coefficient to control the arc length
        'theta': np.pi * 3 / 2,  # Angle to control the orientation of the arc
        'thetas': np.arange(0, 2 * np.pi, np.pi / 4),  # Array of angles for multi-directional attention
        'thick': 3,  # Thickness of the arc in the attention map
        'fltr_resize_perc': [2, 2],  # Resize percentage for filters
        'offsetpxs': 0,  # Offset in pixels (half the size of the kernel)
        'offset': (0, 0),  # Offset for attention positioning
        'num_pyr': 6,  # Number of pyramid levels in the attention network
        'tau_mem': 0.3,  # Memory time constant for the attention mechanism
        'stride': 1,  # Stride for attention processing
        'out_ch': 1  # Number of output channels
    }


# Set the device for PyTorch (using Metal Performance Shaders on macOS if available)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Initialize the configuration
config = Config()

# Load event data from a .npy file containing two objects
data = np.load('data/twoobjects/twoobjects.npy')

# Extract coordinates and properties from the data
x, y, p, t = data[:, 0].astype(int), data[:, 1].astype(int), data[:, 2], data[:, 3] * 1e3

# Determine the resolution based on the maximum coordinates
max_x = x.max() + 1  # Maximum x coordinate + 1 for resolution
max_y = y.max() + 1  # Maximum y coordinate + 1 for resolution
resolution = (max_y, max_x)  # Resolution tuple for attention processing

# Initialize saliency map and coordinates for maximum saliency
saliency_map = np.zeros((max_y, max_x), dtype=np.float32)  # Saliency map initialized to zero
salmax_coords = np.zeros((2,), dtype=np.int32)  # Array to hold coordinates of maximum saliency

##### Attention Mechanism #####
# Initialize the attention modules with the specified device and parameters
net_attention = initialise_attention(device, config.ATTENTION_PARAMS)

# Set the time window period for processing events (in milliseconds)
window_period = 100  # Time window in milliseconds
time = window_period  # Initialize the time variable
window = torch.zeros((1, max_y, max_x), dtype=torch.float32)  # Create a tensor to hold the current window of events

# Iterate through the event data
for xi, yi, pi, ti in zip(x, y, p, t):
    if ti <= time:
        # If the event time is within the current time window, update the window
        window[0][yi][xi] = 255  # Mark the pixel corresponding to the event
    else:
        # If the event time exceeds the current time window, process the attention
        saliency_map[:], salmax_coords[:] = run_attention(window, net_attention, device, resolution,
                                                          config.ATTENTION_PARAMS['num_pyr'])

        # Apply a color map to the window for better visualization
        window_map_jet = cv2.applyColorMap(window.detach().cpu().numpy().squeeze(0).astype(np.uint8), cv2.COLORMAP_JET)
        # Add a title to the visualization
        cv2.putText(window_map_jet, 'Events map', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2, cv2.LINE_AA)

        # Draw a circle at the location of maximum saliency on the visualization
        cv2.circle(window_map_jet, (salmax_coords[1], salmax_coords[0]), 6, (255, 255, 255), 4)
        cv2.putText(window_map_jet, 'Visual Attention', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, cv2.LINE_AA)

        # Display the events map and saliency map
        cv2.imshow('Events map and Saliency Map', window_map_jet)

        # Wait for a key press to update the display
        cv2.waitKey(1)

        # Increment the time by the window period for the next iteration
        time += window_period

        # Reset the window for the next time period
        window = torch.zeros((1, max_y, max_x), dtype=torch.float32)

# Clean up by closing the OpenCV window after processing all events
cv2.destroyAllWindows()
