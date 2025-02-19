import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def enable_auto_stop():
    """
    Sends the command to enable the auto stop function.
    """
    command_code = 0x21012109
    command_value = 0x20  # Enable auto stop function
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Enabled auto stop function.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    enable_auto_stop()
