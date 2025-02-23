import numpy as np
import cv2
import numpy as np
import cv2
from collections import deque
from scipy.special import iv
import torch
import numpy as np
from scipy.special import iv
import torch
import torch.nn as nn
import sinabs.layers as sl
from skimage.transform import rescale, resize, downscale_local_mean
import torchvision
import torch.nn.functional as F


def time_window(events, camera_events,height, width,window_period):
    # Extract the 'x' and 'y' coordinates of events, their timestamps ('ts'), and polarity ('pol')
    e_x = events['data'][camera_events]['dvs']['x']  # x-coordinates of events
    e_y = events['data'][camera_events]['dvs']['y']  # y-coordinates of events
    e_ts = np.multiply(events['data'][camera_events]['dvs']['ts'], 10 ** 3)  # Convert timestamps to milliseconds
    e_pol = events['data'][camera_events]['dvs']['pol']  # Event polarity (1 for ON events, 0 for OFF events)

    ### Binning Events for Fixed Time Window ###
    time = window_period
    # Create empty windows to store event data for positive and negative events
    window_pos = np.zeros((height, width))
    window_neg = np.zeros((height, width))

    # Loop through all the events (x, y, timestamp, polarity)
    for x, y, ts, pol in zip(e_x, e_y, e_ts, e_pol):
        # Check if the event timestamp is within the current time window
        if ts <= time:
            # Set the pixel based on the polarity of the event
            if pol == 1:
                window_pos[y][x] = 255  # Bright pixel for ON events
            else:
                window_neg[y][x] = 255  # Bright pixel for OFF events
        else:
            # If the event is outside the window period, display the current window of events
            cv2.imshow('Event Pos and Neg', np.hstack((window_pos, window_neg)))  # Show combined image
            cv2.waitKey(1)  # Allow the plot to be displayed interactively

            # Update the time for the next window
            time += window_period
            # Reset the windows for the next batch of events
            window_pos.fill(0)
            window_neg.fill(0)


def sliding_window(events, camera_events, height, width, initial_window_period, sliding_wdw, time_buff):
    # Extract event data (X, Y coordinates, timestamps, and polarity)
    e_x = events['data'][camera_events]['dvs']['x']  # X-coordinates of events
    e_y = events['data'][camera_events]['dvs']['y']  # Y-coordinates of events
    e_ts = np.multiply(events['data'][camera_events]['dvs']['ts'], 10 ** 3)  # Convert timestamps to milliseconds
    e_pol = events['data'][camera_events]['dvs']['pol']  # Event polarity (1 = ON, 0 = OFF)

    # Initialize sliding window visualization arrays
    sliding_window_pos = np.zeros((height, width), dtype=np.uint8)  # Stores ON events
    sliding_window_neg = np.zeros((height, width), dtype=np.uint8)  # Stores OFF events
    event_queue = deque()  # Queue to track events within the window

    # Process the initial window of events
    for x, y, ts, pol in zip(e_x, e_y, e_ts, e_pol):
        if ts <= initial_window_period:
            # Assign event polarity to the correct visualization matrix
            if pol == 1:
                sliding_window_pos[y][x] = 255  # Mark ON events in white
            else:
                sliding_window_neg[y][x] = 255  # Mark OFF events in white
            event_queue.append((x, y, ts, pol))  # Store the event for future updates
        else:
            # Start processing sliding window updates
            if ts <= initial_window_period + time_buff:
                # Remove old events outside the sliding window
                while event_queue and event_queue[0][2] < ts - initial_window_period:
                    old_event = event_queue.popleft()
                    x_old, y_old, ts_old, pol_old = old_event
                    if pol_old == 1:
                        sliding_window_pos[y_old][x_old] = 0  # Remove old ON event
                    else:
                        sliding_window_neg[y_old][x_old] = 0  # Remove old OFF event
                # Add new event to visualization
                if pol == 1:
                    sliding_window_pos[y][x] = 255
                else:
                    sliding_window_neg[y][x] = 255
                event_queue.append((x, y, ts, pol))  # Store event in queue
            else:
                # Update display and allow continuous visualization
                cv2.imshow('Event Pos and Neg', np.hstack((sliding_window_pos, sliding_window_neg)))
                cv2.waitKey(1)
                time_buff += sliding_wdw  # Expand time buffer for next updates


def number_events(events, camera_events, height, width, num_events):
    # Extract the 'x' and 'y' coordinates of events, their timestamps ('ts'), and polarity ('pol')
    e_x = events['data'][camera_events]['dvs']['x']  # x-coordinates of events
    e_y = events['data'][camera_events]['dvs']['y']  # y-coordinates of events
    e_ts = np.multiply(events['data'][camera_events]['dvs']['ts'], 10 ** 3)  # Convert timestamps to milliseconds
    e_pol = events['data'][camera_events]['dvs']['pol']  # Event polarity (1 for ON events, 0 for OFF events)

    ### Binning Events for Fixed Event Count Window ###
    # Create empty windows to store event data for positive and negative events
    window_pos = np.zeros((height, width))
    window_neg = np.zeros((height, width))

    # Loop through events in batches of 'num_events'
    for i in range(0, len(e_x), num_events):
        # Reset the windows for the next batch of events
        window_pos.fill(0)
        window_neg.fill(0)

        # Process the next 'num_events' events
        for j in range(i, min(i + num_events, len(e_x))):
            x, y, pol = e_x[j], e_y[j], e_pol[j]
            if pol == 1:
                window_pos[y][x] = 255  # Bright pixel for ON events
            else:
                window_neg[y][x] = 255  # Bright pixel for OFF events

        # Display the current window of events
        cv2.imshow('Event Pos and Neg', np.hstack((window_pos, window_neg)))
        cv2.waitKey(1)  # Allow the plot to be displayed interactively

