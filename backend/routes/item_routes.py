from flask import Blueprint, request, jsonify
from mysqlDB.items.insert_new_item_to_db import insert_item_to_db
from datetime import date

item_bp = Blueprint('item_bp', __name__)

@item_bp.route('/insert_item', methods=['POST'])
def insert_item():
    try:
        data = request.get_json()

        required_fields = ["item_id", "is_inserted_by_user", "product_id", "camera_ip", "date_entered", "anticipated_expiry_date", "is_rotten"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields. Required: {', '.join(required_fields)}"}), 400

        data["date_entered"] = date.fromisoformat(data["date_entered"])
        data["anticipated_expiry_date"] = date.fromisoformat(data["anticipated_expiry_date"])

        insert_item_to_db(
            item_id=data["item_id"],
            is_inserted_by_user=data["is_inserted_by_user"],
            product_id=data["product_id"],
            camera_ip=data["camera_ip"],
            date_entered=data["date_entered"],
            anticipated_expiry_date=data["anticipated_expiry_date"],
            is_rotten=data["is_rotten"]
        )

        return jsonify({"message": "Item inserted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
