from datetime import datetime
import base64
import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple
from socketio import Client
import threading

socket = Client()
lock = threading.Lock()
def sendToDB(socket,camera_ip: str, port: int, expDate: List[Tuple[int, int, Tuple[int, int, int, int], str]]) -> None:

    data = {
        "camera_ip": camera_ip,
        "port": port,
        "products_data": expDate     
    }
    try:
        # Acquire the lock before emitting data
        with lock:
            socket.emit("send_to_db", data)
        print(f"Data sent to backend for DB: {data}")
    except Exception as e:
        print(f"Error sending data to backend for DB: {e}")

#depends on tomer:
#from bson import Binary
def sendToMongo(socket,camera_ip: str,port:int, image: Image.Image):
    # Convert PIL Image to NumPy array
    image_np = np.array(image)
    
    # Convert RGB to BGR (OpenCV uses BGR)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    _, buffer = cv2.imencode('.jpg', image_bgr)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    data = {
        "camera_ip": camera_ip,
        "image": image_base64
    }
    try:
        # Acquire the lock before emitting data
        with lock:
            socket.emit("send_to_mongo", data)
        print(f"Data sent to backend for MongoDB: {data}")
    except Exception as e:
        print(f"Error sending data to backend for MongoDB: {e}")

if __name__ == "__main__":  # Testing
    try:
        socket.connect("http://127.0.0.1:5000") 
        print("SocketIO connection established.")
    except Exception as e:
        print(f"Error connecting to SocketIO server: {e}")
        exit(1)

    camera_ip = "10.0.0.1"
    port=8554
    expDate = [1, 2, (100, 200, 300, 400), "2025-02-01"]
    image = cv2.imread("example.jpg")

    sendToDB(camera_ip, expDate)
    sendToMongo(camera_ip, image)

    socket.disconnect()
    print("SocketIO connection closed.")
