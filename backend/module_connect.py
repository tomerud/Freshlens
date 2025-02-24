from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import eventlet
import gridfs
import ssl
from datetime import datetime, timedelta
from backend.mysqlDB.items.insert_new_item_to_db import insert_item_to_db
from backend.mysqlDB.items.handle_item_update import handle_camera_update

import os

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

# Connect to MongoDB and set up GridFS
client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

def insert_items(camera_ip, item_list):
    """Iterates over the item_list and inserts each item into the 'item' table."""
    for item in item_list:
        required_fields = ['item_id', 'is_inserted_by_user', 'product_id', 'camera_ip', 'date_entered', 'anticipated_expiry_date']
        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            print(f"Warning: Missing required fields {missing_fields} in item: {item}. Skipping insertion.")
            continue
        
        insert_item_to_db(
            item_id=item['item_id'],
            is_inserted_by_user=item['is_inserted_by_user'],
            product_id=item['product_id'],
            camera_ip=item['camera_ip'],
            date_entered=item['date_entered'],
            anticipated_expiry_date=item['anticipated_expiry_date'],
            remove_from_fridge_date=item.get('remove_from_fridge_date'),
            is_rotten=item.get('is_rotten', 0)
        )
        print(f"Inserted item_id={item['item_id']} into the database.")

@socketio.on("connect")
def handle_connect():
    print("Client connected.")

@socketio.on("send_to_db")
def handle_send_to_db(data):
    camera_ip = data.get('camera_ip')
    products_data = data.get('products_data')
    print(f"Received data from camera {camera_ip}")
    
    item_list = []
    for product in products_data:
        track_id, class_id, exp_date = product
        current_date = datetime.today().date()

        # Determine anticipated expiry date and compute is_rotten
        if isinstance(exp_date, int):
            expiry_datetime = datetime.today() + timedelta(days=exp_date)
            anticipated_expiry_date = expiry_datetime.strftime("%Y-%m-%d")
        else:
            anticipated_expiry_date = exp_date
            expiry_datetime = datetime.strptime(exp_date, "%Y-%m-%d")
        
        # Set is_rotten to 1 if current date is greater than anticipated expiry date
        is_rotten = 1 if current_date > expiry_datetime.date() else 0

        item = {
            "item_id": track_id,
            "is_inserted_by_user": 0,
            "product_id": class_id,
            "camera_ip": camera_ip,
            "date_entered": datetime.today().strftime("%Y-%m-%d"),
            "anticipated_expiry_date": anticipated_expiry_date,
            "remove_from_fridge_date": None,
            "is_rotten": is_rotten
        }
        item_list.append(item)
        print(f"Prepared item: {item}")

    handle_camera_update(camera_ip, item_list)

@socketio.on("send_to_mongo")
def handle_send_to_mongo(data):
    image_base64 = data.get('image_base64')
    user_id = data.get('user_id')
    camera_ip = data.get('camera_ip')
    timestamp = data.get('timestamp')
    
    if not image_base64 or not user_id or not camera_ip:
        print("Error: Missing required fields 'image_base64', 'user_id', or 'camera_ip'.")
        return

    # Make sure to import decode_and_store_image if needed.
    decode_and_store_image(image_base64, user_id, camera_ip, timestamp)

@socketio.on("error_in_module")
def stream_error(data):
    ip = data.get('camera_ip')
    port = data.get('port')
    error_message = data.get('error')
    print(f"Received error from module at camera {ip}:{port}: {error_message}")
    with open("error_log.txt", "a") as file:
        file.write(f"{ip}:{port} - {error_message}\n")

if __name__ == "__main__":
    print("Starting Flask-SocketIO server on port 5000 with SSL...")

    # Construct absolute paths to the certificate files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(current_dir, "server.cert")
    key_path = os.path.join(current_dir, "server.key")
    print("Using certificate:", cert_path)
    print("Using key:", key_path)

    secure_socket = eventlet.wrap_ssl(
        eventlet.listen(('0.0.0.0', 5000)),
        certfile=cert_path,
        keyfile=key_path,
        server_side=True
    )

    # Start the server using the wrapped SSL socket.
    eventlet.wsgi.server(secure_socket, app)
