import os
import gridfs
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

def store_image(file_path, camera_ip):
    filename = os.path.basename(file_path)  # Extract filename

    with open(file_path, "rb") as image_file:
        image_id = fs.put(image_file, filename=filename, metadata={"camera_ip": camera_ip})
    
    print(f"Image stored with ID: {image_id}, Camera IP: {camera_ip}, Filename: {filename}")
    return image_id

# Example Usage
camera_ip = "192.168.1.100"
relative_path = os.path.join("backend", "mongo", "demo-images", "one.jpg")
absolute_path = os.path.abspath(relative_path)

store_image(absolute_path, camera_ip)




