# routes/item_routes.py
from flask import Blueprint, request, jsonify

item_bp = Blueprint('item_bp', __name__)

@item_bp.route('/get_items_from_shelves', methods=['GET'])
def get_items_from_shelves():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    # call for get items here...

    return jsonify({"message": "List of objects retrieved successfully", "data": data}), 200
