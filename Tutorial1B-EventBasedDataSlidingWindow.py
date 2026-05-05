'''
================================================================================
Tutorial 1B — Sliding Window for Event-Based Data Visualisation
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

In this script we extend the fixed time window approach from Tutorial 1A with
a SLIDING window. Rather than resetting at the end of each interval, the window
moves forward continuously — old events are removed as new ones arrive, giving
a smooth, temporally consistent view of scene activity.

Two parameters control the behaviour:
    initial_window_period — how many milliseconds of events are held at once
    sliding_wdw           — how far the window advances at each step (ms)

A smaller sliding_wdw gives smoother motion but higher computational cost.
A larger one is faster but produces a more flickering visualisation.

Press Q to quit the visualisation.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

from bimvee.importIitYarp import importIitYarp  # Load IIT-YARP event data
import matplotlib                               # Plotting backend
from helpers.helpers import sliding_window      # Sliding-window visualisation loop

matplotlib.use('TkAgg')  # Required for interactive OpenCV windows


# ── Parameters ────────────────────────────────────────────────────────────────

width                = 304    # DVS camera width  (pixels)
height               = 240    # DVS camera height (pixels)
initial_window_period = 100   # Initial time window size (ms)
sliding_wdw          = 100     # Step size the window advances each update (ms)
time_buff            = sliding_wdw  # Internal buffer — initialised to sliding_wdw

camera_events        = 'right'                        # Camera stream to visualise
codec                = '24bit'                        # Event data encoding format
filePathOrName       = 'data/attention-multiobjects/' # Path to the dataset


# ── Load Events ───────────────────────────────────────────────────────────────

events = importIitYarp(filePathOrName=filePathOrName, codec=codec)


# ── Visualise ─────────────────────────────────────────────────────────────────

sliding_window(events, camera_events, height, width, initial_window_period, sliding_wdw, time_buff)