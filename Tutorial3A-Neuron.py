"""
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz
Sarka Liskova, sarka.liskova@fel.cvut.cz
"""

### Task 0: Get familiar with the leaky integrate-and-fire (LIF) neuron model
"""
Play with the following simulation: In the code, the neuron is periodically stimulated by a current I_ext 
of amplitude I_ext_amp, influencing the membrane potential.
Run the simulation with I_ext_amp = 1.0, then with 3.0 and 5.0. 
Observe the membrane potential behaviour, its growth and the exponential leaky decay towards the resting 
potential value, when not stimulated. Notice the membrane potential dropping after crossing the firing threshold 
back to the Reset voltage (VR) value before increasing again.
"""
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# LIF parameters
Cm = 0.74
gL = 0.1
VL = -65.0
VT = -50.0
VR = -67.0
Rm = 1 / gL
tau_m = Cm / gL

# Time parameters
dt = 0.2
T = 100
time = np.arange(0, T, dt)

# Define input current
I_ext_amp = 1.0
I_ext = np.zeros_like(time)
pulse_times = [5, 60]
for t in pulse_times:
    I_ext[int(t/dt):int((t+10)/dt)] = I_ext_amp

# Initialize membrane potential
V = np.zeros_like(time)
V[0] = VL
display_V = V.copy()

# Create figure
fig, ax = plt.subplots(
    3, 1, figsize=(16, 8), sharex=True, gridspec_kw={'height_ratios': [2, 2, 1]}
)

ax[0].set_xlim(0, T)
ax[0].set_ylim(-0.5, max(I_ext) + 0.5)
ax[0].set_ylabel("Input Current I(uA)", fontsize=12)
ax[0].set_title("LIF Neuron Simulation", fontsize=20)
line_I, = ax[0].plot([], [], lw=2, color='gold', label="Input Current (I_ext)")
ax[0].legend(fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))

ax[1].set_xlim(0, T)
ax[1].set_ylim(-70, -40)
ax[1].set_ylabel("Membrane Potential (mV)", fontsize=12)
ax[1].axhline(y=VT, color='coral', linestyle='--', label=f"Threshold (VT = {VT} mV)")
ax[1].axhline(y=VL, color='cornflowerblue', linestyle='--', label=f"Resting Potential (VL = {VL} mV)")
line_V, = ax[1].plot([], [], lw=2, color='royalblue', label="Membrane Potential (V)")
ax[1].legend(fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))

ax[2].set_xlim(0, T)
ax[2].set_ylim(0.8, 1.2)
ax[2].set_xlabel("Time (ms)", fontsize=12)
ax[2].set_ylabel("Spike Output", fontsize=12)
ax[2].set_yticks([])
ax[2].axhline(y=1.0, color='k', linestyle='-')
line_spikes, = ax[2].plot([], [], 'k|', markersize=30, label="Spikes")
ax[2].legend(fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))

spike_times = []
plt.tight_layout(rect=[0.1, 0, 0.95, 1])
for axis in ax:
    axis.tick_params(axis='both', which='major', labelsize=10)

plt.ion()
plt.show()

# Simulation loop
for i in range(1, len(time)):
    dVdt = ((VL - V[i-1]) + Rm * I_ext[i]) / tau_m
    V[i] = V[i-1] + dVdt * dt
    display_V[i] = V[i]
    fired = False

    if V[i] >= VT:
        V[i] = VR
        display_V[i] = VT
        fired = True
        if i + 1 < len(time):
            V[i + 1] = VR

    if fired:
        spike_times.append(time[i])

    line_I.set_data(time[:i + 1], I_ext[:i + 1])
    line_spikes.set_data(spike_times, np.ones(len(spike_times)))
    line_V.set_data(time[:i + 1], display_V[:i + 1])

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)

plt.ioff()
plt.show(block=True)

"""
Additional exploration prompt:  
What happens if you modify the LIF parameters, such as Cm, gL, or VT? 
Experiment by increasing or decreasing these values and observe how the membrane potential and spiking behavior change in the animation. 
"""

###__________________________________________________________________________________________
### Task 2: Find the minimum firing current.
"""
Now, let's consider a constant current I_ext input instead of the pulsed one.
Find the minimal constant current I_min which causes the neuron to fire at least once.

LIF Neuron equation:
  tau_m * dV(t)/dt = (V_L - V(t)) + R_m * I_ext(t)

Hint: With constant current dV(t)/dt = 0, spiking condition: V(t) = V_T (threshold).
"""

#TODO solve for I_min here
I_min = None
print(f"Minimum input current required to reach threshold: {I_min:.2f} uA")