from flask import Blueprint, request, jsonify
from mysqlDB.camera.insert_camera_to_db import insert_camera_to_db


camera_bp = Blueprint('camera_bp', __name__)

@camera_bp.route('/add_camera', methods=['POST'])
def add_camera():
    try:
        data = request.get_json()
        if not data or "camera_ip" not in data or "fridge_id" not in data:
            return jsonify({"error": "Invalid data format. 'camera_ip' and 'fridge_id' are required."}), 400

        insert_camera_to_db(camera_ip=data["camera_ip"], fridge_id=data["fridge_id"])

        return jsonify({"message": "Camera added successfully!", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
