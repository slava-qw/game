import cv2
import numpy as np

# Set the dimensions of the video frames
frame_width, frame_height = 100, 100

# Define the frame rate (in frames per second)
fps = 24.0

# Create a VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_out = cv2.VideoWriter('output2.mp4', fourcc, fps, (frame_width, frame_height))

# Define the color gradient range
start_color = np.array([255, 0, 0], dtype=np.uint8)  # Starting color (red)
end_color = np.array([0, 0, 255], dtype=np.uint8)  # Ending color (blue)

num_frames = 100  # Number of frames in the video

for i in range(num_frames):
    # Calculate the color at the current frame
    alpha = i / (num_frames - 1)  # Interpolation factor
    color = (1 - alpha) * start_color + alpha * end_color

    # Create a frame with the current color
    frame = np.full((frame_height, frame_width, 3), color, dtype=np.uint8)

    # Write the frame to the video file
    video_out.write(frame)

video_out.release()
