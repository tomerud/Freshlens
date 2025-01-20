from flask import Blueprint, request, jsonify
from DB.fridge.insert_fridge_to_db import insert_new_fridge_to_db
from DB.fridge.get_fridges import get_fridges_from_db


fridge_bp = Blueprint('fridge_bp', __name__)

@fridge_bp.route('/add_fridge', methods=['POST'])
def add_fridge():
    data = request.get_json()
    if not data or "user_id" not in data or "fridge_name" not in data:
        return jsonify({"error": "Invalid data format. 'user_id' and 'fridge_name' are required."}), 400

    insert_new_fridge_to_db(data["user_id"], data["fridge_name"])
    return jsonify({"message": "Fridge added successfully!", "data": data}), 200


@fridge_bp.route('/get_all_fridges', methods=['GET'])
def get_all_fridges():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    fridges = get_fridges_from_db(user_id)
    return jsonify({"message": "All fridges returned successfully!", "fridges": fridges}), 200
