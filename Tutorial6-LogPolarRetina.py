'''
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz

This script simulates the eccentric representation of the retina using log-polar mapping.
It generates receptive fields (RFs) for neurons arranged in a log-polar pattern, which is commonly used to model the retina's visual mapping.
Each receptive field (RF) represents the region of the visual field captured by a neuron and changes size as the eccentricity (distance from the fovea) increases.
'''

import sys
sys.path.append('/Users/giuliadangelo/workspace/code/foveated-vision')  # Adds a custom directory to the system path for importing required modules
import numpy as np
import matplotlib.pyplot as plt
import sinabs.layers as sl  # Importing necessary layers from the Sinabs library for spiking neurons
import torch
import imageio
import matplotlib
matplotlib.use('qt5agg')  # Configures matplotlib to use the Qt5 backend for interactive graphics

class RFs:
    # Class to define properties of a neuron with a receptive field (RF).
    def __init__(self, tau_mem):
        self.neuron = sl.LIF(tau_mem=tau_mem)  # Leaky Integrate-and-Fire neuron model
        self.vmem = []  # Membrane potential history
        self.spikes_ts = []  # Spike timestamps
        self.cx: int = 0  # x-coordinate of the RF center
        self.cy: int = 0  # y-coordinate of the RF center
        self.radius: int = 0  # Radius of the receptive field
        self.R: int = 0  # Eccentricity ring
        self.S: int = 0  # Sector of the visual field
        self.ID: int = 0  # Unique ID for the neuron

# Function to rescale the rho value to ensure it fits within the defined plot dimensions.
def rescale_rho(rho, max_rho, R):
    # The rescaling ensures that the rho value remains proportional while fitting within the maximum defined radius.
    return (rho / (rho0 * a ** R)) * max_rho

# Function to convert polar coordinates (rho, psi) to Cartesian coordinates (x, y).
def polar_to_cartesian(rho, psi):
    # Converts polar coordinates to Cartesian coordinates for plotting
    x = rho * np.cos(psi)
    y = rho * np.sin(psi)
    return x, y

# Function to compute the size of a receptive field based on its eccentricity (rho).
# If rho is less than rho0 (the blind spot), no receptive field is generated.
def compute_rf_size(rho, W_max, rho0, R):
    if rho < rho0:
        return 0  # No receptive fields inside the blind spot
    rf_size = W_max * (rho / R)  # Scale the RF size based on eccentricity
    return rf_size

# Function to plot the Gaussian shape of a receptive field centered at (cx, cy) with a specified radius.
def gaussian_plot(neurons, ID, window):
    # Draws a Gaussian-shaped receptive field at the center (cx, cy)
    sigma = neurons[ID].radius / 2.0  # Standard deviation for the Gaussian shape
    for i in range(-neurons[ID].radius, neurons[ID].radius):
        for j in range(-neurons[ID].radius, neurons[ID].radius):
            if (neurons[ID].cy + i) >= 0 and (neurons[ID].cy + i) < height and (neurons[ID].cx + j) >= 0 and (neurons[ID].cx + j) < width:
                distance = np.sqrt(i ** 2 + j ** 2)
                if distance <= neurons[ID].radius:
                    gaussian_value = np.exp(-(distance ** 2) / (2 * sigma ** 2))  # Gaussian function
                    window[neurons[ID].cy + i, neurons[ID].cx + j] = gaussian_value * 255  # Apply Gaussian to window
    return window

