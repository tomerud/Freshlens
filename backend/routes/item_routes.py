# routes/item_routes.py
from flask import Blueprint, request, jsonify
from DB.items.insert_new_item_to_db import insert_new_item_to_db


item_bp = Blueprint('item_bp', __name__)

@item_bp.route('/insert_item', methods=['POST'])
def insert_items_from_shelves():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    insert_new_item_to_db(data["product_id"], data["fridge_id"], data["shelf_id"], data["fridge_id"], data["date_entered"], data["anticipated_expiry_date"], data["is_rotten"])
    return jsonify({"message": "Fridge added successfully!", "data": data}), 200

