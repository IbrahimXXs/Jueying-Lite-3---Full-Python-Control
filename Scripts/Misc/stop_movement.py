import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def stop_movement():
    """
    Sends the command to stop the robot's movement.
    """
    command_code = 0x21010C0A
    command_value = 7  # Stop
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Robot movement stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    stop_movement()
