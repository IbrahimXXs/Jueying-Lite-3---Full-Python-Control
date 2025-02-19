import socket
import struct

DEVELOPMENT_HOST_IP = "192.168.1.103"  # Replace with your machine's IP
TARGET_PORT = 43897  # The port configured in `network.toml`
BUFFER_SIZE = 1024

def parse_ultrasound(data):
    """
    Parse and extract ultrasound data from the received packet.
    Enforces the valid range of [0.28m, 4.50m].
    """
    try:
        # Assuming ultrasound data is at the end of the received structure
        if len(data) >= 16:  # Ultrasound is represented by two double-precision floats (16 bytes)
            ultrasound = struct.unpack('<2d', data[-16:])  # Parse the last 16 bytes as two doubles
            forward_distance = max(0.28, min(4.50, ultrasound[0]))  # Clamp to [0.28, 4.50]
            backward_distance = max(0.28, min(4.50, ultrasound[1]))  # Clamp to [0.28, 4.50]
            return forward_distance, backward_distance
        else:
            return None, None  # Data insufficient for ultrasound parsing
    except Exception as e:
        print(f"Error parsing ultrasound data: {e}")
        return None, None

def receive_robot_ultrasound():
    """
    Listens for robot state data sent by the motion host and extracts ultrasound data.
    """
    # Create a UDP socket to listen for incoming data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((DEVELOPMENT_HOST_IP, TARGET_PORT))

    print(f"Listening for robot data on {DEVELOPMENT_HOST_IP}:{TARGET_PORT}...")

    try:
        while True:
            # Receive data from the motion host
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(f"Received data from {addr}")

            # Parse ultrasound data
            forward_distance, backward_distance = parse_ultrasound(data)

            if forward_distance is not None and backward_distance is not None:
                print(f"Ultrasound Data - Forward: {forward_distance:.2f} m, Backward: {backward_distance:.2f} m")
            else:
                print("Ultrasound Data - Unable to parse.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sock.close()

if __name__ == "__main__":
    receive_robot_ultrasound()
