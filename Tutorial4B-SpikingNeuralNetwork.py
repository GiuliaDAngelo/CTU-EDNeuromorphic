'''

Giulia D'Angelo, giulia.dangelo@fel.cvut.cz
Sarka Liskova, sarka.liskova@fel.cvut.cz 

Task 1: Adding connections
The previous network consisted of independent neurons with spontaneous spiking. Now we will add connections and make only one of the neurons spike spontaneously. 
We will form a chain of 10 neurons, where signal can travel in both directions and just the middle neuron will have non-zero baseline potential. 

Run the provided script and see how the signal spreads from the spiking neuron. Play around with tau parameter to see how it influences the system.  

Then return tau back to `tau = 10*ms`, disable the right-to-left connections (`S.connect(condition='j == i-1 and i > 0')`), and set the non-zero 
baseline potential for the first neuron instead of the middle one.  
Run the simulation. How far does the signal travel, which neuron in the chain is the most distant one to spike?  

Now play with the connection strength weight `w`, explore values (0.9 - 1.1). How does the spiking behaviour change?  

Set weights back to `w = 1.0` and start decreasing the refractory period from `5*ms` down to `1*ms`. How far does the signal spread for `1*ms` refractory period?
'''
from brian2 import * # get by `pip install brian2`
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
import matplotlib.pyplot as plt
import time


def animate_signal_transfer(VM, N):
    plt.close('all')
    n_frames = VM.v.shape[1]
    skip = 5

    fig, ax = plt.subplots(figsize=(10, 4))
    plt.show(block=False)  # Open the window once, non-blocking

    for frame in range(0, n_frames, skip):
        ax.clear()
        v_now = VM.v[:, frame]
        ax.bar(range(N), np.clip(v_now, 0, 1.5), color='salmon')
        ax.axhline(1.0, color='k', linestyle='--', label='threshold')
        ax.set_ylim(0, 1.5)
        ax.set_xlim(-0.5, N - 0.5)
        ax.set_xlabel('Neuron index')
        ax.set_ylabel('Membrane potential')
        ax.set_title(f't = {VM.t[frame]/ms:.1f} ms')
        ax.legend()
        plt.pause(0.01)  # Renders the frame and yields control briefly — this is the key line

start_scope() # Start a new Brian2 simulation scope to reset any previous settings

N = 10  # Total number of neurons
tau = 10 * ms  # Time constant (in milliseconds) determining how quickly the membrane potential responds
duration = 120 * ms  # Set the total duration of the simulation (in milliseconds)

# Define the differential equation governing the dynamics of the neuron membrane potential (v)
eqs = '''
dv/dt = (v0 - v) / tau : 1 (unless refractory)  # Membrane potential dynamics
v0 : 1  # Baseline membrane potential for each neuron
'''

# Create a group of neurons (NeuronGroup) with 'N' neurons using the specified dynamics equations
G = NeuronGroup(N, eqs, threshold='v > 1', reset='v = 0', refractory= 5 * ms, method='euler')
M = SpikeMonitor(G) # Create a SpikeMonitor to record the spiking activity of the neurons in the group 'G'
VM = StateMonitor(G, 'v', record=True)  # record all neurons

G.v0 = 0 # Initialize the baseline membrane potential (v0) for all neurons to 0 (no spontaneous spiking)
# Set the first neuron (index 0) to have a v0 > 1 so it spikes continuously on its own
# and propagates its activity down the chain

S = Synapses(G, G, model='w : 1', on_pre='v_post += w')
S.connect(condition='j == i+1 and i < N_pre-1')
S.connect(condition='j == i-1 and i > 0')  # bidirectional
S.w = 1.0

# 1. Set the non-zero baseline potential for the middle neuron to trigger the spiking activity
G.v0[4] = 2.0  

# 2. Run the simulation 
run(duration)
animate_signal_transfer(VM, N)


# Plot spiking activity
figure(figsize=(12, 4))  
plot( M.i, M.t / ms, '.k')  # Plot spike times (M.t) against neuron indices (M.i) as black dots
xlabel('Neuron index')  # Label the y-axis as "Neuron index"
ylabel('Time (ms)')  # Label the x-axis as "Time (ms)" 
title('Spiking Activity of Neurons') 
# Display the plots
plt.show()
