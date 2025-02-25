import socketio
from module.backend_connect import send_to_db, send_to_mongo
from PIL import Image
import base64
import io
import time
from datetime import datetime, timedelta

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
# camera_ip = "10.0.0.1"
# port=8554

camera_ip = "192.168.1.100"
port = 8554
"""
tomer camera Ip, port and a list
    [(product_id,class_id,exp date)]
"""
# for testing
# detections = [
#     (-1, -1, 1),
#     (10, 2, "2019-02-01"),
#     (7, 5, "2020-03-30"),
#     (8, 5, "2020-03-11"),
#     (23, 5, "2020-03-11"),
#     (22, 1, "2020-03-11")
# ]

# # Generate a detection for each week between Jan 1, 2023 and Dec 31, 2024.
# start_date = datetime(2023, 1, 1)
# end_date = datetime(2024, 12, 31)
# current_date = start_date

# while current_date <= end_date:
#     # Create a unique item_id and cycle through some class IDs (1 to 5) as an example.
#     week_index = (current_date - start_date).days // 7
#     item_id = 1000 + week_index
#     class_id = (week_index % 5) + 1  # cycles class id: 1,2,3,4,5,1,2,...
    
#     # Format the date as a string.
#     date_str = current_date.strftime("%Y-%m-%d")
    
#     # Append the new detection tuple.
#     detections.append((item_id, class_id, date_str))
    
#     # Move to the next week.
#     current_date += timedelta(weeks=1)

# send_to_db(socket, camera_ip, port, detections)

detections = [(-1,-1,1),(10, 2, "2019-02-01"),(7,5, "2020-03-30"),(8,5, "2020-03-11"), (23,5, "2020-03-11"), (22.,1, "2020-03-11")]
send_to_db(socket,camera_ip,port, detections)
# time.sleep(1)
# detections = [(-1, -1, (-1, -1, -1, -1), -1)]
# send_to_db(socket,camera_ip,port, detections)

# image = Image.open("assets/shelf.jpg")
# send_to_mongo(socket, camera_ip, port, image)
