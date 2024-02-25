import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import randint
from itertools import count
from matplotlib.animation import FuncAnimation
import numpy as np

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the limits of the plot
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
ax.set_zlim([0, 10])

# Initialize empty scatter plot
scatter = [ax.scatter([], [], [], c='r', marker='o')]

# Initialize a list to store the last 5 points
prev_points = [[0, 0, 0]]

def update(frame):
    global prev_points

    # Generate a random point x, y, z that is a multiple of 0.1 and is a maximum of +-1 away from the previous point (and between 0 and 10)
    x = prev_points[-1][0] + 2*(randint(-10, 10) / 10)
    x = np.clip(x, 0, 10).round(1)
    y = prev_points[-1][1] + 2*(randint(-10, 10) / 10)
    y = np.clip(y, 0, 10).round(1)
    z = prev_points[-1][2] + 2*(randint(-10, 10) / 10)
    z = np.clip(z, 0, 10).round(1)
    ax.clear()
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    ax.set_zlim([0, 10])

    # Add the new point to the list
    prev_points.append((x, y, z))

    # If there are more than 5 points, remove the oldest one
    if len(prev_points) > 20:
        prev_points.pop(0)

    # Draw lines between the points
    lines = []
    for i in range(len(prev_points) - 1):
        line, = ax.plot([prev_points[i][0], prev_points[i+1][0]], 
                [prev_points[i][1], prev_points[i+1][1]], 
                [prev_points[i][2], prev_points[i+1][2]], color='b', alpha=(0.2 + i/25))
        lines.append(line)

    scatter = ax.scatter(x, y, z, c=z, cmap='viridis')

    ax.plot([x, x], [y, y], [0, z], color='r', linestyle=':', alpha=0.5)  # line to x-y plane
    ax.plot([x, x], [0, y], [z, z], color='r', linestyle=':', alpha=0.5)  # line to x-z plane
    ax.plot([0, x], [y, y], [z, z], color='r', linestyle=':', alpha=0.5)  # line to y-z plane

    ax.text(x + 0.8, y + 0.8, z + 0.8, f'({x}, {y}, {z})', color='green', fontsize=8)
    return lines,

# Create animation
ani = FuncAnimation(fig, update, frames=count(1), interval=500)

# Show the plot
# fig.patch.set_facecolor('gray')

plt.show()