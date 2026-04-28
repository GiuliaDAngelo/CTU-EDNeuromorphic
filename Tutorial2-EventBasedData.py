#!/usr/bin/env python3
"""

Tutorial 2 - Event-Based Data (DVSGesture)

In this script, we load and visualize event-based data from the **DVSGesture** dataset using `tonic`.

The events are converted into frame slices over a fixed time window, then displayed as positive and negative polarities side by side.
"""

# ============================================================================
# 1. Import libraries
# ============================================================================
# We import `tonic` for neuromorphic datasets/transforms, `cv2` for visualization,
# and `numpy` for array manipulation.

import tonic
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'



# ============================================================================
# 2. Load DVSGesture events
# ============================================================================
# We select the dataset path and load the training split.
# Then we choose one trial (`user_trial`) to inspect.

# Step 1: Load the Events from the DVSGesture Dataset
# Specify the path to your dataset
path = 'data/'
dvs_training = tonic.datasets.DVSGesture(path, train=True)

# Define parameters for the event processing
time_window = 10000  # Time window in microseconds (10 ms)
user_trial = 1       # Index of the user trial to analyze

# Load events and corresponding numpy data for the specified trial
events, npys = dvs_training[user_trial]


# ============================================================================
# 3. Convert events to frames
# ============================================================================
# Using `tonic.transforms.ToFrame`, events are binned into temporal slices of `time_window` microseconds.
# This gives a sequence of frames with separate channels for positive and negative events.

# Transform events into frames using the specified time window
transform = tonic.transforms.ToFrame(
    sensor_size=dvs_training.sensor_size,
    time_window=time_window  # Convert events to frames based on the time window
)
frames = transform(events)  # Generate frames from events

# Output the number of frames generated
print(f"Number of frames: {len(frames)}")


# ============================================================================
# 4. Visualize positive and negative polarities (Method 1: concatenated frames)
# ============================================================================
# In a script environment, we visualize frames using matplotlib and save or display them.

print("\nVisualizing frames (positive and negative polarities)...")

# Create output directory for frames if desired (optional)
import os
os.makedirs("frames_output", exist_ok=True)

