import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def perform_twist_jump():
    """
    Sends the command to make the robot perform the Twist Jump action.
    """
    command_code = 0x2101020D
    command_value = 0
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Twist Jump action performed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    perform_twist_jump()
