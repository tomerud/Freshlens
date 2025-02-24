import socketio
from module.backend_connect import send_to_db, send_to_mongo
from PIL import Image
import base64
import io

# Setup SocketIO client (using SSL verification disabled for testing)
socket = socketio.Client(ssl_verify=False)

@socket.event
def connect():
    print("Connected to SocketIO server.")

@socket.event
def disconnect():
    print("Disconnected from SocketIO server.")

def connect_to_socket():
    try:
        socket.connect("wss://127.0.0.1:5000", transports=["websocket"])
        print("SocketIO connected.")
    except Exception as e:
        print(f"Error connecting to SocketIO server: {e}")

# Connect before sending any data
connect_to_socket()

camera_ip = "192.168.1.100"
port = 8554

"""
Example data format:
  A list of products where each product is a list of tuples.
  Each tuple contains (track_id, class_id, exp_date)
"""
detections = [
    [(-1, -1, 1)],
    [ (3, 2, "2026-02-01"), (4, 2, "2026-02-01"), (5, 2, "2026-02-01")]
]

# Emit data to the server using send_to_db function.
send_to_db(socket, camera_ip, port, detections)

# Uncomment below to send an image via MongoDB
# image = Image.open("assets/shelf.jpg")
# send_to_mongo(socket, camera_ip, port, image)
