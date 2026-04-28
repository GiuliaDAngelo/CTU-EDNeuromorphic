'''
================================================================================
Tutorial 1A — Time Window for Event-Based Data Visualisation
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

In this script we load and visualise event-based data captured by a Dynamic
Vision Sensor (DVS). Unlike conventional cameras, a DVS records brightness
changes at each pixel independently and asynchronously, providing microsecond
temporal resolution with no redundant data.

We use the 'importIitYarp' function from the 'bimvee' library to load the
event stream and extract its four core attributes per event:
    x   — pixel column
    y   — pixel row
    ts  — timestamp (seconds, microsecond resolution)
    pol — polarity: 1 = ON (brightness increase), 0 = OFF (brightness decrease)

Events are then grouped into fixed-duration time windows and rendered in real
time using OpenCV. Press Q to quit the visualisation.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

from bimvee.importIitYarp import importIitYarp  # Load IIT-YARP event data
import matplotlib                               # Plotting backend
from helpers.helpers import time_window         # Time-window visualisation loop

matplotlib.use('TkAgg')  # Required for interactive OpenCV windows


# ── Parameters ────────────────────────────────────────────────────────────────

width          = 304                             # DVS camera width  (pixels)
height         = 240                             # DVS camera height (pixels)
window_period  = 350                             # Time window duration (ms)
camera_events  = 'right'                         # Camera stream to visualise
codec          = '24bit'                         # Event data encoding format
filePathOrName = 'data/attention-multiobjects/'  # Path to the dataset


# ── Load Events ───────────────────────────────────────────────────────────────

events = importIitYarp(filePathOrName=filePathOrName, codec=codec)


# ── Visualise ─────────────────────────────────────────────────────────────────

time_window(events, camera_events, height, width, window_period)