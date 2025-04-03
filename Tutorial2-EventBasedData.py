import tonic
import cv2
import numpy as np

'''
Giulia D'Angelo, giulia.dangelo@fel.cvut.cz


In this tutorial, we will load and visualize event-based data from the DVSGesture dataset.
This dataset consists of events captured by a Dynamic Vision Sensor (DVS), which records changes
in the scene over time with high temporal resolution.

We will convert the events into frames for both positive and negative polarities, allowing us to
visualize how the sensor responds to different stimuli. The output will be a concatenated display
of frames representing the two polarities, enabling us to analyze the data more effectively.
'''


# Step 1: Load the Events from the DVSGesture Dataset
# Specify the path to your dataset
path = 'data/'
dvs_training = tonic.datasets.DVSGesture(path, train=True)

# Define parameters for the event processing
time_window = 10000  # Time window in microseconds (10 ms)
user_trial = 1      # Index of the user trial to analyze

# Load events and corresponding numpy data for the specified trial
events, npys = dvs_training[user_trial]

# Transform events into frames using the specified time window
transform = tonic.transforms.ToFrame(
    sensor_size=dvs_training.sensor_size,
    time_window=time_window  # Convert events to frames based on the time window
)
frames = transform(events)  # Generate frames from events

# Output the number of frames generated
print(f"Number of frames: {len(frames)}")

# Step 2: Visualize the Frames
for i, frame in enumerate(frames):
    print(f"Displaying frame {i}")

    # Concatenate the two polarities into a single frame for visualization
    concatenated_frame = np.hstack((
        cv2.cvtColor(frame[0].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR),  # Positive events
        cv2.cvtColor(frame[1].astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR)   # Negative events
    ))

    # Display the concatenated frame in a window
    cv2.imshow('Positive and Negative Polarities', concatenated_frame)
    cv2.waitKey(1)  # Wait for 1 millisecond before displaying the next frame

# Clean up and close all OpenCV windows (optional)
cv2.destroyAllWindows()
