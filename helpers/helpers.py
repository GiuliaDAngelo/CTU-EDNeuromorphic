import numpy as np
import cv2
import numpy as np
import cv2
from collections import deque


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
