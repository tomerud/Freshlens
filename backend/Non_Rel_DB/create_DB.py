from pymongo import MongoClient
import gridfs
import os

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]  

fs = gridfs.GridFS(db)

def store_image(file_path):
    filename = os.path.basename(file_path)  # for the correct name
    
    with open(file_path, "rb") as image_file:
        image_id = fs.put(image_file, filename=filename)  
    print(f"Image stored with ID(should be camera ip): {image_id}, Filename {filename}")

store_image(r"C:\studies\fourth year\eccomerce backup 2\ecommerce\backend\Non_Rel_DB\pics\cucamber.jpeg") # replace with your url
