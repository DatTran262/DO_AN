# def read_file(file_path, encoding='utf-8'):
#     try:
#         with open(file_path, 'r', encoding=encoding) as file:
#             lines = file.readlines()
#             return lines
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# def main():
#     file_path = 'Action.txt'  # Thay thế bằng đường dẫn tới file của bạn

#     lines = read_file(file_path)

#     if lines is not None:
#         print("Array content:")
#         array_content = [line.strip() for line in lines]
#         print(array_content)

# if __name__ == "__main__":
#     main()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define DH parameters for a simple leg
# (Modify these parameters according to your robot configuration)
L1 = 1.0  # Length of link 1
L2 = 1.0  # Length of link 2
L3 = 0.5  # Length of link 3

# Function to compute forward kinematics
def forward_kinematics(theta1, theta2, theta3):
    x = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2) + L3 * np.sin(theta1 + theta2 + theta3)
    y = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2) + L3 * np.cos(theta1 + theta2 + theta3)
    z = -L1 * np.cos(theta2) - L2 * np.cos(theta2 + theta3) + L3 * np.cos(theta2 + theta3)
    return x, y, z

# Number of frames for animation
frames = 100

# Initialize joint angles
theta1 = np.linspace(0, np.pi / 2, frames)
theta2 = np.linspace(0, np.pi / 2, frames)
theta3 = np.linspace(0, np.pi / 2, frames)

# Create figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create line object for leg
line, = ax.plot([], [], [], 'o-', lw=2)

# Set axis limits
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

# Function to update plot during animation
def update_plot(frame, line, theta1, theta2, theta3):
    x, y, z = forward_kinematics(theta1[frame], theta2[frame], theta3[frame])
    line.set_data([0, x], [0, y])
    line.set_3d_properties([0, z])
    return line,

# Create animation
ani = FuncAnimation(fig, update_plot, frames=frames, fargs=(line, theta1, theta2, theta3), blit=True)

# Show plot
plt.show()


