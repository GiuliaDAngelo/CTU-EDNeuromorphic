#!/usr/bin/env python3
"""
Tutorial 7 - OMS (Object Motion Sensitivity)

This tutorial demonstrates an SNN object motion segmentation system using 
neuromorphic vision processing techniques.

The system employs **Optimized Motion Sensitivity (OMS)** cells to analyze 
event-based frames and generate motion segmentation. The tutorial covers key 
steps including kernel generation, neural network initialization, and the 
processing pipeline to detect local motion differences between center and 
surround regions.

Structure:
1. Define configuration, Gaussian kernels, and OMS networks.
2. Load EVIMO data (frames + masks).
3. Run dynamic visualization using matplotlib.

Authors: Giulia D'Angelo, giulia.dangelo@fel.cvut.cz
"""

# ============================================================================
# 1. Import libraries and configuration
# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import sinabs.layers as sl
import matplotlib

matplotlib.use('TkAgg')  # Set the backend for Matplotlib to TkAgg


# Global OMS configuration and execution device.
class Config:
    """Configuration class for OMS network parameters."""
    OMS_PARAMS = {
        'size_krn_center': 8,
        'sigma_center': 1,
        'size_krn_surround': 8,
        'sigma_surround': 4,
        'threshold': 0.86,
        'tau_memOMS': 0.02,
        'sc': 1,
        'ss': 1
    }
    SHOWIMGS = False
    maxBackgroundRatio = 2
    DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')


# ============================================================================
# 2. OMS Model Definition
# ============================================================================
# This section defines:
# - Model parameters (kernel sizes, threshold, membrane time constant).
# - Center/surround Gaussian kernel generation.
# - Spiking branch architecture using Conv2d + LIF.
#
# The `egomotion(...)` function returns a binary OMS map that highlights 
# salient motion areas.

def egomotion(window, net_center, net_surround, device, max_y, max_x, threshold):
    """
    Compute the OMS (Optimized Motion Sensitivity) output for an event frame.
    
    Args:
        window: Input event frame tensor
        net_center: Center pathway network
        net_surround: Surround pathway network
        device: PyTorch device (cpu or mps)
        max_y: Maximum y dimension
        max_x: Maximum x dimension
        threshold: Threshold for binarization
        
    Returns:
        OMS: Binary OMS map (0 or 255)
        indexes: Boolean map of pixels above threshold
    """
    # Convert frame to 4D tensor expected by Conv2D: [B, C, H, W].
    window = window.unsqueeze(0).float().to(device)
    center = net_center(window)
    surround = net_surround(window)

    # Center-surround difference highlights salient motion.
    events = center - surround

    # Safe normalization to avoid division by zero.
    eps = 1e-8
    events = 1 - (events - events.min()) / (events.max() - events.min() + eps)
    indexes = events >= threshold

    # Binary OMS map (0 or 255).
    if indexes.any():
        OMS = torch.zeros_like(events)
        OMS[indexes] = 255
    else:
        OMS = torch.zeros_like(events)

    return OMS, indexes


def initialize_oms(device, oms_params):
    """
    Build and initialize the OMS center and surround branches.
    
    Args:
        device: PyTorch device
        oms_params: Dictionary of OMS parameters
        
    Returns:
        net_center: Center pathway network
        net_surround: Surround pathway network
    """
    # Build center/surround kernels and initialize both OMS branches.
    center, surround = OMSkernels(
        oms_params['size_krn_center'], oms_params['sigma_center'],
        oms_params['size_krn_surround'], oms_params['sigma_surround']
    )

    net_center = net_def(
        center, oms_params['tau_memOMS'], 1, 1,
        oms_params['size_krn_center'], device, oms_params['sc']
    )
    net_surround = net_def(
        surround, oms_params['tau_memOMS'], 1, 1,
        oms_params['size_krn_surround'], device, oms_params['ss']
    )
    return net_center, net_surround


def OMSkernels(size_krn_center, sigma_center, size_krn_surround, sigma_surround):
    """Generate center and surround Gaussian kernels."""
    center = gaussian_kernel(size_krn_center, sigma_center).unsqueeze(0)
    surround = gaussian_kernel(size_krn_surround, sigma_surround).unsqueeze(0)
    return center, surround


