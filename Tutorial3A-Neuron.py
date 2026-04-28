'''
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz

This script simulates the behavior of a Leaky Integrate-and-Fire (LIF) neuron model.
The LIF model is a simple yet effective representation of neuronal dynamics, capturing
essential features of spiking behavior. The simulation visualizes the neuron's membrane
potential over time in response to an external input current composed of short pulses.

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

# Set the backend for Matplotlib to 'TkAgg' for interactive plotting
matplotlib.use('TkAgg')


# Define LIF parameters
Cm = 0.74          # Membrane capacitance (uF)
gL = 0.1           # Leak conductance (mS)
VL = -65.0         # Resting potential (mV)
VT = -50.0         # Threshold voltage (mV)
VR = -70.0         # Reset voltage (mV)
Rm = 1 / gL        # Membrane resistance (MΩ)
tau_m = Cm / gL   # Membrane time constant (ms)

# Time parameters
dt = 0.2           # Time step (ms)
T = 200            # Total simulation time (ms)
time = np.arange(0, T, dt)  # Create a time array

# Define input current
I_ext = np.zeros_like(time)  # Initialize external current array
pulse_times = np.arange(20, T, 40)  # Define pulse start times
for t in pulse_times:
    I_ext[int(t/dt):int((t+10)/dt)] = 2.0  # Create short pulses of current

# Initialize membrane potential
V = np.zeros_like(time)  # Membrane potential array
V[0] = VL  # Set initial potential to resting potential

# Simulate LIF neuron dynamics
for i in range(1, len(time)):
    # Calculate change in membrane potential (dV/dt) based on leak and input current
    dVdt = ((VL - V[i-1]) + Rm * I_ext[i]) / tau_m
    V[i] = V[i-1] + dVdt * dt  # Update membrane potential using Euler's method

    # Check if the potential exceeds the threshold to generate a spike
    if V[i] >= VT:
        V[i] = VT + 5  # Simulate spike peak by temporarily exceeding threshold
        if i + 1 < len(time):
            V[i + 1] = VR  # Reset potential after spike

# Create animation of the simulation
fig, ax = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

# Plot membrane potential
ax[0].set_xlim(0, T)
ax[0].set_ylim(min(V) - 5, max(V) + 5)
ax[0].set_ylabel("Membrane Potential (mV)", fontsize=20)
ax[0].set_title("LIF Neuron Simulation", fontsize=20)

# Add lines for threshold and resting potentials
ax[0].axhline(y=VT, color='r', linestyle='--', label=f"Threshold ($V_T$ = {VT} mV)")
ax[0].axhline(y=VL, color='b', linestyle='--', label=f"Resting Potential ($V_L$ = {VL} mV)")

# Plot input current
ax[1].set_xlim(0, T)
ax[1].set_ylim(0, max(I_ext) + 0.5)
ax[1].set_xlabel("Time (ms)", fontsize=20)
ax[1].set_ylabel("Input Current (I_ext)", fontsize=20)

# Initialize line objects for animation
line_V, = ax[0].plot([], [], lw=2, label="Membrane Potential ($V$)")
line_I, = ax[1].plot([], [], lw=2, color='orange', label="Input Current ($I_{\text{ext}}$)")

def init():
    """Initialize the animation lines."""
    line_V.set_data([], [])
    line_I.set_data([], [])
    return line_V, line_I

def update(frame):
    """Update the animation for each frame."""
    line_V.set_data(time[:frame], V[:frame])  # Update membrane potential line
    line_I.set_data(time[:frame], I_ext[:frame])  # Update input current line
    return line_V, line_I

# Create the animation without 'blit' for TkAgg compatibility
ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, interval=20)

# Add legends to each subplot for clarity
ax[0].legend(loc="best", fontsize=20)
ax[1].legend(loc="best", fontsize=20)

# Set font size for tick marks
for axis in ax:
    axis.tick_params(axis='both', which='major', labelsize=20)

# Display the plot
plt.show()
plt.pause(0.001)
