from flask import Blueprint, request, jsonify
from mongo.mongo_utils import get_latest_image_by_camera_ip
from mysqlDB.user.user_queries import get_user_camera_ips

image_bp = Blueprint('image_bp', __name__)

@image_bp.route('/get_image', methods=['GET'])
def get_image():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user_id parameter"}), 400

        camera_ips = get_user_camera_ips(user_id)
        if not camera_ips:
            return jsonify({"error": f"No cameras found for user_id={user_id}"}), 404

        fridge_images = {}

        for entry in camera_ips:
            camera_ip = entry["camera_ip"]
            fridge_id = entry["fridge_id"]
            fridge_name = entry["fridge_name"]

            image_data = get_latest_image_by_camera_ip(camera_ip)
            if image_data:
                print("timestamp:", image_data["timestamp"])
                if fridge_id not in fridge_images:
                    fridge_images[fridge_id] = {
                        "fridge_id": fridge_id,
                        "fridge_name": fridge_name,
                        "images": []
                    }
                fridge_images[fridge_id]["images"].append({
                    "camera_ip": camera_ip,
                    **image_data
                })
                print(fridge_images[fridge_id]["images"])

        if not fridge_images:
            return jsonify({"error": f"No images found for user_id={user_id}"}), 404

        return jsonify({
            "user_id": user_id,
            "fridges": list(fridge_images.values())
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
