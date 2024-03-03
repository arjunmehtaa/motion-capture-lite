import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import randint
from itertools import count
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from collections import deque

class Visualization:
    def __init__(self):
        print("Vis initialized")
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # Set the limits of the plot
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])

        # Initialize empty scatter plot
        self.scatter = [self.ax.scatter([], [], [], c='r', marker='o')]

        # Initialize a list to store the last 20 points
        self.prev_points = deque([[0, 0, 0]])

        plt.ion()
        plt.show()

    def update(self, x, y, z):
        # print("Update called: ", x, y, z)

        self.ax.clear()
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])

        # Add the new point to the list
        self.prev_points.append((x, y, z))

        # If there are more than 5 points, remove the oldest one
        if len(self.prev_points) > 5:
            self.prev_points.popleft()

        # Draw lines between the points
        lines = []
        for i in range(len(self.prev_points) - 1):
            line, = self.ax.plot([self.prev_points[i][0], self.prev_points[i+1][0]], 
                    [self.prev_points[i][1], self.prev_points[i+1][1]], 
                    [self.prev_points[i][2], self.prev_points[i+1][2]], color='b', alpha=(0.2 + i/25))
            lines.append(line)

        self.scatter = self.ax.scatter(x, y, z, c=z, cmap='viridis')

        self.ax.plot([x, x], [y, y], [0, z], color='r', linestyle=':', alpha=0.5)  # line to x-y plane
        self.ax.plot([x, x], [0, y], [z, z], color='r', linestyle=':', alpha=0.5)  # line to x-z plane
        self.ax.plot([0, x], [y, y], [z, z], color='r', linestyle=':', alpha=0.5)  # line to y-z plane

        self.ax.text(x + 0.8, y + 0.8, z + 0.8, f'({x}, {y}, {z})', color='green', fontsize=8)
        plt.pause(0.1)  # Pause for a short period to allow the plot to update
        plt.draw()

if __name__ == "__main__":
    vis = Visualization()
    for i in range(10):
        vis.update(randint(0, 10), randint(0, 10), randint(0, 10))
        time.sleep(0.1)
