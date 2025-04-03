'''

Giulia D'Angelo, giulia.dangelo@fel.cvut.cz

This tutorial demonstrates the implementation of an egomotion detection system using neuromorphic
vision processing techniques. The system employs Optimized Motion Segmentation (OMS) networks to
analyze event-based frames and generate motion saliency maps. The tutorial covers key steps
including kernel generation, neural network initialization, and the processing pipeline to
detect motion differences between center and surround regions. The output consists of an
OMS-generated motion map, which can be compared with ground-truth segmentation masks.

'''


import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
import torch
import sinabs.layers as sl

import matplotlib

matplotlib.use('TkAgg')  # Set the backend for Matplotlib to TkAgg


# Configuration class to store model parameters
class Config:
    OMS_PARAMS = {
        'size_krn_center': 8,  # Kernel size for the center
        'sigma_center': 1,  # Standard deviation for the center Gaussian kernel
        'size_krn_surround': 8,  # Kernel size for the surround
        'sigma_surround': 4,  # Standard deviation for the surround Gaussian kernel
        'threshold': 0.86,  # Threshold for event detection
        'tau_memOMS': 0.02,  # Membrane time constant for spiking neurons
        'sc': 1,  # Stride for the center kernel
        'ss': 1  # Stride for the surround kernel
    }
    SHOWIMGS = False  # Flag to toggle image display
    maxBackgroundRatio = 2  # Maximum background ratio for filtering
    DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')  # Select device (Mac MPS or CPU)


# Function to compute egomotion by processing input frames through OMS networks
def egomotion(window, net_center, net_surround, device, max_y, max_x, threshold):
    window = window.unsqueeze(0).float().to(device)  # Convert input to float and move to device
    center = net_center(window)  # Process with center kernel
    surround = net_surround(window)  # Process with surround kernel
    events = center - surround  # Compute event difference
    events = 1 - (events - events.min()) / (events.max() - events.min())  # Normalize events
    indexes = events >= threshold  # Apply thresholding

    if indexes.any():
        OMS = torch.zeros_like(events)  # Initialize output tensor
        OMS[indexes] = 255  # Set detected event pixels to maximum value
    else:
        OMS = torch.zeros_like(events)  # Return empty event map if no events detected
    return OMS, indexes


# Function to initialize OMS (Optic Motion Sensor) networks
def initialize_oms(device, OMS_PARAMS):
    """Initialize OMS kernels and networks."""
    center, surround = OMSkernels(
        OMS_PARAMS['size_krn_center'], OMS_PARAMS['sigma_center'],
        OMS_PARAMS['size_krn_surround'], OMS_PARAMS['sigma_surround']
    )
    net_center = net_def(center, OMS_PARAMS['tau_memOMS'], 1, 1,
                         OMS_PARAMS['size_krn_center'], device, OMS_PARAMS['sc'])
    net_surround = net_def(surround, OMS_PARAMS['tau_memOMS'], 1, 1,
                           OMS_PARAMS['size_krn_surround'], device, OMS_PARAMS['ss'])
    return net_center, net_surround


# Function to generate Gaussian kernels for center and surround regions
def OMSkernels(size_krn_center, sigma_center, size_krn_surround, sigma_surround):
    center = gaussian_kernel(size_krn_center, sigma_center).unsqueeze(0)  # Create center kernel
    surround = gaussian_kernel(size_krn_surround, sigma_surround).unsqueeze(0)  # Create surround kernel
    return center, surround


# Function to generate a Gaussian kernel
def gaussian_kernel(size, sigma):
    x = torch.linspace(-size // 2, size // 2, size)
    y = torch.linspace(-size // 2, size // 2, size)
    x, y = torch.meshgrid(x, y, indexing='ij')  # Create coordinate grid
    kernel = torch.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))  # Compute Gaussian function
    kernel = (kernel - kernel.min()) / (kernel.max() - kernel.min())  # Normalize kernel values
    return kernel


# Function to define the neural network for processing event-based data
def net_def(filter, tau_mem, in_ch, out_ch, size_krn, device, stride):
    net = nn.Sequential(
        nn.Conv2d(in_ch, out_ch, (size_krn, size_krn), stride=stride, bias=False),  # Convolutional layer
        sl.LIF(tau_mem),  # Leaky Integrate-and-Fire (LIF) spiking neuron layer
    )
    net[0].weight.data = filter.unsqueeze(1).to(device)  # Assign precomputed filter to convolution layer
    net[1].v_mem = net[1].tau_mem * net[1].v_mem.to(device)  # Initialize membrane potential
    return net




# Load event-based frames and masks from .npy files
evframes = 'data/evimo/seq_00_frames.npy'
evimomasks = 'data/evimo/seq_00_masks.npy'
evframesdata = np.load(evframes, allow_pickle=True)
evmaskdata = np.load(evimomasks, allow_pickle=True)

# Initialize configuration
config = Config()
# Initialize OMS network
net_center, net_surround = initialize_oms(config.DEVICE, config.OMS_PARAMS)

i = 0
fig, axs = plt.subplots(1, 3, figsize=(10, 5))  # Create a figure with 3 subplots
max_x = evframesdata[0].shape[2]
max_y = evmaskdata[0].shape[1]


# Loop through event frames and process them
def process_events():
    global i
    for evframe in evframesdata:
        mask = evmaskdata[i]  # Load corresponding ground truth mask
        OMS, indexes = egomotion(torch.tensor(evframe[0]), net_center, net_surround, config.DEVICE, max_y, max_x,
                                 config.OMS_PARAMS['threshold'])

        # Clear previous images in subplots
        axs[0].cla()
        axs[1].cla()
        axs[2].cla()

        # Display event frame, ground truth mask, and OMS output
        axs[0].imshow(evframe[0])
        axs[0].set_title('Event Frame')
        axs[1].imshow(mask)
        axs[1].set_title('Ground Truth Mask')
        axs[2].imshow(OMS[0].detach().cpu().numpy())
        axs[2].set_title('OMS Output')

        plt.draw()
        plt.pause(0.001)  # Pause to allow visualization update
        i += 1


process_events()
print('Processing completed')