import base64
import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple
import threading
import time

#TODO:

# 1. **Secure connection**
#    - Auth token
#    - SSL/TLS
# 2. **Create Readme file**

"""
Backend Connection Design:

Decision:
- Use a single shared socket for all cameras, guarded by a thread lock to enforce sequential access,
  so we avoid concurrency issues.
- Socket auto reconnects with exponential backoff - we have set it to 10 tries, with max delay of 30.

Rationale:
- Avoids managing multiple connections.
- Aviods overwhelming the server with excessive connections.

Known Limitations:
- Potential throughput bottleneck.
- Latency increases if cameras block each other waiting for the lock.

Future Considerations:
- Switch to multiple sockets.
- Learn more about Asyncio - according to sources online it might be better than the approach here, maybe even instead of threading
  will need to learn about it more deeply to understand if and where it fits.
- multiprocessing instead? 
- GIL forces us to initilaize yolo in each thread seperatly
- Consider the right parameters for the Recorvy/Reconnection.

"""


lock = threading.Lock()
max_retries = 10  # Max attempts before giving up
retry_delay = 4   # Time (in seconds) to wait between retries

def sendToDB(socket,camera_ip: str, port: int, expDate: List[Tuple[int, int, Tuple[int, int, int, int], str]]) -> None:
    #  Recive data and socket, and emit it to server (to Mysql db)
    #  Returns:None 

    data = {
        "camera_ip": camera_ip,
        "port": port,
        "products_data": expDate     
    }
    for attempt in range(max_retries):
        if socket.connected: # we already have a thread that trys to recconect, so we only need to wait for it to succeed
            try:
                with lock: # protect from concurrency on the shared resource - socket
                    socket.emit("send_to_db", data)
                print(f"Data sent to backend for DB: {data}")
                return  # Success, exit function
            except Exception as e:
                print(f"Error sending data to backend for DB: {e}")
        print(f"Socket disconnected. Waiting to retry {attempt+1}/{max_retries}...")
        time.sleep(retry_delay)
    print("Failed to send data after multiple attempts. Dropping the message.")


#depends on tomer:
#from bson import Binary
def sendToMongo(socket,camera_ip: str,port:int, image: Image.Image):
    #  Recive data and socket, and emit it to server (to Mongo db)
    #  Returns:None 

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
    for attempt in range(max_retries):
        if socket.connected: # we already have a thread that trys to recconect, so we only need to wait for it to succeed
            try:
                with lock: # protect from concurrency on the shared resource - socket
                    socket.emit("send_to_mongo", data)
                print(f"Data sent to backend for MongoDB: {data}")
                return  # Success, exit function
            except Exception as e:
                print(f"Error sending data to backend for MongoDB: {e}")
        print(f"Socket disconnected. Waiting to retry {attempt+1}/{max_retries}...")
        time.sleep(retry_delay)
    print("Failed to send data after multiple attempts. Dropping the message.")

