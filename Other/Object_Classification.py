import cv2
import numpy as np
from ultralytics import YOLO  # YOLOv8 library

def access_and_classify_objects():
    """
    Access the wide-angle camera of the robot and classify objects in real time using YOLOv8.
    """
    model = YOLO("/home/ibrahim/Documents/Lite 3 Full Control (Python)/Other/Object_Assets/yolov8l.pt")  # Using the YOLOv8 Nano model (small and fast)
    # Replace with the correct RTSP URL for the robot
    rtsp_url = "rtsp://192.168.1.120:8554/test"

    # Open the video stream
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Failed to open video stream. Please check the RTSP URL and robot connection.")
        return

    print("Press 'q' to exit the video stream.")

    # Load YOLOv8 model

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from the video stream.")
                break

            # Run YOLOv8 model inference on the frame
            results = model(frame)

            # Loop through detected objects
            for result in results[0].boxes.data.tolist():
                x_min, y_min, x_max, y_max, confidence, class_id = result
                if confidence > 0.35:  # Confidence threshold
                    label = f"{model.names[int(class_id)]}: {confidence:.2f}"
                    color = (0, 255, 0)  # Green for bounding boxes

                    # Draw the bounding box and label
                    cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)
                    cv2.putText(frame, label, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Display the frame
            cv2.imshow("Jueying Lite3 Object Classification (YOLOv8)", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting the video stream.")
                break
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Release the video capture and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    access_and_classify_objects()
