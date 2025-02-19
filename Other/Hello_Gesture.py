import cv2
import mediapipe as mp
import socket
import struct
import time

# Robot Motion Host Information
MOTION_HOST_IP = "192.168.1.120"
MOTION_HOST_PORT = 43893

# Function to send the "Hello" command to the robot
def send_hello_command():
    """
    Sends the "Hello" command to the robot.
    """
    command_code = 0x21010507
    command_value = 0
    command_type = 0
    command_head = struct.pack('<III', command_code, command_value, command_type)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(command_head, (MOTION_HOST_IP, MOTION_HOST_PORT))
        print("Hello action performed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

# Function to access the wide-angle camera and detect an open palm
def access_wide_angle_camera_with_gesture_detection():
    """
    Access the wide-angle camera of the robot, detect an open palm gesture, and send a "Hello" command.
    """
    rtsp_url = "rtsp://192.168.1.120:8554/test"  # Replace with your robot's RTSP URL
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Failed to open video stream. Please check the RTSP URL and robot connection.")
        return

    print("Press 'q' to exit the video stream.")

    # Mediapipe Hands setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    # Cooldown timer to prevent repeated Hello commands
    last_hello_time = 0
    hello_cooldown = 8  # Cooldown in seconds

    # Process every nth frame to optimize performance
    frame_skip = 5  # Process every 5th frame
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from the video stream.")
                break

            # Skip processing for frames to improve performance
            frame_count += 1
            if frame_count % frame_skip != 0:
                cv2.imshow("Jueying Lite3 Wide-Angle Camera with Gesture Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            # Convert the frame to RGB for Mediapipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame to detect hands
            results = hands.process(frame_rgb)

            # Draw hand landmarks and detect open palm
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Check if the hand is an open palm
                    landmarks = hand_landmarks.landmark

                    # Calculate the relative positions of key points
                    thumb_tip = landmarks[4]
                    index_tip = landmarks[8]
                    middle_tip = landmarks[12]
                    ring_tip = landmarks[16]
                    pinky_tip = landmarks[20]
                    wrist = landmarks[0]

                    # If all fingers are open and pointing away from the wrist, it's an open palm
                    if (
                        thumb_tip.y < wrist.y and
                        index_tip.y < wrist.y and
                        middle_tip.y < wrist.y and
                        ring_tip.y < wrist.y and
                        pinky_tip.y < wrist.y
                    ):
                        current_time = time.time()
                        if current_time - last_hello_time > hello_cooldown:
                            print("Open palm detected!")
                            send_hello_command()
                            last_hello_time = current_time

            # Display the frame
            cv2.imshow("Jueying Lite3 Wide-Angle Camera with Gesture Detection", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting the video stream.")
                break
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

if __name__ == "__main__":
    access_wide_angle_camera_with_gesture_detection()
