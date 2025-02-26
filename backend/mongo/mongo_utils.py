import base64
import gridfs
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

def get_latest_image_by_camera_ip(camera_ip):
    latest_image = fs.find_one(
        {"metadata.camera_ip": camera_ip},
        sort=[("uploadDate", -1)]
    )

    if not latest_image:
        return None

    image_data = latest_image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    return {
    "camera_ip": camera_ip,
    "image_base64": image_base64,  # no prefix
    "timestamp": latest_image.upload_date.isoformat()
    }
