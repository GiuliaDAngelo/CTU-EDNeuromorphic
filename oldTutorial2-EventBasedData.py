'''
================================================================================
Tutorial 2 — Event-Based Data Visualisation (DVSGesture Dataset)
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

In this tutorial we load and visualise event-based data from the DVSGesture
dataset. This dataset was recorded using a Dynamic Vision Sensor (DVS) and
contains 11 hand gesture classes performed under different lighting conditions.
It is one of the standard benchmarks in neuromorphic vision research.

We convert the raw event stream into temporal frames using a fixed time window,
then visualise the positive (ON) and negative (OFF) polarities separately.

Each frame has shape (2, H, W):
    frame[0] — positive events (ON,  brightness increase)
    frame[1] — negative events (OFF, brightness decrease)

--------------------------------------------------------------------------------
HOW TO USE THIS SCRIPT
--------------------------------------------------------------------------------
1. On first run, tonic will automatically download the DVSGesture dataset
   (~1.4 GB) into the 'data/' folder. This may take a few minutes depending
   on your connection — run it ahead of the tutorial session.

2. Search for ### TODO and fill in the missing values.

3. Run the script:
       python Tutorial2_EventBasedData.py

4. Press Q in the visualisation window to quit.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

import tonic                  # Neuromorphic datasets and event transforms
import cv2                    # Real-time visualisation
import numpy as np            # Array operations
import matplotlib             # Plotting backend
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')       # Required for interactive display windows


# ── Step 1: Load the Dataset ──────────────────────────────────────────────────
#
# tonic.datasets.DVSGesture downloads and caches the dataset automatically.
# On first run this will take a few minutes — subsequent runs are instant.

path = 'data/'
dvs_training = tonic.datasets.DVSGesture(path, train=True)

print(f'Dataset loaded ✓')
print(f'Sensor size:    {dvs_training.sensor_size}')
print(f'Total trials:   {len(dvs_training)}')
print(f'Classes:        {dvs_training.classes}')


# ── Step 2: Select a Trial ────────────────────────────────────────────────────
#
# Each trial is one recording of a single gesture.
# Try changing user_trial to explore different gestures and subjects.

### TODO: Choose a trial index to visualise.
###       Valid range: 0 to len(dvs_training) - 1
###       Start with 1, then try 5, 10, 67 and compare.
user_trial = 67

events, label = dvs_training[user_trial]

print(f'\nTrial {user_trial} loaded ✓')
print(f'Gesture label:  {label}')
print(f'Total events:   {len(events)}')
print(f'Event dtype:    {events.dtype}')


# ── Step 3: Convert Events to Frames ─────────────────────────────────────────
#
# tonic.transforms.ToFrame bins the asynchronous event stream into temporal
# slices of duration time_window microseconds.
# Each slice becomes one frame with two channels: ON events and OFF events.
#
# Smaller time_window → more frames, fewer events per frame (finer detail)
# Larger  time_window → fewer frames, denser frames (smoother but less precise)

### TODO: Set the time window duration in microseconds.
###       Start with 10000 (= 10 ms). Then try 5000 and 20000.
time_window = 10000  # microseconds

transform = tonic.transforms.ToFrame(
    sensor_size=dvs_training.sensor_size,
    time_window=time_window
)
frames = transform(events)

print(f'\nTime window:    {time_window} μs')
print(f'Frames generated: {len(frames)}')
print(f'Frame shape:    {frames[0].shape}  (channels, height, width)')


# ── Step 4: Visualise — Side-by-Side Grayscale ────────────────────────────────
#
# We display ON and OFF event frames side by side as grayscale images.
# White pixels indicate where events occurred; black pixels are silent.
# Press Q to skip to the coloured visualisation.

print('\nShowing grayscale visualisation — press Q to skip...')

for i, frame in enumerate(frames):
    concatenated = np.hstack((
        cv2.cvtColor(frame[0].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR),  # ON  events
        cv2.cvtColor(frame[1].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR)   # OFF events
    ))
    cv2.imshow('ON events (left)  |  OFF events (right)', concatenated)
    key = cv2.waitKey(30)
    if key == ord('q'):
        break

cv2.destroyAllWindows()


# ── Step 5: Visualise — Coloured Scatter Plot ─────────────────────────────────
#
# A more intuitive representation: ON events in green, OFF events in red,
# on a black background — the standard colour convention in neuromorphic vision.

print('\nShowing coloured scatter visualisation...')

plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('black')

for i, frame in enumerate(frames):
    ax.clear()
    ax.set_facecolor('black')

    # ON events — green
    pos_y, pos_x = np.where(frame[0] > 0)
    ax.scatter(pos_x, pos_y, c='green', s=2, label='ON events')

    # OFF events — red
    neg_y, neg_x = np.where(frame[1] > 0)
    ax.scatter(neg_x, neg_y, c='red', s=2, label='OFF events')

    ax.set_title(f'Frame {i} — Gesture: {label}', color='white')
    ax.set_xlim(0, frame.shape[2])
    ax.set_ylim(frame.shape[1], 0)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.pause(0.03)

plt.ioff()
plt.close(fig)


# ── Exercise ──────────────────────────────────────────────────────────────────
#
# GOAL: Quantify the total number of events and the sparsity for user_trial = 67.
#
# Sparsity (%) = percentage of pixels that generated NO events across all frames.
# A high sparsity means most of the sensor was silent — typical for event cameras.
#
# Expected output:
#   total_events  (integer)
#   sparsity      (float, between 0 and 100)

exercise_trial = 67
ex_events, ex_label = dvs_training[exercise_trial]
ex_frames = transform(ex_events)

### TODO: Compute the total number of events in this trial.
###       Hint: len(ex_events) gives you the total number of events directly.
total_events = None

### TODO: Compute the sparsity as the percentage of zero pixels across all frames.
###       Hint: sparsity = (number of zero pixels / total pixels) * 100
###       Total pixels = num_frames * height * width * 2 channels
###       Zero pixels  = pixels where ex_frames == 0
sparsity = None

if total_events is None or sparsity is None:
    raise NotImplementedError("TODO: compute total_events and sparsity above")

print(f'\nExercise results for trial {exercise_trial} (gesture: {ex_label}):')
print(f'Total events: {total_events}')
print(f'Sparsity:     {sparsity:.2f}%')


# ── Question ──────────────────────────────────────────────────────────────────
#
# Try different values for user_trial and time_window above, then answer:
#
# Q. How do changes to time_window affect the number of frames and the density
#    of events per frame? What are the trade-offs for a real-time robot system?
#
# ANSWER: ???
#
# ── Experiments ───────────────────────────────────────────────────────────────
#
# - Print events.dtype to see the structured array format (x, y, t, p)
# - Count how many ON vs OFF events exist: np.sum(events['p'] == 1)
# - Try time_window = 1000 (1 ms) — what happens to the frames?