# Function to create a grid of eccentric receptive fields (RFs) for the retina model.
def create_eccentric_RFs():
    neurons = [RFs(tau_mem=tau_mem) for _ in range(R * S)]  # Initialize neurons
    neuronID = 0

    # Compute W_max, the maximum receptive field size, based on Equation 4.
    W_max = rho0 * (a ** R) * (1 - a ** (-1))

    # Calculate the maximum rho value based on plot dimensions.
    max_rho = np.sqrt((width / 2) ** 2 + (height / 2) ** 2)

    # Create an empty mask initialized to -1 (or any value to indicate no receptive field).
    mask = [[[] for _ in range(width)] for _ in range(height)]

    # Set up the plot for visualizing the receptive fields
    fig, ax = plt.subplots()
    ax.set_aspect('equal')  # Ensure equal scaling on both axes

    # Loop over eccentricity rings (r) and angular sectors (s)
    for r in range(1, R + 1):
        rho = rho0 * (a ** r)  # Calculate eccentricity
        rescaled_rho = rescale_rho(rho, max_rho, R)  # Rescale to fit the plot

        # Loop through each sector
        for s in range(S):
            psi = 2 * np.pi * s / S  # Angular displacement in polar coordinates
            cx, cy = polar_to_cartesian(rescaled_rho, psi)  # Convert to Cartesian coordinates

            # Shift the coordinates to center them in the plot
            cx += width // 2
            cy += height // 2

            # Skip neurons whose receptive fields are out of bounds
            if cx < 0 or cx >= width or cy < 0 or cy >= height:
                continue

            circle_radius = int(compute_rf_size(rho, W_max, rho0, R))  # Compute RF size

            # Initialize neuron properties
            neurons[neuronID].cx = int(cx)
            neurons[neuronID].cy = int(cy)
            neurons[neuronID].radius = circle_radius
            neurons[neuronID].R = int(r)
            neurons[neuronID].S = int(s)
            neurons[neuronID].ID = neuronID

            # Plot the receptive field circle
            circle = plt.Circle((cx, cy), circle_radius, color='k', fill=False)
            ax.add_patch(circle)  # Add the circle to the plot

            # Mark the center with a small red dot
            plt.scatter(cx, cy, color='r', s=1)

            # Update the mask with the neuron ID for pixels inside the receptive field
            for i in range(-circle_radius, circle_radius + 1):
                for j in range(-circle_radius, circle_radius + 1):
                    if i ** 2 + j ** 2 <= circle_radius ** 2:  # Pixel inside the circle
                        x_pixel = int(cx + j)
                        y_pixel = int(cy + i)
                        if 0 <= x_pixel < width and 0 <= y_pixel < height:
                            mask[y_pixel][x_pixel].append(neuronID)

            neuronID += 1

    return neurons, mask, ax

# Define camera and neuron parameters
width = 128
height = 128
num_neurons = width * height
tau_mem = 1  # Membrane time constant

# Simulation parameters
lenstim = 1000
t_window = 20
a = 1.3  # Nonlinearity parameter for log-polar mapping
q = 2    # Scaling factor for angular displacement
rho0 = 0.5  # Blind spot radius
R = 16   # Number of eccentricity rings
S = 24   # Number of angular sectors

# Generate Poisson-distributed spike train
rate_spikes = 5
ts = torch.poisson(torch.ones(1, lenstim, 1) * rate_spikes).float()

# Create random x, y coordinates for spike generation
x = np.random.randint(0, width, lenstim)
y = np.random.randint(0, height, lenstim)
p = np.zeros(lenstim).astype(int)

# Generate the receptive fields and mask
[neurons, mask, ax] = create_eccentric_RFs()

# Print the number of neurons generated
print('Number of neurons: ', len(neurons))

# Create a window to store and plot spikes
plt.figure()
window = np.zeros((height + 1, width + 1))
windows = []
tw = 20

# Simulate and visualize spikes over time
with torch.no_grad():  # Disable gradient computation
    for t in range(0, lenstim - 1):
        # Get the list of neuron IDs for the current x, y position
        IDs = mask[y[t]][x[t]]
        for ID in IDs:
            # Compute the neuron's spike output and plot the receptive field
            out = neurons[ID].neuron(ts[:, t:t + 1]) / (neurons[ID].radius ** 2)
            if (out != 0).any():  # If the neuron produces a spike
                neurons[ID].spikes_ts.append(t)  # Record the spike time
                gaussian_plot(neurons, ID, window)
                if t > t_window:
                    # Update the plot with the spike window
                    plt.imshow(window, cmap='jet')
                    windows.append(np.copy(window))  # Store window for GIF
                    plt.draw()
                    plt.pause(0.0001)
                    window = np.zeros((height + 1, width + 1))  # Reset the window
                    t_window = t + tw

# Optionally save the simulation as a GIF
# imageio.mimsave('windows.gif', windows, duration=0.1)
