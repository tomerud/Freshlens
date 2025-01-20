from flask import Blueprint, request, jsonify
from DB.shelves.insert_shelf import insert_new_shelf_to_db



shelves_bp = Blueprint('shelves_bp', __name__)

@shelves_bp.route('/addd_shelf', methods=['POST'])
def add_shelf():
    data = request.get_json()
    if not data or "fridge_id" not in data or "shelve_name" not in data:
        return jsonify({"error": "Invalid data format"}), 400

    insert_new_shelf_to_db(data["fridge_id"], data["shelve_name"])
    return jsonify({"message": "shelve added successfully!", "data": data}), 200


