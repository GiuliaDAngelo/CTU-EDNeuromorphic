"""
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz
Sarka Liskova, sarka.liskova@fel.cvut.cz
"""

import os
import torch
import sinabs.layers as sl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('qt5agg')

### Task 0: Simulate a single neuron in sinabs
"""
This script creates a LIF neuron using the sinabs library and stimulates it with constant current.   
Run the script explore the resulting membrane potential dynamic behaviour.
"""

# Length of the stimulation
lenstim = 100
tau_mem = 1.0     # Membrane time constant

# Create a neuron using the LIF() class
neuron = sl.LIF(tau_mem=tau_mem)  # Initialize the LIF neuron with a given membrane time constant
neuron.reset_states()

# Input current: shape (batch=1, time=lenstim, neurons=1)
ts = torch.ones(1, lenstim, 1)

vmem = []
spike_train = []
spike_times = []

with torch.no_grad():
    for i in range(lenstim):
        out = neuron(ts[:, i:i+1, :])          # shape (1, 1, 1)
        spike = out.item()                     # 0.0 or >0
        spike_train.append(spike)
        if spike > 0:
            spike_times.append(i)

        vmem.append(neuron.v_mem.item())       # membrane after this step

# Plot membrane potential
plt.figure(figsize=(8, 4))
plt.plot(range(lenstim), vmem, label = "membrane potential", color="cornflowerblue")
plt.plot(spike_times, np.ones(len(spike_times)), "|", markersize=12, label="spikes", color="salmon")
plt.title("LIF membrane dynamics")
plt.xlabel("t [ms]")
plt.ylabel("V_mem")
plt.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1.02, 1))
plt.show()

print('end')

### Task 1: Effects of tau_mem
"""
Use the previously provided script to explore how the spiking changes with change in tau_mem.  
Start with initializing a neuron `neuron = sl.LIF(tau_mem=tau_mem, spike_threshold = 0.99)` and see how lowering the firing threshold changed the firing frequency. 
Then add three more neurons with tau_mem values = {2.0, 5.0, 10.0} and spike_threshold = 0.99.  
Plot all of the obtained dynamics below each other to compare.  

How many times did each of the four neurons spike within the simulation window?
"""

lenstim = 100   # Length of the stimulation ms
tau_mem = 1.0   # Membrane time constant to start with

# Input current: shape (batch=1, time=lenstim, neurons=1)
ts = torch.ones(1, lenstim, 1)

# Create a neuron using the LIF() class
neuron = sl.LIF(tau_mem=tau_mem, spike_threshold = 0.99)  # Initialize the LIF neuron with a given membrane time constant
neuron.reset_states()

# TODO
# Add three more neurons with tau_mem values = {2.0, 5.0, 20.0}
# and plot the resulting membrane potentials together to see the effect of tau_mem on the membrane dynamics.