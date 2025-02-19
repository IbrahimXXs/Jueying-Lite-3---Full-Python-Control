import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def switch_to_move_mode():
    """
    Sends the command to switch the robot to Move Mode.
    """
    command_code = 0x21010D06
    paramters_size = 0
    command_type = 0
    command_head = struct.pack('<III', command_code, paramters_size, command_type)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Move Mode Command sent.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    switch_to_move_mode()
