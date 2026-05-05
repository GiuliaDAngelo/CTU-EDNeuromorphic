'''
================================================================================
Tutorial 1C — Fixed Event Count for Event-Based Data Visualisation
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

In Tutorials 1A and 1B, events were grouped by time. Here we take a different
approach: instead of asking "what happened in the last N milliseconds?", we ask
"what do the next N events look like?".

This fixed-count approach processes a set number of events per visualisation
frame regardless of how much time they span. In a busy scene, N events may
cover only a few microseconds; in a quiet scene, the same N events may span
several seconds.

This makes fixed-count windows naturally adaptive to scene activity — a useful
property for downstream processing such as spiking neural networks, which often
expect fixed-size inputs.

Press Q to quit the visualisation.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

from bimvee.importIitYarp import importIitYarp  # Load IIT-YARP event data
import matplotlib                               # Plotting backend
from helpers.helpers import number_events       # Fixed-count visualisation loop

matplotlib.use('TkAgg')  # Required for interactive OpenCV windows


# ── Parameters ────────────────────────────────────────────────────────────────

width          = 304                             # DVS camera width  (pixels)
height         = 240                             # DVS camera height (pixels)
num_events     = 100                             # Number of events per frame
camera_events  = 'right'                         # Camera stream to visualise
codec          = '24bit'                         # Event data encoding format
filePathOrName = 'data/attention-multiobjects/'  # Path to the dataset


# ── Load Events ───────────────────────────────────────────────────────────────

events = importIitYarp(filePathOrName=filePathOrName, codec=codec)


# ── Visualise ─────────────────────────────────────────────────────────────────

number_events(events, camera_events, height, width, num_events)