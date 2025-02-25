"""
Camera Event Scheduling and Object Detection

This module manages the event driven camera monitoring system using:
- SocketIO for real time communication with the server.
- Threading for handling multiple cameras.
- Call all the other file functions for the module functionality
"""

import signal
import threading
from ultralytics import YOLO
import socketio

from module.detect_and_track import process_video
from module.backend_connect import send_to_db, send_to_mongo, alert_server
from module.pass_obj_to_exp_date import find_exp_date
from module.draw_bb import draw_on_image

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
# 7. ALERT SERVERS!!

# Setup SocketIO client
socket_client = socketio.Client(
    reconnection=True,
    reconnection_attempts=10,
    reconnection_delay=1,
    reconnection_delay_max=30,
    ssl_verify=False
)  # Client will attempt to reconnect when disconnected.

@socket_client.event
def connect():
    print("Connected to SocketIO server.")

@socket_client.event
def disconnect():
    print("Disconnected from SocketIO server.")

def connect_to_socket():
    try:
        socket_client.connect("wss://127.0.0.1:5000", transports=["websocket"])
        print("SocketIO connected.")
    except Exception as e:
        print(f"Error connecting to SocketIO server: {e}")

# Connect before sending any data
connect_to_socket()

stop_event = threading.Event()

def handle_signal(_sig, _frame):
    """Handle termination signals."""
    print("Received termination signal. Stopping all threads")
    stop_event.set()  # Signal all threads to stop.

# Set up signal handler for termination.
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal) # had problem with just ctrl+c

def event_listen(client, cam_ip: str, cam_port: int, demo: bool, video_stream: str = "stream") -> None:
    """Listen for events from a camera and process video streams."""
    # Load the YOLO model and class list
    model, class_list = load_model()

    while not stop_event.is_set():
        event = get_event_from_camera(cam_ip, cam_port, demo)
        if event == "light_detected":
            handle_light_detected(cam_ip, cam_port, video_stream, model, class_list, client)

    print(f"Stopped event listener for camera {cam_ip}:{cam_port}")

def load_model():
    """
    Load the YOLO model
    return: model and class list.
    """
    model_path = "models/ProductDetection.pt"
    model = YOLO(model_path)
    class_list = [class_name for _, class_name in sorted(model.names.items())]
    return model, class_list

def handle_light_detected(cam_ip: str, cam_port: int, video_stream: str, model, class_list, client):
    """Handles light detection by processing the video stream."""
    rtsp_path = f"rtsp://{cam_ip}:{cam_port}/{video_stream}"

    try:
        # Process the video stream -> get detections -> find expiration date -> draw on image -> send to DB and MongoDB
        detections = process_video(rtsp_path, model)
        if detections in (-1, None):
            alert_server(client, cam_ip, cam_port, "Error: Unable to open video stream.")
            return
        exp_date = find_exp_date(detections, class_list)
        fimg = draw_on_image(exp_date)
        send_to_db(client, cam_ip, cam_port, exp_date)
        send_to_mongo(client, cam_ip, cam_port, fimg)

    # error handling
    except IOError:
        print("I/O error occurred while processing video.")
        alert_server(client, cam_ip, cam_port, "I/O error occurred while processing video.")
    except ValueError:
        print("Value error encountered in video processing.")
        alert_server(client, cam_ip, cam_port, "Value error encountered in video processing.")
    except RuntimeError as err:
        print(f"Runtime error: {err}")
        alert_server(client, cam_ip, cam_port, "Runtime error encountered.")

def get_event_from_camera(_cam_ip: str, _cam_port: int, demo: bool) -> str:
    """
    Simulate getting an event from a camera.
    Return: The event type ("light_detected" or "no_light_detected").
    future work - handle this according to the camers configurations
    """
    if demo:
        return "light_detected"
    return "no_light_detected"

# Start listener for each camera.
camera_info = [("10.0.0.1", 8554, "concatenated-sample")]
threads = []
for ip, port, stream in camera_info:
    thread = threading.Thread(
        target=event_listen,
        args=(socket_client, ip, port, True, stream),  # Demo mode is True.
        daemon=False
    )
    threads.append(thread)
    print(f"starting thread for camera:{ip}, port:{port}") 
    thread.start()

try:
    # Keep the main thread alive, but allow SIGINT to stop it
    while not stop_event.is_set():
        pass  # Do nothing, just wait for SIGINT
except KeyboardInterrupt:
    print("KeyboardInterrupt received - CTRL+C pressed. Stopping all threads.")
    stop_event.set()

for thread in threads:
    thread.join()  # Block the main thread until all threads are done.

print("All threads stopped. Exiting.")