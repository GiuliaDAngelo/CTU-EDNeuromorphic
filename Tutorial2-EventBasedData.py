'''
================================================================================
Tutorial 2 — Event-Based Data Visualisation (N-MNIST Dataset)
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

In this tutorial we load and visualise event-based data from the N-MNIST dataset.
N-MNIST is the neuromorphic version of the classic MNIST handwritten digit dataset,
recorded by moving a DVS camera in front of an LCD screen displaying each digit.
It is one of the most widely used benchmarks in neuromorphic vision research and
downloads automatically (~13 MB) on first run.

We convert the raw event stream into temporal frames using a fixed time window,
then visualise the positive (ON) and negative (OFF) polarities separately.

Each frame has shape (2, H, W):
    frame[0] — positive events (ON,  brightness increase)
    frame[1] — negative events (OFF, brightness decrease)

--------------------------------------------------------------------------------
HOW TO USE THIS SCRIPT
--------------------------------------------------------------------------------
1. On first run, tonic will automatically download N-MNIST (~13 MB) into
   the 'data/' folder.

2. Search for ### TODO and fill in the missing values.

3. Run the script:
       python Tutorial2_EventBasedData.py

4. Press Q in any visualisation window to move to the next section.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

import os
import tonic                  # Neuromorphic datasets and event transforms
import cv2                    # Real-time visualisation
import numpy as np            # Array operations
import matplotlib             # Plotting backend
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')       # Required for interactive display windows


# ── Step 1: Load the Dataset ──────────────────────────────────────────────────
#
# tonic.datasets.NMNIST downloads and caches the dataset automatically.
# Each sample is one handwritten digit recording from the DVS camera.

dvs_training = tonic.datasets.NMNIST(save_to='data/', train=True)

print(f'Dataset loaded ✓')
print(f'Sensor size:    {dvs_training.sensor_size}')
print(f'Total samples:  {len(dvs_training)}')
print(f'Classes:        {dvs_training.classes}')


# ── Step 2: Select a Sample ───────────────────────────────────────────────────
#
# Each sample is one digit recording.
# Try changing 'number' to explore different digits and subjects.

### TODO: Choose a sample index to visualise.
###       Valid range: 0 to len(dvs_training) - 1
###       Start with 1, then try 5, 10, 67 and compare.
number = 1

events, label = dvs_training[number]

print(f'\nSample {number} loaded ✓')
print(f'Digit label:    {label}')
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

# ### TODO: Set the time window duration in microseconds.
# ###       Start with 10000 (= 10 ms). Then try 5000 and 20000.
time_window = 10000  # microseconds

transform = tonic.transforms.ToFrame(
    sensor_size=dvs_training.sensor_size,
    time_window=time_window
)
frames = transform(events)

print(f'\nTime window:      {time_window} μs')
print(f'Frames generated: {len(frames)}')
print(f'Frame shape:      {frames[0].shape}  (channels, height, width)')


# ── Step 4: Visualise — Side-by-Side Grayscale ────────────────────────────────
#
# ON and OFF event frames displayed side by side as grayscale images.
# White pixels = events occurred, black pixels = silence.
# Press Q to skip to the coloured visualisation.

print('\nShowing grayscale visualisation — press Q to skip...')

num_frames_to_show = 200
sample_interval    = max(1, len(frames) // num_frames_to_show)

fig, ax = plt.subplots(figsize=(10, 4))

for i in range(0, len(frames), sample_interval):
    frame = frames[i]

    concatenated = np.hstack((
        cv2.cvtColor(frame[0].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR),  # ON  events
        cv2.cvtColor(frame[1].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR)   # OFF events
    ))
    rgb_frame = cv2.cvtColor(concatenated, cv2.COLOR_BGR2RGB)

    ax.clear()
    ax.imshow(rgb_frame)
    ax.set_title(f'Frame {i} — Digit: {label} | ON events (left)  OFF events (right)')
    ax.axis('off')
    plt.pause(0.1)

plt.close(fig)
print('Grayscale visualisation complete.')


# ── Step 5: Visualise — Coloured Scatter Plot ─────────────────────────────────
#
# ON events in green, OFF events in red on a black background —
# the standard colour convention in neuromorphic vision.

print('\nShowing coloured scatter visualisation...')

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('black')

for i in range(0, len(frames), sample_interval):
    frame = frames[i]

    ax.clear()
    ax.set_facecolor('black')

    pos_y, pos_x = np.where(frame[0] > 0)
    if len(pos_x) > 0:
        ax.scatter(pos_x, pos_y, c='green', s=2, label='ON events')

    neg_y, neg_x = np.where(frame[1] > 0)
    if len(neg_x) > 0:
        ax.scatter(neg_x, neg_y, c='red', s=2, label='OFF events')

    ax.set_title(f'Frame {i} — Digit: {label}', color='white')
    ax.set_xlim(0, frame.shape[2])
    ax.set_ylim(frame.shape[1], 0)
    ax.set_aspect('equal')
    ax.legend(loc='upper right', fontsize=8)
    ax.axis('off')
    plt.pause(0.1)

plt.close(fig)
print('Scatter visualisation complete.')


# ── Step 6: Quantitative Comparison ──────────────────────────────────────────
#
# Compare how different sample indices and time windows affect the data
# in terms of frame count, event density, and sparsity.

print('\n' + '='*80)
print('Quantitative comparison across configurations')
print('='*80)

test_configs = [
    (1,  5000),
    (1,  10000),
    (1,  20000),
    (5,  10000),
    (10, 10000),
]

def compute_metrics(dataset, trial, tw):
    ev, _ = dataset[trial]
    fr    = tonic.transforms.ToFrame(sensor_size=dataset.sensor_size, time_window=tw)(ev)
    epf   = fr.sum(axis=(1, 2, 3))
    return {
        'sample'       : trial,
        'time_window'  : tw,
        'num_frames'   : len(fr),
        'total_events' : len(ev),
        'mean_epf'     : float(epf.mean()) if len(fr) > 0 else 0.0,
        'std_epf'      : float(epf.std())  if len(fr) > 0 else 0.0,
        'non_empty'    : float((epf > 0).mean()) if len(fr) > 0 else 0.0,
    }

results = [compute_metrics(dvs_training, s, tw) for s, tw in test_configs]

print(f'\n{"sample":>6}  {"tw (μs)":>8}  {"frames":>6}  {"events":>8}  '
      f'{"mean/frame":>10}  {"std/frame":>9}  {"non_empty":>9}')
print('-' * 70)
for r in results:
    print(f'{r["sample"]:>6}  {r["time_window"]:>8}  {r["num_frames"]:>6}  '
          f'{r["total_events"]:>8}  {r["mean_epf"]:>10.2f}  '
          f'{r["std_epf"]:>9.2f}  {r["non_empty"]:>9.2f}')

print('\nInterpretation hints:')
print('- Smaller time_window → more frames, fewer events per frame.')
print('- Larger  time_window → fewer frames, denser frames.')
print('- Changing sample index changes the digit and the recording dynamics.')


# ── Exercise ──────────────────────────────────────────────────────────────────
#
# GOAL: Compute the total number of events and the sparsity for sample index 67.
#
# Sparsity (%) = percentage of pixels that generated NO events across all frames.
# A high sparsity means most of the sensor was silent — typical for event cameras.

print('\n' + '='*80)
print('Exercise — sample index 67')
print('='*80 + '\n')

ex_events, ex_label = dvs_training[67]
ex_frames = tonic.transforms.ToFrame(
    sensor_size=dvs_training.sensor_size,
    time_window=10000
)(ex_events)

## TODO: Compute the total number of events for sample 67.
##       Hint: len(ex_events)
total_events = None

## TODO: Compute the sparsity as the percentage of zero pixels across all frames.
##       Hint: sparsity = (np.sum(ex_frames == 0) / ex_frames.size) * 100
sparsity = None

if total_events is None:
    raise NotImplementedError('TODO: compute total_events for sample 67.')
if sparsity is None:
    raise NotImplementedError('TODO: compute sparsity (%) for sample 67.')

print(f'Sample index:   67  (digit: {ex_label})')
print(f'Total events:   {total_events}')
print(f'Sparsity:       {sparsity:.2f}%')


# ── Question ──────────────────────────────────────────────────────────────────
#
# Try different values for 'number' and 'time_window' above, then answer:
#
# Q. How do changes to time_window affect the number of frames and the density
#    of events per frame? What are the trade-offs for a real-time robot system?
#
# ANSWER: ???