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

# Update function to be called for each animation frame
prev_x = 0
prev_y = 0
prev_z = 0

def update(frame):
    global prev_x, prev_y, prev_z

    x = randint(0, 10)
    y = randint(0, 10)
    z = randint(0, 10)

    ax.clear()
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    ax.set_zlim([0, 10])

    line, = ax.plot([prev_x, x], [prev_y, y], [prev_z, z], color='r')
    prev_x = x
    prev_y = y
    prev_z = z

    return line,

# Create animation
ani = FuncAnimation(fig, update, frames=count(1), interval=100)

# Show the plot
plt.show()