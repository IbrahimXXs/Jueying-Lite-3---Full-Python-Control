import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def send_stop_command():
    """
    Sends the STOP command for software-based emergency stop.
    """
    command_code = 0x21020C0E
    paramters_size = 0
    command_type = 0
    command_head = struct.pack('<III', command_code, paramters_size, command_type)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("STOP Command sent.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    send_stop_command()
