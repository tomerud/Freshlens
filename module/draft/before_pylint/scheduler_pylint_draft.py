"""
Camera Event Scheduling and Object Detection

This module manages the event driven camera monitoring system using:
- SocketIO for real time communication with the server.
- Threading for handling multiple cameras.
- Call all the other file functions for the module functionality

Functions each thread does independently:
    - event_listen: Listens for camera events and processes video streams.
    - load_model: Loads the YOLO model and returns the model with class labels.
    - handle_light_detected: Handles object detection when light is detected.
    - get_event_from_camera: Simulates receiving an event from a camera.

"""

import signal
import threading
from ultralytics import YOLO
import socketio

from detect_and_track import process_video
from backend_connect import send_to_db, send_to_mongo, alert_server
from pass_obj_to_expDate import find_exp_date
from draw_bb import draw_on_image

#TODO:
# 1. **Threading** - think about where / if Thread - GIL , Multiproccess
# 2. **Demo** - change demo configuration
# 3. **connection to db and threading** Should the for loop be switched with while?
#    - Update the Ip list from DB?
# 4. **Secure conneciton** - future work
#    - replace the RTSP with Secure RTSP / vpn etc
# 5. ** YOLO resizing**:
#    - think if resizing training or scaling!!!!
# 6. ** Add SSL/TLS / mTLS**

# Setup SocketIO client
socket_client = socketio.Client(
    reconnection=True,
    reconnection_attempts=10,
    reconnection_delay=1,
    reconnection_delay_max=30
)  # Client will attempt to reconnect when disconnected.

@socket_client.event
def connect():
    """Handle connection to the SocketIO server."""
    print("Connected to SocketIO server.")

@socket_client.event
def disconnect():
    """Handle disconnection from the SocketIO server."""
    print("Disconnected from SocketIO server.")

def event_listen(socket_client, camera_ip: str, port: int, demo: bool, stream: str = "stream") -> None:
    """
    Listen for events from a camera and process video streams.

    Args:
        socket_client: The SocketIO client instance.
        camera_ip (str): The IP address of the camera.
        port (int): The port of the camera.
        demo (bool): Whether to run in demo mode.
        stream (str): The stream name (default: "stream").
    """
    stop_event = threading.Event()  # Signal to stop all threads.

    def handle_signal(sig, frame):
        """Handle termination signals."""
        stop_event.set()  # Set the stop event to signal termination.
        print(f"Stopping event listener for camera {camera_ip}:{port}...")

    # Set up signal handler for graceful termination.
    signal.signal(signal.SIGINT, handle_signal)

    # Load the YOLO model and class list
    model, class_list = load_model()

    while not stop_event.is_set():
        event = get_event_from_camera(camera_ip, port, demo)
        if event == "light_detected":
            handle_light_detected(camera_ip, port, stream, model, class_list, socket_client)

    print(f"Stopped event listener for camera {camera_ip}:{port}...")

def load_model():
    """Load the YOLO model and return the model and class list."""
    model_path = "Models/ProductDetection.pt"
    model = YOLO(model_path)
    class_list = [class_name for _, class_name in sorted(model.names.items())]
    return model, class_list

def handle_light_detected(camera_ip: str, port: int, stream: str, model, class_list, socket_client):
    """Handles light detection by processing the video stream."""
    rtsp_path = f"rtsp://{camera_ip}:{port}/{stream}"

    try:
        detections = process_video(rtsp_path, model)
        if detections in (-1, None):
            error_message = "Error: Unable to open video stream."
            alert_server(socket_client, camera_ip, port, error_message)
            return

        exp_date = find_exp_date(detections, class_list)
        fimg = draw_on_image(exp_date)
        send_to_db(socket_client, camera_ip, port, exp_date)
        send_to_mongo(socket_client, camera_ip, port, fimg)
    except Exception as error:
        print(f"Error processing video: {error}")
        error_message = "Error processing video."
        alert_server(socket_client, camera_ip, port, error_message)

def get_event_from_camera(camera_ip: str, port: int, demo: bool) -> str:
    """
    Simulate getting an event from a camera.

    Args:
        camera_ip (str): The IP address of the camera.
        port (int): The port of the camera.
        demo (bool): Whether to run in demo mode.

    Returns:
        str: The event type ("light_detected" or "no_light_detected").
    """
    if demo:
        return "light_detected"
    return "no_light_detected"


# Connect to the server.
socket_client.connect("http://127.0.0.1:5000")

# Start listener for each camera.
camera_info = [("10.0.0.1", 8554, "concatenated-sample")]
threads = []
for ip, port, stream in camera_info:
    thread = threading.Thread(
        target=event_listen,
        args=(socket_client, ip, port, stream, True),  # Demo mode is True.
        daemon=False
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()  # Block the main thread until all threads are done.
