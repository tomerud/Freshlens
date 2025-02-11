from pymongo import MongoClient
import gridfs
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]  

fs = gridfs.GridFS(db)

def store_image(file_path):
    filename = os.path.basename(file_path)  # for the correct name
    
    with open(file_path, "rb") as image_file:
        image_id = fs.put(image_file, filename=filename)  
    print(f"Image stored with ID(should be camera ip): {image_id}, Filename {filename}")

relative_path = os.path.join("backend", "mongo", "images", "cucamber.jpeg")
absolute_path = os.path.abspath(relative_path)

store_image(absolute_path)
