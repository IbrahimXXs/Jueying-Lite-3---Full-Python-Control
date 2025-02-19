import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def perform_backflip():
    """
    Sends the command to make the robot perform the Backflip action.
    """
    command_code = 0x21010502
    command_value = 0
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Backflip action performed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    perform_backflip()
