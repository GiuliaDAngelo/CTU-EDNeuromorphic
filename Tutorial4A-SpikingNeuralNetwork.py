'''

Giulia D'Angelo, giulia.dangelo@fel.cvut.cz
Sarka Liskova, sarka.liskova@fel.cvut.cz 

This tutorial demonstrates how to simulate a simple spiking neural network using the Brian2 library.
We will create a network of 100 neurons, each with a defined membrane potential that evolves over time.
The neurons will fire action potentials when their membrane potential exceeds a certain threshold,
and we will visualize the spiking activity and firing rates based on their baseline potentials.

Task 1: Spontaneous activity  
Some biological neurons fire spontaneously without external input, for example, brainstem neurons that drive breathing. 
This intrinsic excitability is modelled using the baseline membrane potential `v0`: the higher it is, the more often the neuron fires on its own.  
This first example builds a group of independent neurons, each with different baseline membrane potentials, ranging from  0 to v0_max with growing neuron index.  
 
Run the simulation and observe at which times is each of the neurons firing and how the baseline potential controls the firing rate.  

Adjust the tau parameter, how does the activity change for tau = {2.0, 10.0, 50.0}?
'''

from brian2 import * # get by `pip install brian2`
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
import matplotlib.pyplot as plt
import time
from IPython.display import display, clear_output

# Start a new Brian2 simulation scope to reset any previous settings
start_scope()

# Set the number of neurons in the simulation
N = 100  # Total number of neurons

# Define the time constant (tau) for the neuron dynamics (in milliseconds)
tau = 10.0 * ms  # Time constant determining how quickly the membrane potential responds

# Define the maximum initial membrane potential (v0) for the neurons
v0_max = 20.  # Maximum baseline potential for the neurons

# Set the total duration of the simulation (in milliseconds)
duration = 1000 * ms  # Simulation time set to 1 second

# Define the differential equation governing the dynamics of the neuron membrane potential (v)
# The equation states that the change in membrane potential over time is proportional to the difference
# between the baseline potential (v0) and the current potential (v), scaled by the time constant (tau).
eqs = '''
dv/dt = (v0 - v) / tau : 1 (unless refractory)  # Membrane potential dynamics
v0 : 1  # Baseline membrane potential for each neuron
'''

# Create a group of neurons (NeuronGroup) with 'N' neurons using the specified dynamics equations
# Neurons will spike (generate action potentials) when their membrane potential exceeds 1,
# after which their potential resets to 0. They will also experience a refractory period of 5 ms.
# We use method='euler' to avoid AST parsing issues with method='exact' and NumPy 2.0.
G = NeuronGroup(N, eqs, threshold='v > 1', reset='v = 0', refractory= 5 * ms, method='euler')

# Create a SpikeMonitor to record the spiking activity of the neurons in the group 'G'
M = SpikeMonitor(G)

# Initialize the baseline membrane potential (v0) for each neuron based on its index (i)
# This ensures a range of baseline potentials from 0 to v0_max across all neurons
G.v0 = 'i * v0_max / (N - 1)'

# Run the simulation for the specified duration (1000 ms)
run(duration)

# Begin plotting the results:
figure(figsize=(12, 4))  # Create a figure with dimensions 12x4 inches

# First subplot: Visualize the spiking activity of the neurons
subplot(121)  # Create the first subplot (1 row, 2 columns, 1st plot)
plot(M.t / ms, M.i, '.k', markersize=2)  # Plot spike times (M.t) against neuron indices (M.i) as black dots
xlabel('Time (ms)')  # Label the x-axis as "Time (ms)"
ylabel('Neuron index')  # Label the y-axis as "Neuron index"
title('Spiking Activity of Neurons')  # Add a title for clarity

# Second subplot: Visualize the relationship between baseline potential and firing rate
subplot(122)  # Create the second subplot (1 row, 2 columns, 2nd plot)
plot(G.v0, M.count / duration)  # Plot baseline potential (G.v0) against firing rate (M.count/duration)
xlabel('v0')  # Label the x-axis as "v0"
ylabel('Firing rate (sp/s)')  # Label the y-axis as "Firing rate (spikes per second)"
title('Firing Rate vs Baseline Potential')  # Add a title for clarity

# Display the plots
plt.show(block=True)

# Print 'end' to indicate that the simulation and plotting are complete
print('end')
