'''
================================================================================
Tutorial 5 — Event-Based Spiking Visual Attention
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

When we look at a scene, we do not process everything equally. The brain
selectively routes processing resources toward the most relevant regions —
a mechanism called VISUAL ATTENTION. Computationally, this is modelled by
computing a SALIENCY MAP: a 2D score over the image where high values indicate
regions likely to attract attention.

The model here is inspired by the proto-object saliency framework (Russell et
al., Vision Research, 2014): early visual processing groups nearby features
into coherent regions — proto-objects — before recognition. Saliency emerges
from competition between these grouped regions.

Implementation details:
- Von Mises filters at 8 orientations mimic orientation-tuned V1 neurons
- Filters are applied across a 6-level spatial pyramid (multi-scale)
- Outputs are summed into a single saliency map
- LIF neurons replace static normalisation, adding temporal integration
- This makes the pipeline directly compatible with DVS event camera output

--------------------------------------------------------------------------------
HOW TO USE THIS SCRIPT
--------------------------------------------------------------------------------
1. Download the dataset from Dropbox and place it at data/twoobjects/twoobjects.npy:
   https://www.dropbox.com/scl/fi/bt7l382p1b7ouau5x07tb/twoobjects.npy

2. This script has TWO tasks:
   Task 1 — Run the basic attention pipeline (fully provided)
   Task 2 — Implement inhibition of return (one TODO to complete)

3. Run the script:
       python Tutorial5_EventBasedVisualAttention.py

4. Press Q in the visualisation window to quit.
================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
import torch
import cv2
import torchvision
import matplotlib

from helpers.helpers import initialise_attention, run_attention

matplotlib.use('TkAgg')

# Device selection: GPU > Apple MPS > CPU
device = (
    torch.device('cuda')  if torch.cuda.is_available()          else
    torch.device('mps')   if torch.backends.mps.is_available()  else
    torch.device('cpu')
)
print(f'Using device: {device}')


# ── Attention Parameters ──────────────────────────────────────────────────────

class Config:
    ATTENTION_PARAMS = {
        'size_krn'       : 16,                          # Kernel size for Von Mises filters
        'r0'             : 14,                          # Radius shift from centre for attention arc
        'rho'            : 0.05,                        # Scale coefficient — controls arc length
        'theta'          : np.pi * 3 / 2,               # Base orientation angle
        'thetas'         : np.arange(0, 2*np.pi, np.pi/4),  # 8 filter orientations
        'thick'          : 3,                           # Arc thickness in the attention map
        'fltr_resize_perc': [2, 2],                     # Filter resize percentage
        'offsetpxs'      : 0,                           # Pixel offset (half kernel size)
        'offset'         : (0, 0),                      # Attention positioning offset
        'num_pyr'        : 6,                           # Spatial pyramid levels
        'tau_mem'        : 0.3,                         # LIF membrane time constant
        'stride'         : 1,                           # Convolution stride
        'out_ch'         : 1                            # Number of output channels
    }


# ── Load Event Data ───────────────────────────────────────────────────────────
#
# The dataset contains events from a scene with two moving objects.
# Each event: (x, y, polarity, timestamp_ms)

data = np.load('data/twoobjects/twoobjects.npy')

x, y, p, t = (
    data[:, 0].astype(int),
    data[:, 1].astype(int),
    data[:, 2],
    data[:, 3] * 1e3       # Convert timestamps to milliseconds
)

max_x      = x.max() + 1
max_y      = y.max() + 1
resolution = (max_y, max_x)

print(f'Events loaded ✓  |  Resolution: {max_x} x {max_y}  |  Total events: {len(x)}')

# Quick preview — first 100 ms of events
m       = (t >= t[0]) & (t < t[0] + 100)
preview = np.zeros((max_y, max_x))
preview[y[m], x[m]] = np.where(p[m] > 0, 1, -1)
plt.figure()
plt.imshow(preview, cmap='bwr', vmin=-1, vmax=1)
plt.title('Event Data Preview — First 100 ms  (blue=ON, red=OFF)')
plt.colorbar()
plt.show(block=False)
plt.pause(0.5)


# ── Task 1: Basic Attention Pipeline ─────────────────────────────────────────
#
# For each time window of window_period ms:
#   1. Accumulate events into a 2D frame
#   2. Run the Von Mises attention network → saliency map
#   3. Find the most salient location (salmax_coords)
#   4. Display events map and saliency map side by side
#
# Play with window_period — how does it affect the saliency computation?

config        = Config()
net_attention = initialise_attention(device, config.ATTENTION_PARAMS)

### TODO: Set the time window duration in milliseconds.
###       Start with 100 ms. Then try 50 and 200 and compare the saliency maps.
window_period = ???  # ms

time          = window_period
window        = torch.zeros((1, max_y, max_x), dtype=torch.float32)
saliency_map  = np.zeros((max_y, max_x), dtype=np.float32)
salmax_coords = np.zeros((2,), dtype=np.int32)

print(f'\nTask 1 — Running basic attention (window_period={window_period} ms)...')
print('Press Q to quit.')

for xi, yi, pi, ti in zip(x, y, p, t):
    if ti <= time:
        window[0][yi][xi] = 255  # Accumulate event into current window
    else:
        # ── Compute saliency ──────────────────────────────────────────────────
        saliency_map[:], salmax_coords[:] = run_attention(
            window, net_attention, device, resolution,
            config.ATTENTION_PARAMS['num_pyr']
        )

        # ── Visualise: events map ─────────────────────────────────────────────
        window_map_jet = cv2.applyColorMap(
            window.detach().cpu().numpy().squeeze(0).astype(np.uint8),
            cv2.COLORMAP_JET
        )
        cv2.putText(window_map_jet, 'Events map', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(window_map_jet,
                   (int(salmax_coords[1]), int(salmax_coords[0])), 6, (255, 255, 255), 4)

        # ── Visualise: saliency map ───────────────────────────────────────────
        sal_norm          = cv2.normalize(saliency_map, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        saliency_map_color = cv2.applyColorMap(sal_norm, cv2.COLORMAP_JET)
        cv2.putText(saliency_map_color, 'Saliency map', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.circle(saliency_map_color,
                   (int(salmax_coords[1]), int(salmax_coords[0])), 6, (255, 255, 255), 4)

        cv2.imshow('Task 1 — Events and Saliency Map',
                   cv2.hconcat([window_map_jet, saliency_map_color]))
        if cv2.waitKey(1) == ord('q'):
            break

        time  += window_period
        window = torch.zeros((1, max_y, max_x), dtype=torch.float32)

cv2.destroyAllWindows()


# ── Task 2: Inhibition of Return ─────────────────────────────────────────────
#
# The most salient point can guide a region-of-interest for further processing.
# But if we always return to the same salient spot, we never explore the scene.
#
# INHIBITION OF RETURN: once a location has been attended, suppress it in the
# saliency map so attention shifts to the next most salient region.
#
# Your task: complete run_attention_inhibition_of_return() below.
# Zero out a circle of radius 30 px around each previously visited location.
#
# Question: What are the coordinates of the first three detected salient points?
# Expected: [334 180], [298 264], [246 278]

def run_attention_inhibition_of_return(window, net, device, resolution, num_pyr, visited_locations):
    # Build multi-scale pyramid and run attention network
    resized_frames = [
        torchvision.transforms.Resize((int(resolution[0] / num_pyr),
                                       int(resolution[1] / num_pyr)))(window)
        for _ in range(1, num_pyr + 1)
    ]
    batch_frames = torch.stack([
        torchvision.transforms.Resize((resolution[0], resolution[1]))(f)
        for f in resized_frames
    ]).type(torch.float32).to(device)

    output_rot     = net(batch_frames)
    output_rot_sum = torch.sum(
        torch.sum(output_rot, dim=1, keepdim=True), dim=0, keepdim=True
    ).type(torch.float32).cpu().detach()
    salmap = torchvision.transforms.Resize((resolution[0], resolution[1]))(
        output_rot_sum
    ).squeeze(0).squeeze(0)

    ### TODO: Mask out already visited locations.
    ###       For each (y, x) in visited_locations, zero out a circle of radius 30
    ###       in salmap using cv2.circle on the numpy array, then convert back to tensor.
    ###
    ###       Hint:
    ###           radius = 30
    ###           for y_v, x_v in visited_locations:
    ###               salmap_np = salmap.numpy()
    ###               cv2.circle(salmap_np, (x_v, y_v), radius, 0, -1)
    ###               salmap = torch.from_numpy(salmap_np)

    salmax_coords = np.unravel_index(torch.argmax(salmap).cpu().numpy(), salmap.shape)
    salmap        = salmap.detach().cpu().numpy()
    salmap        = np.array((salmap - salmap.min()) / (salmap.max() - salmap.min()) * 255)
    return salmap, salmax_coords


# ── Run Task 2 ────────────────────────────────────────────────────────────────

net_attention = initialise_attention(device, config.ATTENTION_PARAMS)
time          = window_period
window        = torch.zeros((1, max_y, max_x), dtype=torch.float32)
saliency_map  = np.zeros((max_y, max_x), dtype=np.float32)
salmax_coords = np.zeros((2,), dtype=np.int32)
visited_locations = []

print(f'\nTask 2 — Running attention with inhibition of return...')
print('Press Q to quit.')

for xi, yi, pi, ti in zip(x, y, p, t):
    if ti <= time:
        window[0][yi][xi] = 255
    else:
        saliency_map[:], salmax_coords[:] = run_attention_inhibition_of_return(
            window, net_attention, device, resolution,
            config.ATTENTION_PARAMS['num_pyr'], visited_locations
        )
        visited_locations.append((salmax_coords[0], salmax_coords[1]))
        print(f'  Salient point: {salmax_coords}')

        # ── Visualise ─────────────────────────────────────────────────────────
        window_map_jet = cv2.applyColorMap(
            window.detach().cpu().numpy().squeeze(0).astype(np.uint8),
            cv2.COLORMAP_JET
        )
        cv2.putText(window_map_jet, 'Events map', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(window_map_jet,
                   (int(salmax_coords[1]), int(salmax_coords[0])), 6, (255, 255, 255), 4)

        sal_norm           = cv2.normalize(saliency_map, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        saliency_map_color = cv2.applyColorMap(sal_norm, cv2.COLORMAP_JET)
        cv2.putText(saliency_map_color, 'Saliency + IoR', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.circle(saliency_map_color,
                   (int(salmax_coords[1]), int(salmax_coords[0])), 6, (255, 255, 255), 4)

        cv2.imshow('Task 2 — Events and Saliency Map (IoR)',
                   cv2.hconcat([window_map_jet, saliency_map_color]))
        if cv2.waitKey(1) == ord('q'):
            break

        time  += window_period
        window = torch.zeros((1, max_y, max_x), dtype=torch.float32)

cv2.destroyAllWindows()


# ── Questions ─────────────────────────────────────────────────────────────────
#
# Q1. Why is a time window (window_period) used in the attention mechanism?
#     How does it affect the saliency computation?
#
# ANSWER: ???
#
# Q2. What role does run_attention play in updating the saliency map,
#     and how is the most salient location determined?
#
# ANSWER: ???
