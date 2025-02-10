from flask import Blueprint, request, jsonify, Response
from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["image_database"]
fs = gridfs.GridFS(db)

picture_bp = Blueprint('picture_bp', __name__)

@picture_bp.route('/get_picture', methods=['GET'])
def get_picture():
    try:
        # Hardcode user_id and camera_ip
        user_id = "user123"
        camera_ip = "192.168.1.10"

        # Find the most recent image with those fields
        latest_image = fs.find_one(
            {"metadata.user_id": user_id, "metadata.camera_ip": camera_ip},
            sort=[("uploadDate", -1)]
        )

        if not latest_image:
            return jsonify({"error": f"No image found for user_id={user_id} and camera_ip={camera_ip}"}), 404

        # Convert to base64
        image_data = latest_image.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        return jsonify({
            "user_id": user_id,
            "camera_ip": camera_ip,
            "image_base64": image_base64,
            "timestamp": latest_image.metadata.get("time")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def serve_pil_image(pil_img):
    """Optional helper to return a PIL image directly as JPEG in HTTP response."""
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return Response(img_io, mimetype='image/jpeg')