# Display a subset of frames (sampling every 10th frame for quick viewing)
fig, ax = plt.subplots(figsize=(10, 4))
num_frames_to_show = 10
sample_interval = max(1, len(frames) // num_frames_to_show)  # Show ~10 frames

for i in range(0, len(frames), sample_interval):
    frame = frames[i]

    # Concatenate the two polarities into a single frame for visualization
    concatenated_frame = np.hstack((
        cv2.cvtColor(frame[0].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR),  # Positive events
        cv2.cvtColor(frame[1].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR)   # Negative events
    ))

    # Convert BGR to RGB for correct matplotlib colors
    rgb_frame = cv2.cvtColor(concatenated_frame, cv2.COLOR_BGR2RGB)

    ax.clear()
    ax.imshow(rgb_frame)
    ax.set_title(f'Frame {i}: Positive and Negative Polarities')
    ax.axis('off')

    plt.pause(0.1)

plt.close(fig)
print("Frame visualization complete.")


# ============================================================================
# 4b. Visualize both polarities using colored dots (Method 2: scatter plot)
# ============================================================================

print("\nVisualizing events as colored scatter dots...")

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

sample_interval = max(1, len(frames) // num_frames_to_show)  

for i in range(0, len(frames), sample_interval):
    frame = frames[i]

    ax.clear()
    ax.set_facecolor('black')

    # Positive events in green.
    pos_y, pos_x = np.where(frame[0] > 0)
    if len(pos_x) > 0:
        ax.scatter(pos_x, pos_y, c='green', s=2, label='Positive events')

    # Negative events in red.
    neg_y, neg_x = np.where(frame[1] > 0)
    if len(neg_x) > 0:
        ax.scatter(neg_x, neg_y, c='red', s=2, label='Negative events')

    ax.set_title(f'Frame {i}: Positive and Negative Events')
    ax.set_xlim(0, frame.shape[2])
    ax.set_ylim(frame.shape[1], 0)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.axis('off')

    plt.pause(0.1)

plt.close(fig)
print("Event visualization complete.")


# ============================================================================
# 5. Quantitative experiment: user_trial and time_window
# ============================================================================
# Try experimenting with different values for `user_trial` and `time_window`.
# How do these changes affect the visualization and interpretation of the data?

print("\n" + "="*100)
print("Quantitative Experiment: Comparing different (user_trial, time_window) configurations")
print("="*100)

test_configs = [
    (1, 5000),
    (1, 10000),
    (1, 20000),
    (5, 10000),
    (10, 10000),
]

def compute_metrics(dataset, trial, tw):
    """Compute quantitative metrics for a given trial and time window."""
    ev, _ = dataset[trial]
    tr = tonic.transforms.ToFrame(
        sensor_size=dataset.sensor_size,
        time_window=tw
    )
    fr = tr(ev)

    events_per_frame = fr.sum(axis=(1, 2, 3))
    num_frames = int(len(fr))
    total_events = int(len(ev))
    mean_events_per_frame = float(events_per_frame.mean()) if num_frames > 0 else 0.0
    std_events_per_frame = float(events_per_frame.std()) if num_frames > 0 else 0.0
    non_empty_ratio = float((events_per_frame > 0).mean()) if num_frames > 0 else 0.0

    return {
        "user_trial": trial,
        "time_window_us": tw,
        "num_frames": num_frames,
        "total_events": total_events,
        "mean_events_per_frame": mean_events_per_frame,
        "std_events_per_frame": std_events_per_frame,
        "non_empty_frame_ratio": non_empty_ratio,
    }

results = [compute_metrics(dvs_training, trial, tw) for trial, tw in test_configs]

print("\nNumerical comparison across configurations:\n")
for row in results:
    print(
        f"trial={row['user_trial']:>2}, tw={row['time_window_us']:>5} us | "
        f"frames={row['num_frames']:>4}, total_events={row['total_events']:>7}, "
        f"mean/frame={row['mean_events_per_frame']:.2f}, std/frame={row['std_events_per_frame']:.2f}, "
        f"non_empty_ratio={row['non_empty_frame_ratio']:.2f}"
    )

print("\nInterpretation hints:")
print("- Smaller time_window -> usually more frames, fewer events per frame.")
print("- Larger time_window  -> usually fewer frames, denser frames (more events/frame).")
print("- Changing user_trial may change total activity and temporal dynamics.")


# ============================================================================
# 6. Exercise: Quantify total events and sparsity for user_trial = 67
# ============================================================================
# GOAL: Quantify the **total number of events** and the **sparsity** for `user_trial = 67`.
#
# Expected Output:
# - `total events` (integer);
# - `sparsity (%)` in [0, 100].

print("\n" + "="*100)
print("EXERCISE: Compute metrics for user_trial = 67")
print("="*100 + "\n")

# TODO: compute the total number of events and the sparsity for the specific user_trial
user_trial = 67
time_window_exercise = 10000


# Total number of events
total_events = None

# Sparsity calculation
sparsity = None

if total_events is None:
    raise NotImplementedError("Please compute the total number of events for user_trial = 67.")
if sparsity is None:
    raise NotImplementedError("Please compute the sparsity (%) for user_trial = 67.")

print(f"Total number of events: {total_events}")
print(f"Sparsity: {sparsity:.2f}%")


# ============================================================================
# 7. Questions for further exploration
# ============================================================================
print("\n" + "="*100)
print("Questions for further exploration:")
print("="*100)
print("1. Try experimenting with different values for **user_trial** and **time_window**.")
print("   How do these changes affect the visualization and interpretation of the data?")
print("\nTip: Modify the values at the beginning of this script and re-run to experiment.")
