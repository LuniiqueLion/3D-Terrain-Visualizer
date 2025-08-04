import numpy as np
import matplotlib.pyplot as plt


def thrust_profile(t):
    return 10000 if t < 20 else 0

def simulate_rocket_trajectory(time_interval, time_step, initial_position, initial_velocity, initial_mass, thrust_profile, tilt_angles, num_points=20):
    # Initialize lists to store trajectory data
    time_points = []
    x_points, y_points, z_points = [], [], []

    # Constants (unchanged)
    drag_coefficient = 0.2
    density_air = 1.225
    reference_area = 5
    gravitational_acceleration = 9.81

    # Unpack tilt angles
    pitch_angle, yaw_angle, roll_angle = tilt_angles

    # Initial conditions (unchanged)
    x, y, z = initial_position
    vx, vy, vz = initial_velocity
    mass = initial_mass

    # Run the simulation until the rocket touches the ground
    num_points = 0
    while z >= 0 and num_points<20:
        thrust = thrust_profile(time_interval)*10
        if mass > 0:
            drag = 0.5 * drag_coefficient * density_air * reference_area * np.linalg.norm([vx, vy, vz]) ** 2
        else:
            drag = 0
        num_points +=1
        ax = thrust / mass - drag / mass
        ay, az = 0, 0

        # Rotation matrices for pitch, yaw, and roll
        rotation_matrix_pitch = np.array([[1, 0, 0], [0, np.cos(pitch_angle), -np.sin(pitch_angle)], [0, np.sin(pitch_angle), np.cos(pitch_angle)]])
        rotation_matrix_yaw = np.array([[np.cos(yaw_angle), 0, np.sin(yaw_angle)], [0, 1, 0], [-np.sin(yaw_angle), 0, np.cos(yaw_angle)]])
        rotation_matrix_roll = np.array([[np.cos(roll_angle), -np.sin(roll_angle), 0], [np.sin(roll_angle), np.cos(roll_angle), 0], [0, 0, 1]])

        # Rotate velocity vector
        velocity_vector = np.array([vx, vy, vz])
        rotated_velocity = np.dot(rotation_matrix_roll, np.dot(rotation_matrix_pitch, np.dot(rotation_matrix_yaw, velocity_vector)))

        # Update position with tilted velocity
        x += rotated_velocity[0] * time_step
        y += rotated_velocity[1] * time_step
        z += rotated_velocity[2] * time_step

        vx += ax * time_step
        vy += ay * time_step
        vz += az * time_step

        mass -= thrust / 5000 * time_step

        # Append current coordinates to the lists
        time_points.append(time_interval)
        x_points.append(x)
        y_points.append(y)
        z_points.append(z)

        # Update time for the next iteration
        time_interval += time_step

    return time_points, x_points, y_points, z_points


time_interval = 0
time_step = 0.1

# Initial conditions
initial_position = (0, 28, 0)
initial_velocity = (0, 0, 0)
initial_mass = 1000
tilt_angles = (np.pi/4,np.pi/4,np.pi/4)
# Simulate rocket trajectory


time_points, x_points, y_points, z_points = simulate_rocket_trajectory(
    time_interval, time_step, initial_position, initial_velocity, initial_mass, thrust_profile, tilt_angles
)
plt.plot(time_points, x_points, label='X-coordinate')
plt.plot(time_points, y_points, label='Y-coordinate')
plt.plot(time_points, z_points, label='Z-coordinate')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()
plt.show()
