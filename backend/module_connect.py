from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import eventlet
import gridfs
import base64
from io import BytesIO
from PIL import Image
import os
from datetime import datetime
#from Non_Rel_DB.store_pic import decode_and_store_image
import ssl
from mongo.store_image import decode_and_store_image
from mysqlDB.items.handle_item_update import handle_camera_update



app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet") # async_mode eventlet is not really relevant right now, but for future work, when we want to have multiple modules that connect to the server
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

# data is a list of dics in this format. is inserted_by_user = 0 always. items with missing fields will be ignore for now.
REQUIRED_FIELDS = [
    "item_id",
    "is_inserted_by_user",
    "product_id",
    "camera_ip",
    "date_entered",
    "anticipated_expiry_date",
    "remove_from_fridge_date",
    "is_rotten"
]

def validate_item(item):
    """ Ensures all required fields are present."""
    missing_fields = [field for field in REQUIRED_FIELDS if field not in item]
    
    if missing_fields:
        print(f" Warning: Item {item.get('item_id', 'UNKNOWN')} is missing fields: {missing_fields}")
        return False

    if not isinstance(item['item_id'], int):
        print(f"Error: 'item_id' must be an integer. Found: {type(item['item_id'])}")
        return False
    
    if not isinstance(item['is_inserted_by_user'], int):
        print(f"Error: 'is_inserted_by_user' must be an integer (0 or 1). Found: {type(item['is_inserted_by_user'])}")
        return False

    if not isinstance(item['product_id'], int):
        print(f"Error: 'product_id' must be an integer. Found: {type(item['product_id'])}")
        return False

    if not isinstance(item['camera_ip'], str):
        print(f"Error: 'camera_ip' must be a string. Found: {type(item['camera_ip'])}")
        return False

    if not isinstance(item['date_entered'], str):
        print(f"Error: 'date_entered' must be a string in 'YYYY-MM-DD' format.")
        return False

    if not isinstance(item['anticipated_expiry_date'], str):
        print(f"Error: 'anticipated_expiry_date' must be a string in 'YYYY-MM-DD' format.")
        return False

    if item['remove_from_fridge_date'] is not None and not isinstance(item['remove_from_fridge_date'], str):
        print(f"Error: 'remove_from_fridge_date' must be a string in 'YYYY-MM-DD' format or None.")
        return False

    if not isinstance(item['is_rotten'], int):
        print(f"Error: 'is_rotten' must be an integer (0 or 1). Found: {type(item['is_rotten'])}")
        return False

    return True


@socketio.on("connect")
def handle_connect():
    print("Client connected.")


@socketio.on("send_to_db")
def handle_send_to_db(data):
    """
    Handles incoming data and updates the MySQL database:
    1. checks each item has required fields.
    2. Extracts the camera_ip from the first item(all of them share same ip)
    3. Calls handle_camera_update to process valid items.
    """
    camera_ip = data.get('camera_ip')
    products_data = data.get('products_data')
    print(f"Received data from camera {camera_ip}")
        
    for product in products_data:
        track_id = product[0]
        class_id = product[1]
        exp_date= product[2]
        print(f"Product with track_id {track_id} and class_id {class_id} has expiry date {exp_date}")
    #handle_camera_update(camera_ip, product)

    
    
@socketio.on("send_to_mongo")
def handle_send_to_mongo(data):
    """ Handles image storage in MongoDB:
    Expects data with fields: 'image_base64', 'user_id', 'camera_ip', and the time the pic was taken.
    timestamp is reccomended but will work without it as well.
    """
    image_base64 = data.get('image_base64')
    user_id = data.get('user_id')
    camera_ip = data.get('camera_ip')
    timestamp = data.get('timestamp')
    if not image_base64 or not user_id or not camera_ip:
        print("Error: Missing required fields 'image_base64', 'user_id', or 'camera_ip'.")
        return

    decode_and_store_image(image_base64, user_id, camera_ip, timestamp)


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
    

    print("Starting Flask-SocketIO server on port 5000 with SSL...")
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.cert", keyfile="server.key")

    secure_socket = eventlet.wrap_ssl(
        eventlet.listen(('0.0.0.0', 5000)), 
        certfile="server.cert",
        keyfile="server.key",
        server_side=True
    )

    # Start the eventlet WSGI server with the wrapped socket
    eventlet.wsgi.server(secure_socket, app)
