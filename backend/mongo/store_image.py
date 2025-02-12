from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

def decode_and_store_image(image_base64, user_id, camera_ip, timestamp=None):
  
    # Decode base64 to binary image data
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))

    filename = f"{camera_ip}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpeg"

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store in MongoDB 
    with BytesIO() as output:
        image.save(output, format="JPEG")
        image_binary = output.getvalue()
        image_id = fs.put(image_binary, filename=filename, metadata={
            "user_id": user_id,
            "camera_ip": camera_ip,
            "time": timestamp
        })

    print(f" Image stored with ID: {image_id}, Filename: {filename}, User ID: {user_id}, Camera IP: {camera_ip}, Time: {timestamp}")




