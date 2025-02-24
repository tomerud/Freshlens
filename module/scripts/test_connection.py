import socketio
from module.backend_connect import send_to_db,send_to_mongo
from PIL import Image
import base64
import io

# Setup socketIO client - I ahve updated the setup, need to check updated version
socket = socketio.Client(ssl_verify=False)

@socket.event
def connect():
    print(f"Connected to SocketIO server.")

@socket.event
def disconnect():
    print(f"Disconnected from SocketIO server.")

# Connect to SocketIO before threads start
def connect_to_socket():
    try:
        socket.connect("wss://127.0.0.1:5000",transports=["websocket"]) 
        print("SocketIO connected.")
    except Exception as e:
        print(f"Error connecting to SocketIO server: {e}")

connect_to_socket()
camera_ip = "10.0.0.1"
port=8554
"""
tomer camera Ip, port and a list
    [(product_id,class_id,exp date)]
"""
detections = [(-1,-1,1),(1,2, "2025-02-01"),(4,5, "2025-03-04")]
send_to_db(socket,camera_ip,port, detections)
detections = [(-1, -1, (-1, -1, -1, -1), -1)]
send_to_db(socket,camera_ip,port, detections)

#image = Image.open("assets/shelf.jpg")
#send_to_mongo(socket,camera_ip,port, image)