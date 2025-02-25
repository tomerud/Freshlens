import socketio
from module.backend_connect import send_to_db, send_to_mongo
from PIL import Image
import base64
import io
import time
# Setup SocketIO client (using SSL verification disabled for testing)
socket= socketio.Client(
    reconnection=True,
    reconnection_attempts=10,
    reconnection_delay=1,
    reconnection_delay_max=30,
    ssl_verify=False
) 

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
# camera_ip = "10.0.0.1"
# port=8554

camera_ip = "192.168.1.100"
port = 8554
"""
tomer camera Ip, port and a list
    [(product_id,class_id,exp date)]
"""
detections = [(-1,-1,1),(1,2, "2025-02-01"),(4,5, "2025-03-30"),(8,5, "2025-03-11")]
send_to_db(socket,camera_ip,port, detections)
time.sleep(1)
detections = [(-1, -1, (-1, -1, -1, -1), -1)]
send_to_db(socket,camera_ip,port, detections)

# image = Image.open("assets/shelf.jpg")
# send_to_mongo(socket, camera_ip, port, image)
