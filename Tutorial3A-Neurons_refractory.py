"""
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz
Sarka Liskova, sarka.liskova@fel.cvut.cz
"""

### Task 1: Refractory period
"""
In the visualisation of task 0, you may have noticed that after the spike, the neuron is immediately ready to spike again. However, in biological neurons 
this is not possible. There is the so-called refractory period, time required to establish ion equillibrium within the cell again, during which no firing is possible. 
In the following example refractory period of tau_ref = 2.0 ms is implemented.   
Run the script and observe the effect of the refractory period on the firing rate. 
"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# LIF parameters
Cm = 0.74          # Membrane capacitance (uF)
gL = 0.1           # Leak conductance (mS)
VL = -65.0         # Resting potential (mV)
VT = -50.0         # Threshold voltage (mV)
VR = -67.0         # Reset voltage (mV)
Rm = 1 / gL        # Membrane resistance (MΩ)
tau_m = Cm / gL    # Membrane time constant (ms)

# Time parameters
dt = 0.2           # Time step (ms)
T = 100            # Total simulation time (ms)
time = np.arange(0, T, dt)

# Refractory settings
t_ref = 2.0
ref_steps = int(np.round(t_ref / dt))
ref_count = 0

# Define input current
I_ext_amp = 5.0
I_ext = np.zeros_like(time)
pulse_times = [5, 60]
for t in pulse_times:
    I_ext[int(t/dt):int((t+10)/dt)] = I_ext_amp

# Initialize membrane potentials
V = np.zeros_like(time)
V[0] = VL
display_V = V.copy()

V_r = np.zeros_like(time)
V_r[0] = VL
display_V_r = V_r.copy()

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
line_V, = ax[1].plot([], [], lw=1, color='royalblue', linestyle=':', label="Membrane Potential no refractory period (V)")
line_V_r, = ax[1].plot([], [], lw=2, color='darkblue', label="Membrane Potential with refractory period (V_r)")
ax[1].legend(fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))

y_no_ref = 1.06
y_ref = 0.94

ax[2].set_xlim(0, T)
ax[2].set_ylim(0.88, 1.12)
ax[2].set_xlabel("Time (ms)", fontsize=12)
ax[2].set_ylabel("Spike Output", fontsize=12)
ax[2].set_yticks([y_no_ref, y_ref])
ax[2].set_yticklabels(["No refractory", "With refractory"])
ax[2].axhline(y=y_no_ref, color="royalblue", linestyle="-", alpha=0.5)
ax[2].axhline(y=y_ref, color="darkblue", linestyle="-", alpha=0.5)

line_spikes, = ax[2].plot([], [], "|", color="royalblue", markersize=24, label="Spikes no refractory period")
line_spikes_r, = ax[2].plot([], [], "|", color="darkblue", markersize=24, label="Spikes with refractory period")

spike_times = []
spike_times_r = []
plt.tight_layout(rect=[0.1, 0, 0.95, 1])
for axis in ax:
    axis.tick_params(axis='both', which='major', labelsize=10)

plt.ion()
plt.show()

# Simulation loop
for i in range(1, len(time)):
    fired = False
    dVdt = ((VL - V[i - 1]) + Rm * I_ext[i]) / tau_m
    V[i] = V[i - 1] + dVdt * dt
    display_V[i] = V[i]
    if V[i] >= VT:
        V[i] = VR
        display_V[i] = VT
        fired = True
        if i + 1 < len(time):
            V[i + 1] = VR
    if fired:
        spike_times.append(time[i])

    fired_r = False
    if ref_count > 0:
        V_r[i] = VR
        display_V_r[i] = VR
        ref_count -= 1
    else:
        dVdt = ((VL - V_r[i - 1]) + Rm * I_ext[i]) / tau_m
        V_r[i] = V_r[i - 1] + dVdt * dt
        display_V_r[i] = V_r[i]
        if V_r[i] >= VT:
            V_r[i] = VR
            display_V_r[i] = VT
            fired_r = True
            ref_count = ref_steps
            if i + 1 < len(time):
                V_r[i + 1] = VR
    if fired_r:
        spike_times_r.append(time[i])

    line_I.set_data(time[:i + 1], I_ext[:i + 1])
    line_spikes.set_data(spike_times, np.full(len(spike_times), y_no_ref))
    line_spikes_r.set_data(spike_times_r, np.full(len(spike_times_r), y_ref))
    line_V_r.set_data(time[:i + 1], display_V_r[:i + 1])
    line_V.set_data(time[:i + 1], display_V[:i + 1])

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)

plt.ioff()
plt.show(block=True)


### Task 3: Explore the firing rate
"""
Let's keep the constant driving current and observe how the current amplitude influences the firing rate of the neuron.
The firing rate is defined as: num_spikes / sec.

Adapt the above code to feed the neuron a constant external current I_ext.
For I_ext use 10 equidistant values from interval [I_min,18], where I_min is your result from task 1.
Keep the original time parameters (simulation duration etc.).
For each driving current, collect the number of produced spikes for both no-refractory-period and with-refractory-period scenarios
and finally use {num_spikes} / {total_simulation_time[sec]} to get the per-second firing rates.

Plot both the no-refractory-period and with-refractory-period firing rates in respect to input current amplitude I_ext.

What is the difference in the spike rates with and without refractory period for I_ext = 18 uA?
"""

#TODO

firing_rate = None
firing_rate_r = None
print(f"Difference in Firing rates: {firing_rate[-1] - firing_rate_r[-1]} spikes/sec at I_ext = 18 uA.")
