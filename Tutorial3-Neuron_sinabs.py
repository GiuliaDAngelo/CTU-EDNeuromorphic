'''
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz

This script creates a single neuron and injects it with current to see the membrane potential dynamics.
From sinabs documentation.
'''

import os
import torch
import sinabs.layers as sl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('qt5agg')

# Length of the stimulation
lenstim = 100

# Create a tensor of ones with shape (1, lenstim, 1) to represent the input current
ts = torch.zeros(1, lenstim, 1) + 1

# Initialize arrays for x, y, and p coordinates (all zeros)
x = np.zeros(lenstim).astype(int)
y = np.zeros(lenstim).astype(int)
p = np.zeros(lenstim).astype(int)

# Define a class for Receptive Fields (RFs) with a Leaky Integrate-and-Fire (LIF) neuron
class RFs:
    def __init__(self, tau_mem):
        self.neuron = sl.LIF(tau_mem=tau_mem)  # Initialize the LIF neuron with a given membrane time constant
        self.vmem = []  # List to store membrane potential values

# Define the dimensions of the neuron layer
width = 2
height = 2
num_neurons = width * height

# Membrane time constant
tau_mem = 1

# Create a layer of RFs neurons
neurons = [[RFs(tau_mem=tau_mem) for _ in range(width)] for _ in range(height)]

# Output spike raster
spike_train = []

# Iterate over the time steps to simulate the neuron dynamics
i = 0
for t in range(0, lenstim-1):
    with torch.no_grad():  # Disable gradient calculation for efficiency
        RF = neurons[y[i]][x[i]]  # Select the neuron based on the current coordinates
        out = RF.neuron(ts[:, i : i + 1])  # Inject current into the neuron and get the output spikes
        if (out != 0).any():  # Check if there is a spike
            spike_train.append(ts.unsqueeze(dim=0))  # Record the spike
        RF.vmem.append(RF.neuron.v_mem[0, 0])  # Record the membrane potential
    i += 1

# Plot the membrane potential dynamics of the first neuron
plt.figure()
plt.plot(range(lenstim-1), neurons[0][0].vmem)
plt.title("LIF membrane dynamics")
plt.xlabel("$t$ [ms]")
plt.ylabel("$V_{mem}$")
plt.show()

print('end')