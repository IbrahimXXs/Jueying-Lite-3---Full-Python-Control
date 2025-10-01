from pynput import keyboard
import socket
import struct
import time
import threading
import cv2
import os

MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

# Maximum speed limits
MAX_LINEAR_SPEED = 0.5
MAX_ANGULAR_SPEED = 0.5

# Velocities
angular_velocity = 0.0
linear_velocity_x = 0.0
linear_velocity_y = 0.0

# Key state tracking
key_states = {
    'w': False,
    's': False,
    'a': False,
    'd': False,
    'left': False,
    'right': False
}

# Function to send velocity commands
def send_velocity_command(angular_velocity, linear_velocity_x, linear_velocity_y):
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Pack Angular Velocity Command
        angular_command_head = struct.pack('<III', 0x0141, 8, 1)
        angular_command_value = struct.pack('<d', angular_velocity)
        angular_command = angular_command_head + angular_command_value
        sock.sendto(angular_command, (MOTION_HOST_IP, MOTION_HOST_PORT))

        # Pack Linear Velocity in X Command
        linear_x_command_head = struct.pack('<III', 0x0140, 8, 1)
        linear_x_command_value = struct.pack('<d', linear_velocity_x)
        linear_x_command = linear_x_command_head + linear_x_command_value
        sock.sendto(linear_x_command, (MOTION_HOST_IP, MOTION_HOST_PORT))

        # Pack Linear Velocity in Y Command
        linear_y_command_head = struct.pack('<III', 0x0145, 8, 1)
        linear_y_command_value = struct.pack('<d', linear_velocity_y)
        linear_y_command = linear_y_command_head + linear_y_command_value
        sock.sendto(linear_y_command, (MOTION_HOST_IP, MOTION_HOST_PORT))

        print(f"Command sent: Angular={angular_velocity}, X={linear_velocity_x}, Y={linear_velocity_y}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

# Function to access the wide-angle camera
import os

def access_wide_angle_camera():
    rtsp_url = "rtsp://192.168.1.120:8554/test"
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Failed to open video stream. Please check the RTSP URL and robot connection.")
        return

    print("Press 'q' to exit the video stream.")

    last_saved_time = time.time()
    frame_save_dir = "saved_frames"
    os.makedirs(frame_save_dir, exist_ok=True)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from the video stream.")
                break

            # Display the frame in a window
            cv2.imshow("Jueying Lite3 Wide-Angle Camera", frame)

            # Save a frame every 1 second
            current_time = time.time()
            if current_time - last_saved_time >= 1.0:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(frame_save_dir, f"frame_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Saved frame: {filename}")
                last_saved_time = current_time

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting the video stream.")
                break
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


# Function to update velocities based on key states
def update_velocities():
    global angular_velocity, linear_velocity_x, linear_velocity_y

    while True:
        linear_velocity_x = MAX_LINEAR_SPEED if key_states['w'] else -MAX_LINEAR_SPEED if key_states['s'] else 0.0
        linear_velocity_y = MAX_LINEAR_SPEED if key_states['a'] else -MAX_LINEAR_SPEED if key_states['d'] else 0.0
        angular_velocity = MAX_ANGULAR_SPEED if key_states['right'] else -MAX_ANGULAR_SPEED if key_states['left'] else 0.0

        send_velocity_command(angular_velocity, linear_velocity_x, linear_velocity_y)
        time.sleep(0.05)  # Maintain 20Hz frequency

# Function to handle key press events
def on_press(key):
    try:
        if key.char in key_states:
            key_states[key.char] = True
    except AttributeError:
        if key == keyboard.Key.left:
            key_states['left'] = True
        elif key == keyboard.Key.right:
            key_states['right'] = True

# Function to handle key release events
def on_release(key):
    try:
        if key.char in key_states:
            key_states[key.char] = False
    except AttributeError:
        if key == keyboard.Key.left:
            key_states['left'] = False
        elif key == keyboard.Key.right:
            key_states['right'] = False

        if key == keyboard.Key.esc:
            return False

# Main function to control the robot
def control_robot_with_keyboard():
    # Start the camera feed in a separate thread
    camera_thread = threading.Thread(target=access_wide_angle_camera)
    camera_thread.daemon = True
    camera_thread.start()

    # Start the velocity update loop in a separate thread
    velocity_thread = threading.Thread(target=update_velocities)
    velocity_thread.daemon = True
    velocity_thread.start()

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    control_robot_with_keyboard()
