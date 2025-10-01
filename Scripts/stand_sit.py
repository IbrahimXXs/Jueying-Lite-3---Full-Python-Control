import socket
import struct

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def send_stand_sit_command():
    """
    Sends the Stand/Sit toggle command.
    """
    command_code = 0x21010202
    param1 = 0
    param2 = 0
    payload = struct.pack('<3i', command_code, param1, param2)  # signed int
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(payload, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Stand/Sit Command sent.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    send_stand_sit_command()
