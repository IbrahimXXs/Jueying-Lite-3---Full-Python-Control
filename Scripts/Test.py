import cv2
import subprocess
import pyrealsense2 as rs
import numpy as np
import threading

def start_gstreamer_pipeline():
    """
    Start the GStreamer pipeline to stream the RGB video feed.
    """
    rtsp_url = "rtsp://192.168.1.120:8554/test"

    gstreamer_command = [
        "gst-launch-1.0",
        f"rtspsrc location={rtsp_url} latency=0",
        "!",
        "rtph264depay",
        "!",
        "h264parse",
        "!",
        "nvh264dec",
        "!",
        "videoconvert",
        "!",
        "autovideosink"
    ]

    try:
        print("Starting GStreamer pipeline for RGB stream...")
        gst_process = subprocess.Popen(" ".join(gstreamer_command), shell=True)
        return gst_process
    except Exception as e:
        print(f"Error occurred while running GStreamer pipeline: {e}")
        return None

def access_depth_stream():
    """
    Access and display depth stream from the RealSense camera.
    """
    # Configure depth stream
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # Depth stream

    try:
        # Start the RealSense pipeline
        print("Starting RealSense depth stream...")
        pipeline.start(config)

        while True:
            # Wait for the depth frame
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            if not depth_frame:
                continue

            # Convert depth frame to a numpy array
            depth_image = np.asanyarray(depth_frame.get_data())

            # Apply a colormap for visualization
            depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
            )

            # Display the depth frame
            cv2.imshow("RealSense Depth Stream", depth_colormap)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting depth stream...")
                break
    except Exception as e:
        print(f"Error occurred while accessing RealSense depth stream: {e}")
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Depth stream stopped.")

def access_camera_with_depth():
    """
    Start both the GStreamer RGB stream and RealSense depth stream concurrently.
    """
    gst_process = None
    try:
        # Start the GStreamer pipeline in a separate thread
        gst_process = start_gstreamer_pipeline()

        # Start the depth stream in the main thread
        access_depth_stream()

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure the GStreamer process is terminated
        if gst_process:
            gst_process.terminate()
            print("GStreamer pipeline terminated.")

if __name__ == "__main__":
    access_camera_with_depth()
