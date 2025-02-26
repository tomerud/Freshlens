from pymongo import MongoClient
import gridfs
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import eventlet
import gridfs
import ssl
from datetime import datetime, timedelta
from mysqlDB.items.insert_new_item_to_db import insert_item_to_db
from mysqlDB.items.handle_item_update import handle_camera_update
from mongo.store_image import decode_and_store_image
import os




# Connect to MongoDB and set up GridFS
client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

# Get the first file stored in GridFS
file = fs.find_one()  # Finds the first file in GridFS

if file:
    print(f"Found file: {file.filename} (ID: {file._id})")  # Print file details
    
    # Read the image data
    image_data = file.read()

    # Display using PIL
    image = Image.open(BytesIO(image_data))
    image.show()

    # Convert to OpenCV format (Optional)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No files found in GridFS")
