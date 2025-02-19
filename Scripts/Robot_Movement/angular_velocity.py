import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def set_angular_velocity():
    """
    Sets the angular velocity of the robot (rad/s).
    """
    command_code = 0x0141
    command_type = 1  # Complex command
    value_range = [-1.5, 1.5]  # Allowed range

    try:
        value = float(input(f"Enter Angular Velocity (rad/s) [{value_range[0]} to {value_range[1]}]: "))
        if value < value_range[0] or value > value_range[1]:
            print(f"Error: Value must be within range {value_range}.")
            return

        # Pack command
        command_head = struct.pack('<III', command_code, 8, command_type)  # 8 bytes for a double value
        command_value = struct.pack('<d', value)  # Double precision
        command = command_head + command_value

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(command, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print(f"Angular velocity set to {value} rad/s.")
    except ValueError:
        print("Error: Invalid input. Please enter a numeric value.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    set_angular_velocity()
