'''
================================================================================
Tutorial 1A — Exercise: Coloured Time Window Visualisation
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

In the main tutorial you visualised ON and OFF events as white pixels on two
separate grayscale frames displayed side by side.

In this exercise you will implement a SINGLE coloured frame where:
    ON  events (polarity = 1) → displayed in BLUE
    OFF events (polarity = 0) → displayed in RED

This is the standard colour convention used in the neuromorphic vision community
and gives a much more intuitive read of scene dynamics at a glance.

--------------------------------------------------------------------------------
YOUR TASK
--------------------------------------------------------------------------------
Complete the function 'time_window_colour' below.
It has the same signature and logic as the original time_window(), but instead
of two separate grayscale windows, it uses a single RGB frame.

Sections marked ### TODO require your implementation.
Everything else is provided — do not modify it.

Once complete, run the script and compare your output with the original.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

from bimvee.importIitYarp import importIitYarp
import matplotlib
import numpy as np
import cv2

matplotlib.use('TkAgg')


# ── Parameters ────────────────────────────────────────────────────────────────

width          = 304
height         = 240
window_period  = 50                             # ms — try changing this!
camera_events  = 'right'
codec          = '24bit'
filePathOrName = 'data/attention-multiobjects/'


# ── Load Events ───────────────────────────────────────────────────────────────

events = importIitYarp(filePathOrName=filePathOrName, codec=codec)


# ── Exercise: Implement the Coloured Time Window ──────────────────────────────
#
# HINT: In the original time_window(), two separate arrays store ON and OFF
# events and are displayed with np.hstack(). Here you need a single BGR frame
# of shape (height, width, 3) — OpenCV uses BGR, not RGB, so:
#     Blue  = [255,   0,   0]
#     Red   = [  0,   0, 255]
#
# The rest of the logic (time check, window reset, cv2.imshow) stays the same.

def time_window_colour(events, camera_events, height, width, window_period):
    # Extract event attributes
    e_x   = events['data'][camera_events]['dvs']['x']
    e_y   = events['data'][camera_events]['dvs']['y']
    e_ts  = np.multiply(events['data'][camera_events]['dvs']['ts'], 10 ** 3)
    e_pol = events['data'][camera_events]['dvs']['pol']

    time = window_period

    ### TODO 1: Create a single colour frame of shape (height, width, 3)
    ###         initialised to zeros (black background).
    ###         Hint: np.zeros((height, width, 3), dtype=np.uint8)
    # frame = ???

    # Loop through all events
    # for x, y, ts, pol in zip(e_x, e_y, e_ts, e_pol):

        # if ts <= time:
        #     ### TODO 2: If polarity is ON, set the pixel to BLUE.
        #     ###         If polarity is OFF, set the pixel to RED.
        #     # if pol == 1:
        #     #     frame[y, x] = ???
        #     # else:
        #     #     frame[y, x] = ???
        #
        # else:
        #     ### TODO 3: Display the frame using cv2.imshow
        #     cv2.waitKey(1)
        #     time += window_period
        #
        #     ### TODO 4: Reset the frame to black (all zeros) for the next window.
        #     # ????


# ── Run ───────────────────────────────────────────────────────────────────────

time_window_colour(events, camera_events, height, width, window_period)


# ── Questions ─────────────────────────────────────────────────────────────────
#
# Q1. Why does OpenCV use BGR instead of RGB?
#     Does it affect what you need to write in the pixel assignment?
#
# Q2. What does a frame with mostly BLUE pixels tell you about the scene?
#     What about mostly RED pixels?
#
# Q3. Try changing window_period to 100 ms and 1000 ms.
#     How does the colour balance between ON and OFF events change?
#
# ── Extension (optional) ──────────────────────────────────────────────────────
#
# Once your basic implementation works, try this:
# - Draw a small circle (cv2.circle) at the location of the most recent ON event
#   to track where activity is happening in real time.
# - Add a counter that prints the number of ON and OFF events per window to the
#   terminal.
