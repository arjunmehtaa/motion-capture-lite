import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import randint
from itertools import count
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from collections import deque
import time

from filterpy.kalman import KalmanFilter
import numpy as np

def kalman_smoothing(previous_coordinates, current_coordinates):
    # Determine the dimension of the state space
    state_dim = len(current_coordinates)

    # Create a Kalman filter
    kf = KalmanFilter(dim_x=state_dim, dim_z=state_dim)

    # Define the state transition matrix (identity matrix in this case)
    kf.F = np.eye(state_dim)

    # Define the measurement matrix (identity matrix in this case)
    kf.H = np.eye(state_dim)

    # Initialize the state and covariance matrix
    kf.x = np.array(current_coordinates)
    kf.P *= 1e3  # Set initial state covariance to a large value

    # Process noise covariance (tune as needed)
    kf.Q = np.eye(state_dim) * 0.01

    # Measurement noise covariance (tune as needed)
    kf.R = np.eye(state_dim) * 0.1

    kf._alpha_sq = 10
    kf.compute_log_likelihood = False

    # Smoothen the current coordinates using Kalman filter
    for measurement in previous_coordinates:
        kf.predict()
        kf.update(measurement)

    # Get the smoothened coordinates
    smoothened_coordinates = kf.x.tolist()

    return smoothened_coordinates
class Visualization:
    def __init__(self):
        print("Vis initialized")
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Set the limits of the plot
        self.ax.set_xlim([0, 15])
        self.ax.set_ylim([0, 15])
        self.ax.set_zlim([0, 8])

        # Initialize empty scatter plot
        self.scatter = [self.ax.scatter([], [], [], c='r', marker='o')]

        # Initialize a list to store the last 20 points
        self.prev_points = [deque([[0, 0, 0]]), deque([[0, 0, 0]])]

        plt.ion()
        plt.show()

    def animate(self, x, y, z, tag_id):
        # call update in bey

        # find x, y, z in between this x, y, z and previous x, y, z
        x_mid = (x + self.prev_points[tag_id][-1][0]) / 2
        y_mid = (y + self.prev_points[tag_id][-1][1]) / 2
        z_mid = (z + self.prev_points[tag_id][-1][2]) / 2
        print("IN ANIMATION")

        if x <= 1 and self.prev_points[tag_id][-1][0] >= 12:
            x_mid = 15
            x = 15
        if y <= 1 and self.prev_points[tag_id][-1][1] >= 12:
            y_mid = 15
            y = 15
        if z <= 1 and self.prev_points[tag_id][-1][2] >= 12:
            z_mid = 15
            z = 15

        try:
            self.update(x_mid, y_mid, z_mid, tag_id)
            time.sleep(0.1)
            self.update(x, y, z, tag_id)
        except Exception as e:
            print(e)


    def update(self, x, y, z, tag_id: int):
        # print("Update called: ", x, y, z)

        self.ax.clear()
        self.ax.set_xlim([0, 15])
        self.ax.set_ylim([0, 15])
        self.ax.set_zlim([0, 8])

        try:
            if len(self.prev_points[tag_id]) >= 1:
                if x <= 1 and self.prev_points[tag_id][-1][0] >= 12:
                    x = 15
                if y <= 1 and self.prev_points[tag_id][-1][1] >= 12:
                    y = 15
                if z <= 1 and self.prev_points[tag_id][-1][2] >= 12:
                    z = 15
        except Exception as e:
            print("ahodikajsdhjkas", e)

        # Add the new point to the list
        self.prev_points[tag_id].append((x, y, z))

        # If there are more than 5 points, remove the oldest one
        if len(self.prev_points[tag_id]) > 5:
            self.prev_points[tag_id].popleft()
            try:
                print("Before: ", x, y, z)
                x, y, z = kalman_smoothing(self.prev_points[tag_id], (x, y, z))
                print("After:", x, y, z)
            except Exception as e:
                print("kalman error: ", e)
                pass
        
        for tid in range(0, 2):
            color = 'b' if tid == 0 else 'r'
            # Draw lines between the points
            lines = []
            for i in range(len(self.prev_points[tid]) - 1):
                line, = self.ax.plot([self.prev_points[tid][i][0], self.prev_points[tid][i+1][0]], 
                        [self.prev_points[tid][i][1], self.prev_points[tid][i+1][1]], 
                        [self.prev_points[tid][i][2], self.prev_points[tid][i+1][2]], color=color, alpha=(0.2 + i/25))
                lines.append(line)
                x, y, z = self.prev_points[tid][-1]

                self.ax.text(x + 0.8, y + 0.8, z + 0.8, f'({x}, {y}, {z})', color='green', fontsize=8)

                self.scatter = self.ax.scatter(x, y, z, c=z, cmap='viridis')

        self.ax.plot([x, x], [y, y], [0, z], color='r', linestyle=':', alpha=0.5)  # line to x-y plane
        self.ax.plot([x, x], [0, y], [z, z], color='r', linestyle=':', alpha=0.5)  # line to x-z plane
        self.ax.plot([0, x], [y, y], [z, z], color='r', linestyle=':', alpha=0.5)  # line to y-z plane

        plt.pause(0.01)  # Pause for a short period to allow the plot to update
        plt.draw()

if __name__ == "__main__":
    vis = Visualization()
    for i in range(1000):
        vis.update(randint(0, 10), randint(0, 10), randint(0, 1))
        time.sleep(0.5)
