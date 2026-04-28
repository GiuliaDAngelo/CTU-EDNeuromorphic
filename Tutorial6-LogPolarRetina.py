'''
================================================================================
Tutorial 6 — Log-Polar Retinal Structure
================================================================================
NPC Lab — Czech Technical University in Prague
Giulia D'Angelo | giulia.dangelo@fel.cvut.cz

This tutorial simulates the eccentric spatial organisation of the mammalian
retina using a log-polar mapping. In the biological retina, spatial resolution
is highest at the fovea (centre) and decreases progressively toward the
periphery — receptive fields grow larger with eccentricity.

We model this by arranging neurons in concentric rings (eccentricity) and
angular sectors, where each neuron's receptive field (RF) size is proportional
to its distance from the centre (fovea). A Look-Up Table (LUT) is built to
map each pixel to the set of neurons whose RF covers it — this dramatically
speeds up event-to-neuron routing during simulation.

Key structures:
    Rings  (R) — eccentricity levels, indexed from centre outward
    Sectors (S) — angular subdivisions of each ring
    LUT (mask) — spatial index: mask[y][x] = list of neuron IDs covering (x,y)

Reference:
    Chessa et al., "A space-variant model for motion interpretation across
    the visual field", Journal of Vision, 2016.
    https://jov.arvojournals.org/article.aspx?articleid=2498961

================================================================================
'''

# ── Imports ───────────────────────────────────────────────────────────────────

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sinabs.layers as sl   # LIF neuron layer
import torch

matplotlib.use('TkAgg')      # Required for interactive display windows


# ── Neuron Container ──────────────────────────────────────────────────────────

class RFs:
    '''Receptive field neuron: holds a LIF neuron and its spatial properties.'''
    def __init__(self, tau_mem):
        self.neuron    = sl.LIF(tau_mem=tau_mem)  # Leaky Integrate-and-Fire model
        self.vmem      = []   # Membrane potential history
        self.spikes_ts = []   # Spike timestamps
        self.cx: int   = 0    # RF centre x-coordinate (pixels)
        self.cy: int   = 0    # RF centre y-coordinate (pixels)
        self.radius: int = 0  # RF radius (pixels)
        self.R: int    = 0    # Eccentricity ring index
        self.S: int    = 0    # Angular sector index
        self.ID: int   = 0    # Unique neuron ID


# ── Geometric Utilities ───────────────────────────────────────────────────────

def rescale_rho(rho, max_rho, R):
    '''Rescale eccentricity rho to fit within the image dimensions.
    The nonlinearity parameter a controls how fast RFs grow with ring index.
    '''
    return (rho / (rho0 * a ** R)) * max_rho


def polar_to_cartesian(rho, psi):
    '''Convert polar coordinates (rho, psi) to Cartesian (x, y).'''
    return rho * np.cos(psi), rho * np.sin(psi)


def compute_rf_size(rho, W_max, rho0, R):
    '''Compute RF radius based on eccentricity.
    Returns 0 inside the blind spot (rho < rho0).
    '''
    if rho < rho0:
        return 0
    return W_max * (rho / R)


def gaussian_plot(neurons, ID, window):
    '''Render a Gaussian-shaped RF for neuron ID into the window array.
    Pixels within the RF radius are weighted by a 2D Gaussian centred at (cx, cy).
    This mimics the graded sensitivity profile of biological RFs.
    '''
    sigma = neurons[ID].radius / 2.0
    for i in range(-neurons[ID].radius, neurons[ID].radius):
        for j in range(-neurons[ID].radius, neurons[ID].radius):
            cy_i = neurons[ID].cy + i
            cx_j = neurons[ID].cx + j
            if 0 <= cy_i < height and 0 <= cx_j < width:
                distance = np.sqrt(i ** 2 + j ** 2)
                if distance <= neurons[ID].radius:
                    gaussian_value = np.exp(-(distance ** 2) / (2 * sigma ** 2))
                    window[cy_i, cx_j] = gaussian_value * 255
    return window


# ── Log-Polar Retina Construction ─────────────────────────────────────────────

def create_eccentric_RFs():
    '''Build the full log-polar retina: neurons, RF geometry, and LUT mask.

    Returns:
        neurons — list of RFs objects with spatial and neural properties
        mask    — LUT: mask[y][x] = list of neuron IDs covering pixel (x,y)
        ax      — matplotlib axes with RF structure plot
    '''
    neurons  = [RFs(tau_mem=tau_mem) for _ in range(R * S)]
    neuronID = 0

    # W_max: maximum RF size, derived from log-polar geometry (Eq. 4 in reference)
    W_max   = rho0 * (a ** R) * (1 - a ** (-1))
    max_rho = np.sqrt((width / 2) ** 2 + (height / 2) ** 2)

    # LUT: for each pixel, store which neuron IDs have an RF covering it
    mask = [[[] for _ in range(width)] for _ in range(height)]

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_title('Log-Polar Retina — Receptive Field Structure')
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)

    for r in range(1, R + 1):
        rho          = rho0 * (a ** r)              # Eccentricity for this ring
        rescaled_rho = rescale_rho(rho, max_rho, R) # Scale to image dimensions

        for s in range(S):
            psi    = 2 * np.pi * s / S              # Angular position
            cx, cy = polar_to_cartesian(rescaled_rho, psi)

            # Centre in image coordinates
            cx += width  // 2
            cy += height // 2

            # Skip out-of-bounds neurons
            if not (0 <= cx < width and 0 <= cy < height):
                continue

            circle_radius = max(1, int(compute_rf_size(rho, W_max, rho0, R)))

            # Assign spatial properties to this neuron
            neurons[neuronID].cx     = int(cx)
            neurons[neuronID].cy     = int(cy)
            neurons[neuronID].radius = circle_radius
            neurons[neuronID].R      = int(r)
            neurons[neuronID].S      = int(s)
            neurons[neuronID].ID     = neuronID

            # Plot RF circle and centre
            ax.add_patch(plt.Circle((cx, cy), circle_radius, color='k', fill=False, linewidth=0.5))
            ax.scatter(cx, cy, color='r', s=1)

            # Populate LUT: register this neuron for every pixel inside its RF
            for i in range(-circle_radius, circle_radius + 1):
                for j in range(-circle_radius, circle_radius + 1):
                    if i ** 2 + j ** 2 <= circle_radius ** 2:
                        xp, yp = int(cx + j), int(cy + i)
                        if 0 <= xp < width and 0 <= yp < height:
                            mask[yp][xp].append(neuronID)

            neuronID += 1

    return neurons, mask, ax


