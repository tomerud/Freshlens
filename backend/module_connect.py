from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image
import os
from datetime import datetime
from Non_Rel_DB.store_pic import decode_and_store_image



app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("send_to_db")
def handle_send_to_db(data):
    """ you get camera Ip, port and a list
    [(product_id,class_id,exp date)]
    format of exp date -> with Elya!

    """
    # Handle the data 
    print("Received data for DB:", data)
    
    
@socketio.on("send_to_mongo")
def handle_send_to_mongo(data):
    """ you get camera Ip, port and an image
    decide how you want the data to be encoded / sent - image_base64, image_Binary, nparray etc
    """
    user_id=1 #test
    decode_and_store_image(data["image"], user_id, data["camera_ip"])
    # Handle the data
    return

@socketio.on("error_in_module")
def stream_error(data):
    # Handle the stream error alert from the client
    ip = data['camera_ip']
    port = data['port']
    error_message = data['error']
    print(f"Received error from module: at camera {ip}:{port} , {error_message}")
    # log the error, alert the user
    with open("error_log.txt", "a") as file:
        file.write(f": {error_message}\n")

if __name__ == "__main__":
    print("Starting Flask-SocketIO server on port 5000...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
