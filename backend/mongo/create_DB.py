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

image_paths = [
    os.path.join("mongo", "demo-images", "one.jpg"),
    os.path.join("mongo", "demo-images", "two.jpg"),
    os.path.join("mongo", "demo-images", "three.jpg"),
]

camera_ips = [
    "192.168.1.100",
    "192.168.1.101",
    "192.168.1.102"
]

absolute_paths = [os.path.abspath(path) for path in image_paths]

for path, ip in zip(absolute_paths, camera_ips):
    store_image(path, ip)