# ── Parameters ────────────────────────────────────────────────────────────────

width    = 128    # Image width  (pixels)
height   = 128    # Image height (pixels)
tau_mem  = 1      # LIF membrane time constant

# Simulation
lenstim     = 1000  # Number of time steps
t_window    = 20    # Visualisation refresh interval (time steps)
rate_spikes = 5     # Mean Poisson spike rate

# Log-polar geometry
a    = 1.3   # Nonlinearity: controls how fast RF size grows with ring index
rho0 = 0.5   # Blind spot radius (no RFs closer than this to the centre)
R    = 16    # Number of eccentricity rings
S    = 24    # Number of angular sectors per ring


# ── Build Retina ──────────────────────────────────────────────────────────────

print('Building log-polar retina...')
neurons, mask, ax = create_eccentric_RFs()
print(f'Neurons created: {len(neurons)}')
plt.show(block=False)
plt.pause(0.1)


# ── Generate Input ────────────────────────────────────────────────────────────
#
# We generate a Poisson spike train as synthetic input and assign random
# pixel coordinates to each spike — simulating a noisy visual stimulus.

ts = torch.poisson(torch.ones(1, lenstim, 1) * rate_spikes).float()
x  = np.random.randint(0, width,  lenstim)
y  = np.random.randint(0, height, lenstim)


# ── Simulate and Visualise ────────────────────────────────────────────────────
#
# For each time step:
#   1. Look up which neurons have RFs covering the active pixel (via mask/LUT)
#   2. Inject the spike into each covering neuron
#   3. If the neuron fires, render its Gaussian RF into the visualisation window

print('Running simulation...')

plt.ion()
fig_sim, ax_sim = plt.subplots(figsize=(6, 6))
window  = np.zeros((height + 1, width + 1))
tw      = t_window

with torch.no_grad():
    for t in range(0, lenstim - 1):
        neuron_ids = mask[y[t]][x[t]]   # LUT lookup: which neurons cover (x[t], y[t])?

        for ID in neuron_ids:
            # Normalise output by RF area to avoid large neurons dominating
            out = neurons[ID].neuron(ts[:, t:t + 1]) / max(1, neurons[ID].radius ** 2)

            if (out != 0).any():
                neurons[ID].spikes_ts.append(t)
                gaussian_plot(neurons, ID, window)

                if t > tw:
                    ax_sim.clear()
                    ax_sim.imshow(window, cmap='jet', vmin=0, vmax=255)
                    ax_sim.set_title(f'Gaussian RF Activity — t={t}')
                    ax_sim.axis('off')
                    plt.pause(0.0001)
                    window = np.zeros((height + 1, width + 1))
                    tw     = t + t_window

plt.ioff()
print('Simulation complete.')


# ── Exercise ──────────────────────────────────────────────────────────────────
#
# GOAL: Quantify how the log-polar retina covers the image and how it responds
#       to a diagonal stimulus sweeping from top-left to bottom-right.
#
# Expected outputs:
#   covered_pixels     — number of pixels covered by at least one RF (integer)
#   coverage_percent   — covered_pixels / total_pixels * 100 (float)
#   responding_neurons — sorted list of neuron IDs activated by the diagonal

### TODO 1: Compute image coverage from the LUT mask.
###         A pixel is covered if mask[y][x] contains at least one neuron ID.
###         Hint: loop over all (y, x) and check len(mask[y][x]) > 0
covered_pixels   = None
coverage_percent = None

if covered_pixels is None or coverage_percent is None:
    raise NotImplementedError("TODO 1: compute covered_pixels and coverage_percent")

### TODO 2: Create a diagonal stimulus (top-left → bottom-right).
###         For each pixel (t, t) along the diagonal, find all neurons in mask[t][t]
###         and collect their IDs into a sorted list.
###         Hint: diag_len = min(width, height), then loop t in range(diag_len)
responding_neurons = None

if responding_neurons is None:
    raise NotImplementedError("TODO 2: create diagonal stimulus and find responding neurons")

print(f'\nExercise results:')
print(f'Covered pixels:             {covered_pixels} / {width * height}')
print(f'Coverage (%):               {coverage_percent:.2f}')
print(f'Responding neurons (count): {len(responding_neurons)}')
print(f'Responding neurons:         {responding_neurons}')


# ── Questions ─────────────────────────────────────────────────────────────────
#
# Q1. How does rescale_rho ensure RFs are properly distributed within the image?
#     What is the role of the nonlinearity parameter a?
#
# ANSWER: ???
#
# Q2. What role does gaussian_plot play in visualising RF activity?
#     How does it relate to membrane potential dynamics and spike generation?
#
# ANSWER: ???