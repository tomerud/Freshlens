import base64
import io
from PIL import Image
from typing import List, Tuple
import threading
import time

#TODO:

# 1. **Secure connection**
#    - Auth token
#    - SSL/TLS
# 2. **Create Readme file**
# 3. **fix reconnection**
#    - in mongo DB

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
retry_delay = 1   # Time (in seconds) to wait between retries

def sendToDB(socket,camera_ip: str, port: int, expDate: List[Tuple[int, int, Tuple[int, int, int, int], str]]) -> None:
    #  Recive data and socket, and emit it to server (to Mysql db)
    #  Returns:None 

    data = {
        "camera_ip": camera_ip,
        "port": port,
        "products_data": expDate[1:] #evaluate to empty list if no detections expect shelf    
    }
    for attempt in range(max_retries): #in case of problem with sending the data - retry
        try:
            with lock:  # protect from concurrency
                socket.emit("send_to_db", data)
            print(f"Data sent to backend for DB: {data}")
            return  
        except Exception as e:
            print(f"Error sending data to backend for DB: {e}")
        
        if not socket.connected:
            print(f"Socket disconnected. Retrying {attempt+1}...")
            time.sleep(retry_delay+attempt) # wait for the reconnection - socket setting handle this
    
    print("Failed to send data to Mysql after multiple attempts. Dropping the message.")


def sendToMongo(socket, camera_ip: str, port: int, image: Image.Image):
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")  
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    data = {
        "camera_ip": camera_ip,
        "image": image_base64
    }

    for attempt in range(max_retries): #in case of problem with sending the data - retry
        try:
            with lock:  # protect from concurrency
                socket.emit("send_to_mongo", data)
            print(f"Data sent to backend for MongoDB: {data}")
            return  
        except Exception as e:
            print(f"Error sending data to backend for MongoDB: {e}")
        
        if not socket.connected:
            print(f"Socket disconnected. Retrying {attempt+1}...")
            time.sleep(retry_delay+attempt) # wait for the reconnection - socket setting handle this
    
    print("Failed to send data to Mongo after multiple attempts. Dropping the message.")

def alert_server(socket, camera_ip: str, port: int,error_message: str):
    data = {
        "camera_ip": camera_ip,
        "port": port,
        "error": error_message     
    }
    for attempt in range(max_retries): #in case of problem with sending the data - retry
        try:
            with lock:  # protect from concurrency
                socket.emit("error_in_module", data)# Emit an alert event with the error message to the server            
                print(f"Error sent to server: {data}")
            return  
        except Exception as e:
            print(f"Error sending message to backend: {e}")
        
        if not socket.connected:
            print(f"Socket disconnected. Retrying {attempt+1}...")
            time.sleep(retry_delay+attempt) # wait for the reconnection - socket setting handle this
    
    print("Failed to send error message after multiple attempts. Dropping the message.")
    
