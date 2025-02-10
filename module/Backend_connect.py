"""
Backend Connection Module

Handles communication with the backend database and MongoDB via socket connections.
"""

import base64
import io
import time
import threading
from typing import List, Tuple
from PIL import Image

# TODO:
# 1. Secure connection (Auth token, SSL/TLS)
# 2. Create Readme file
# 3. Fix reconnection in MongoDB


lock = threading.Lock()
MAX_RETRIES = 10  # Max attempts before giving up
RETRY_DELAY = 1   # Time (in seconds) to wait between retries

def send_to_db(
    socket,
    camera_ip: str,
    port: int,
    exp_date: List[Tuple[int, int, Tuple[int, int, int, int], str]]
    ) -> None:
    """Sends data to MySQL database via socket connection."""
    data = {
        "camera_ip": camera_ip,
        "port": port,
        "products_data": exp_date[1:]  # Exclude shelf if no detections
    }

    for attempt in range(MAX_RETRIES):
        try:
            with lock:
                socket.emit("send_to_db", data)
            print(f"Data sent to backend for DB: {data}")
            return
        except (ConnectionError, TimeoutError) as error:
            print(f"Error sending data to backend for DB: {error}")

        if not socket.connected:
            print(f"Socket disconnected. Retrying {attempt+1}...")
            time.sleep(RETRY_DELAY + attempt)

    print("Failed to send data to MySQL after multiple attempts. Dropping the message.")

def send_to_mongo(socket, camera_ip: str, _port: int, image: Image.Image) -> None:
    """Sends image data to MongoDB via socket connection."""
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    data = {
        "camera_ip": camera_ip,
        "image": image_base64
    }

    for attempt in range(MAX_RETRIES):
        try:
            with lock:
                socket.emit("send_to_mongo", data)
            print(f"Data sent to backend for MongoDB: {data}")
            return
        except (ConnectionError, TimeoutError) as error:
            print(f"Error sending data to backend for MongoDB: {error}")

        if not socket.connected:
            print(f"Socket disconnected. Retrying {attempt+1}...")
            time.sleep(RETRY_DELAY + attempt)

    print("Failed to send data to Mongo after multiple attempts. Dropping the message.")

def alert_server(socket, camera_ip: str, port: int, error_message: str) -> None:
    """Sends an error alert to the server via socket connection."""
    data = {
        "camera_ip": camera_ip,
        "port": port,
        "error": error_message
    }

    for attempt in range(MAX_RETRIES):
        try:
            with lock:
                socket.emit("error_in_module", data)
            print(f"Error sent to server: {data}")
            return
        except (ConnectionError, TimeoutError) as error:
            print(f"Error sending message to backend: {error}")

        if not socket.connected:
            print(f"Socket disconnected. Retrying {attempt+1}...")
            time.sleep(RETRY_DELAY + attempt)

    print("Failed to send error message after multiple attempts. Dropping the message.")
