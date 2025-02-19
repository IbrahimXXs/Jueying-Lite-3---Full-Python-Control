import socket
import struct
import time

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def set_combined_velocity():
    """
    Sets the Angular Velocity, Linear Velocity in X, and Linear Velocity in Y.
    Asks the user for how long the command should run (in seconds) and ensures
    the issue frequency is not lower than 20Hz.
    """
    angular_velocity_range = [-1.5, 1.5]
    linear_velocity_x_range = [-1.0, 1.0]
    linear_velocity_y_range = [-0.5, 0.5]

    try:
        # Get user inputs
        angular_velocity = float(input(f"Enter Angular Velocity (rad/s) [{angular_velocity_range[0]} to {angular_velocity_range[1]}]: "))
        if angular_velocity < angular_velocity_range[0] or angular_velocity > angular_velocity_range[1]:
            print(f"Error: Angular Velocity must be within range {angular_velocity_range}.")
            return

        linear_velocity_x = float(input(f"Enter Linear Velocity in X-axis (m/s) [{linear_velocity_x_range[0]} to {linear_velocity_x_range[1]}]: "))
        if linear_velocity_x < linear_velocity_x_range[0] or linear_velocity_x > linear_velocity_x_range[1]:
            print(f"Error: Linear Velocity in X must be within range {linear_velocity_x_range}.")
            return

        linear_velocity_y = float(input(f"Enter Linear Velocity in Y-axis (m/s) [{linear_velocity_y_range[0]} to {linear_velocity_y_range[1]}]: "))
        if linear_velocity_y < linear_velocity_y_range[0] or linear_velocity_y > linear_velocity_y_range[1]:
            print(f"Error: Linear Velocity in Y must be within range {linear_velocity_y_range}.")
            return

        duration = float(input("Enter the duration to run the command (in seconds): "))
        if duration <= 0:
            print("Error: Duration must be greater than 0.")
            return

        # Calculate the number of iterations (20Hz = 50ms interval)
        interval = 1 / 20  # 20Hz = 50ms
        iterations = int(duration / interval)

        # Pack the commands into complex command format
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for i in range(iterations):
            # Pack Angular Velocity Command
            angular_command_head = struct.pack('<III', 0x0141, 8, 1)  # Command code, parameter size, type
            angular_command_value = struct.pack('<d', angular_velocity)  # Double precision value
            angular_command = angular_command_head + angular_command_value
            sock.sendto(angular_command, (MOTION_HOST_IP, MOTION_HOST_PORT))

            # Pack Linear Velocity in X Command
            linear_x_command_head = struct.pack('<III', 0x0140, 8, 1)
            linear_x_command_value = struct.pack('<d', linear_velocity_x)
            linear_x_command = linear_x_command_head + linear_x_command_value
            sock.sendto(linear_x_command, (MOTION_HOST_IP, MOTION_HOST_PORT))

            # Pack Linear Velocity in Y Command
            linear_y_command_head = struct.pack('<III', 0x0145, 8, 1)
            linear_y_command_value = struct.pack('<d', linear_velocity_y)
            linear_y_command = linear_y_command_head + linear_y_command_value
            sock.sendto(linear_y_command, (MOTION_HOST_IP, MOTION_HOST_PORT))

            print(f"Command sent: Angular={angular_velocity}, X={linear_velocity_x}, Y={linear_velocity_y} (Iteration {i+1}/{iterations})")

            time.sleep(interval)  # Wait for 50ms to maintain 20Hz frequency

        print("Velocity commands completed.")
    except ValueError:
        print("Error: Invalid input. Please enter numeric values.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    set_combined_velocity()