def net_def(filter, tau_mem, in_ch, out_ch, size_krn, device, stride):
    # define our single layer network and load the filters
    net = nn.Sequential(
        nn.Conv2d(in_ch, out_ch, (size_krn,size_krn),  stride=stride, bias=False),
        sl.LIF(tau_mem),
    )
    net[0].weight.data = filter.unsqueeze(1).to(device)
    net[1].v_mem = net[1].tau_mem * net[1].v_mem.to(device)
    return net


def initialise_attention(device, ATTENTION_PARAMS):
    vm_kernels = VMkernels(
        ATTENTION_PARAMS['thetas'], ATTENTION_PARAMS['size_krn'],
        ATTENTION_PARAMS['rho'], ATTENTION_PARAMS['r0'], ATTENTION_PARAMS['thick'],
        ATTENTION_PARAMS['offset'], ATTENTION_PARAMS['fltr_resize_perc']
    )
    net_attention = net_def(vm_kernels, ATTENTION_PARAMS['tau_mem'], ATTENTION_PARAMS['num_pyr'], ATTENTION_PARAMS['out_ch'],
                         ATTENTION_PARAMS['size_krn'], device, ATTENTION_PARAMS['stride'])

    return net_attention


def VMkernels(thetas, size, rho, r0, thick, offset,fltr_resize_perc):
    """
    Create a set of Von Mises filters with different orientations.

    Args:
        thetas (np.ndarray): Array of angles in radians.
        size (int): Size of the filter.
        rho (float): Scale coefficient to control arc length.
        r0 (int): Radius shift from the center.

    Returns:
        filters (list): List of Von Mises filters.
    """
    filters = []
    for theta in thetas:
        filter = vm_filter(theta, size, rho=rho, r0=r0, thick=thick, offset=offset)
        filter = rescale(filter, fltr_resize_perc, anti_aliasing=False)
        filters.append(filter)
    filters = torch.tensor(np.stack(filters).astype(np.float32))
    return filters


def vm_filter(theta, scale, rho=0.1, r0=0, thick=0.5, offset=(0, 0)):
    """Generate a Von Mises filter with r0 shifting and an offset."""
    height, width = scale, scale
    vm = np.empty((height, width))
    offset_x, offset_y = offset

    for x in range(width):
        for y in range(height):
            # Shift X and Y based on r0 and offset
            X = (x - width / 2) + r0 * np.cos(theta) - offset_x * np.cos(theta)
            Y = (height / 2 - y) + r0 * np.sin(theta) - offset_y * np.sin(theta)  # Inverted Y for correct orientation
            r = np.sqrt(X**2 + Y**2)
            angle = zero_2pi_tan(X, Y)

            # Compute the Von Mises filter value
            vm[y, x] = np.exp(thick*rho * r0 * np.cos(angle - theta)) / iv(0, r - r0)
    # normalise value between -1 and 1
    # vm = vm / np.max(vm)
    # vm = vm * 2 - 1
    return vm


def zero_2pi_tan(x, y):
    """
    Compute the angle in radians between the positive x-axis and the point (x, y),
    ensuring the angle is in the range [0, 2π].

    Args:
        x (float): x-coordinate of the point.
        y (float): y-coordinate of the point.

    Returns:
        angle (float): Angle in radians, between 0 and 2π.
    """
    angle = np.arctan2(y, x) % (2 * np.pi)  # Get the angle in radians and wrap it in the range [0, 2π]
    return angle


def run_attention(window, net, device, resolution, num_pyr):
    # Create resized versions of the frames
    resized_frames = [torchvision.transforms.Resize((int(resolution[0] / num_pyr), int(resolution[1] / num_pyr)))(
        window) for pyr in range(1, num_pyr + 1)]

    # Process frames in batches
    batch_frames = torch.stack(
        [torchvision.transforms.Resize((resolution[0], resolution[1]))(window) for window in resized_frames]).type(torch.float32)
    batch_frames = batch_frames.to(device)  # Move to GPU if available
    output_rot = net(batch_frames)
    # Sum the outputs over rotations and scales
    output_rot_sum = torch.sum(torch.sum(output_rot, dim=1, keepdim=True), dim=0, keepdim=True).type(torch.float32).cpu().detach()
    salmap = torchvision.transforms.Resize((resolution[0], resolution[1]))(output_rot_sum).squeeze(0).squeeze(
        0)
    salmax_coords = np.unravel_index(torch.argmax(salmap).cpu().numpy(), salmap.shape)
    # normalise salmap for visualization
    salmap = salmap.detach().cpu().numpy()
    salmap = np.array((salmap - salmap.min()) / (salmap.max() - salmap.min()) * 255)
    return salmap,salmax_coords