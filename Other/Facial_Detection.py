import cv2
import time
import mediapipe as mp
import ollama
import threading
import queue

# Initialize Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Finger landmark indices (Tip and Lower Knuckle Points)
FINGER_TIPS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
FINGER_MCP = [2, 6, 10, 14, 18]  # MCP Knuckles for comparison

# Queue for non-blocking Mistral communication
mistral_queue = queue.Queue()

def count_fingers(hand_landmarks, handedness):
    """
    Count the number of fingers raised in the detected hand.
    """
    finger_count = 0
    landmarks = hand_landmarks.landmark

    # Adjust thumb detection based on left/right hand
    if handedness == "Right":
        thumb_extended = landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_MCP[0]].x  # Right hand: thumb moves right
    else:
        thumb_extended = landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_MCP[0]].x  # Left hand: thumb moves left

    if thumb_extended:
        finger_count += 1

    # Count the 4 fingers by comparing tip to lower knuckle
    for i in range(1, 5):
        if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_MCP[i]].y:  # Tip is above knuckle
            finger_count += 1

    return finger_count

def ask_mistral_async(finger_count):
    """
    Runs Mistral query asynchronously and logs the response.
    """
    word_count = finger_count * 10
    print(f"🟡 Sending to Mistral: 'Generate a {word_count}-word sentence.'")

    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": "You are an AI assistant that generates sentences based on word count."},
        {"role": "user", "content": f"Generate a grammatically correct {word_count}-word sentence."}
    ])

    generated_sentence = response['message']['content'].strip()
    
    print(f"🟢 Mistral Response: {generated_sentence}")  # Log the response
    mistral_queue.put(generated_sentence)  # Store response in queue

def process_rtsp_camera(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)  # Use FFmpeg for better RTSP handling
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffering
    cap.set(cv2.CAP_PROP_FPS, 30)  # Maintain higher FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ Error: Could not open RTSP stream.")
        return

    print("✅ Press 'q' to quit.")
    last_analysis_time = time.time()
    analysis_interval = 5.0  # Only send to Mistral every 1 second
    mistral_response = "Waiting for response..."

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame.")
            break

        # Convert frame to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        finger_count_text = "No Hand Detected"

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label  # "Right" or "Left"
                finger_count = count_fingers(hand_landmarks, hand_label)
                finger_count_text = f"Fingers: {finger_count}"

                # Only send to Mistral every 1 second (async)
                if time.time() - last_analysis_time >= analysis_interval:
                    last_analysis_time = time.time()
                    mistral_thread = threading.Thread(target=ask_mistral_async, args=(finger_count,))
                    mistral_thread.start()  # Run Mistral request in a separate thread

                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Check if Mistral has responded with a sentence
        if not mistral_queue.empty():
            mistral_response = mistral_queue.get()

        # Display finger count & sentence
        cv2.putText(frame, finger_count_text, (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display Mistral-generated sentence
        y_offset = 100
        for line in mistral_response.split(". "):  # Split long sentence for display
            cv2.putText(frame, line, (20, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 30

        # Show the video feed
        cv2.imshow("RTSP Camera - Finger Detection + Mistral Sentence", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rtsp_url = "rtsp://192.168.1.120:8554/test"
    process_rtsp_camera(rtsp_url)
