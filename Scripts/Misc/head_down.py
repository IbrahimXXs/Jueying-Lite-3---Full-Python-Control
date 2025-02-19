import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def move_head_down():
    """
    Sends the command to move the robot's head down.
    """
    command_code = 0x21010C0A
    command_value = 8  # Head down
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Head moved down.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    move_head_down()
