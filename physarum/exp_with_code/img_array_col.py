import numpy as np
import matplotlib.pyplot as plt

# Example array
array = np.random.randint(0, 255, size=(100, 100, 3), dtype=np.uint8)  # Random 100x100 array with RGB values

# Create a figure and axis
fig, ax = plt.subplots()

# Display the array as an image
ax.imshow(array)

# Remove the axis labels
ax.axis('off')

# Save the image
plt.savefig('output.png', dpi=300, bbox_inches='tight')

# Close the figure
plt.close(fig)