def gaussian_kernel(size, sigma):
    """
    Create a 2D Gaussian kernel normalized to [0, 1].
    
    Args:
        size: Kernel size
        sigma: Standard deviation of the Gaussian
        
    Returns:
        Normalized 2D Gaussian kernel tensor
    """
    x = torch.linspace(-size // 2, size // 2, size)
    y = torch.linspace(-size // 2, size // 2, size)
    x, y = torch.meshgrid(x, y, indexing='ij')
    kernel = torch.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    kernel = (kernel - kernel.min()) / (kernel.max() - kernel.min())
    return kernel


def net_def(filter_kernel, tau_mem, in_ch, out_ch, size_krn, device, stride):
    """
    Define an OMS processing branch (Conv2d + LIF spiking neuron).
    
    Args:
        filter_kernel: Convolutional kernel weights
        tau_mem: Membrane time constant
        in_ch: Number of input channels
        out_ch: Number of output channels
        size_krn: Kernel size
        device: PyTorch device
        stride: Stride for convolution
        
    Returns:
        Sequential network module
    """
    # Each OMS branch is a fixed convolution followed by a spiking LIF neuron.
    net = nn.Sequential(
        nn.Conv2d(in_ch, out_ch, (size_krn, size_krn), stride=stride, bias=False),
        sl.LIF(tau_mem),
    )
    net[0].weight.data = filter_kernel.unsqueeze(1).to(device)
    net[1].v_mem = net[1].tau_mem * net[1].v_mem.to(device)
    return net


# ============================================================================
# 3. Data Loading and Network Initialization
# ============================================================================
# Load EVIMO event frames and segmentation masks, then initialize the OMS 
# center/surround networks.
# The printed summary helps verify dataset size and selected device (mps or cpu).

print("="*80)
print("Tutorial 7 - OMS (Object Motion Sensitivity)")
print("="*80)
print("\nLoading data and initializing networks...\n")

# Paths to EVIMO frames and corresponding ground-truth masks.
evframes = 'data/evimo/seq_00_frames.npy'
evimomasks = 'data/evimo/seq_00_masks.npy'

# Load event frames and masks from NumPy files.
evframesdata = np.load(evframes, allow_pickle=True)
evmaskdata = np.load(evimomasks, allow_pickle=True)

# Build configuration and initialize the two OMS branches.
config = Config()
net_center, net_surround = initialize_oms(config.DEVICE, config.OMS_PARAMS)

# Store spatial dimensions used in the processing loop.
max_x = evframesdata[0].shape[2]
max_y = evmaskdata[0].shape[1]

print(f'Loaded frames: {len(evframesdata)}')
print(f'Loaded masks: {len(evmaskdata)}')
print(f'Device: {config.DEVICE}')


# ============================================================================
# 4. Dynamic Visualization
# ============================================================================
# This step processes each event frame and shows three synchronized views:
# 1. Input event frame.
# 2. Ground-truth segmentation mask.
# 3. OMS saliency output.

print("\n" + "="*80)
print("Dynamic Visualization")
print("="*80)
print("\nProcessing and visualizing frames...\n")

DISPLAY_MODE = "window"  # Interactive window mode for visualization

fig, axs = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('OMS Object Motion Segmentation Visualization')

# Flag to track if escape key was pressed
escape_pressed = {'flag': False}


def on_key_press(event):
    """Handle key press events. Press ESC to stop visualization."""
    if event.key == 'escape':
        escape_pressed['flag'] = True
        print("\nEscape key pressed. Stopping visualization...")
        plt.close(fig)


# Connect the key press event to the figure
fig.canvas.mpl_connect('key_press_event', on_key_press)


def process_events(display_mode=DISPLAY_MODE, pause_s=0.03):
    """
    Process all event frames and display results with ground truth and OMS output.
    
    Args:
        display_mode: "window" for interactive matplotlib
        pause_s: Pause duration between frames in seconds
    """
    frame_count = 0
    for i, evframe in enumerate(evframesdata):
        # Check if escape was pressed
        if escape_pressed['flag']:
            break

        mask = evmaskdata[i]
        OMS, indexes = egomotion(
            torch.tensor(evframe[0]),
            net_center,
            net_surround,
            config.DEVICE,
            max_y,
            max_x,
            config.OMS_PARAMS['threshold']
        )

        # Refresh subplot content at each frame.
        axs[0].cla()
        axs[1].cla()
        axs[2].cla()

        axs[0].imshow(evframe[0])
        axs[0].set_title('Event Frame')
        axs[0].axis('off')

        axs[1].imshow(mask)
        axs[1].set_title('Ground Truth Mask')
        axs[1].axis('off')

        oms_display = OMS[0].detach().cpu().numpy()
        axs[2].imshow(oms_display, cmap='gray')
        axs[2].set_title('OMS Output')
        axs[2].axis('off')

        fig.suptitle(f'OMS Visualization - Frame {i+1}/{len(evframesdata)} (Press ESC to stop)')

        if display_mode == "window":
            # Update the external interactive window.
            fig.canvas.draw_idle()
            fig.canvas.flush_events()

        plt.pause(pause_s)
        frame_count += 1

    if not escape_pressed['flag']:
        print(f'Processing completed: {frame_count} frames visualized')
    else:
        print(f'Processing stopped by user: {frame_count} frames visualized')


process_events()
plt.show()


# ============================================================================
# 5. Exercise: Compute OMS Motion Score
# ============================================================================
# GOAL: Compute a numeric OMS motion score on one frame.
# Expected Output:
# - frame index (integer)
# - motion ratio (%) in [0, 100]

print("\n" + "="*80)
print("Exercise: OMS Motion Score Calculation")
print("="*80 + "\n")

# Reference solution
frame_idx = np.random.randint(len(evframesdata))
threshold = config.OMS_PARAMS['threshold']

# 1) Select one event frame and convert it to a tensor.
frame_tensor = torch.tensor(evframesdata[frame_idx][0])

# 2) Run OMS on that frame.
oms_map, _ = egomotion(
    frame_tensor,
    net_center,
    net_surround,
    config.DEVICE,
    max_y,
    max_x,
    threshold
)

# 3) Compute the percentage of motion pixels (OMS == 255).
motion_ratio = (oms_map[0] == 255).float().mean().item() * 100.0

print(f"Frame index: {frame_idx}")
print(f"Motion ratio (%): {motion_ratio:.2f}")

# Simple sanity check: result must be a valid percentage.
assert 0.0 <= motion_ratio <= 100.0, "motion_ratio must be in [0, 100]"


# ============================================================================
# 6. Analysis and Questions
# ============================================================================

print("\n" + "="*80)
print("Questions for Further Exploration:")
print("="*80)
print("""
1. How does the difference between center and surround responses contribute 
   to motion segmentation in the OMS network?

2. Why is it important to normalize the Gaussian kernels in the gaussian_kernel 
   function, and how does this affect the processing of event-based frames?

3. Try varying the OMS_PARAMS (threshold, kernel sizes, sigma values) and observe 
   how the segmentation quality changes. Which parameters have the most impact?
""")

print("="*80)
print("Tutorial 7 completed!")
print("="*80)