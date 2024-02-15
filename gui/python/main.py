import matplotlib.pyplot as plt
import numpy as np
import time

# Function to generate random points
def generate_random_point():
    return np.random.rand(2)

# Set the delay between points in seconds
delay_seconds = 0.1

points = [(0, 0), (0, 0), (0, 0), (0, 0)]

# Infinite loop to continuously generate and plot random points
while True:
    # Generate a random point and add it to the list
    print(points)
    points.pop(0)
    points.append(generate_random_point())

    # Extract x and y coordinates from the points
    x_coordinates, y_coordinates = zip(*points)

    # Clear the previous plot
    plt.clf()

    # Plot the points
    plt.scatter(x_coordinates, y_coordinates, label='Random Points')
    plt.title('Random Points Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()

    # Draw and pause for the specified delay
    plt.draw()
    plt.pause(delay_seconds)

# You might need to add this at the end to ensure the window stays open
plt.show(block=True)