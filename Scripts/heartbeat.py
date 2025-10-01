import socket
import struct
import threading
import time

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

def heartbeat_loop(stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_code = 0x21040001  # Heartbeat
    param1, param2 = 0, 0
    payload = struct.pack('<3i', command_code, param1, param2)

    try:
        while not stop_event.is_set():
            sock.sendto(payload, (MOTION_HOST_IP, MOTION_HOST_PORT))
            time.sleep(0.1)  # every 100ms
    finally:
        sock.close()

def start_heartbeat():
    """
    Start heartbeat in a background thread.
    Returns a tuple (thread, stop_event).
    """
    stop_event = threading.Event()
    thread = threading.Thread(target=heartbeat_loop, args=(stop_event,), daemon=True)
    thread.start()
    return thread, stop_event
