import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def turn_back_180():
    """
    Sends the command to turn the robot back by 180 degrees.
    """
    command_code = 0x21010C0A
    command_value = 15  # Turn back by 180°
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Turned back by 180°.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    turn_back_180()
