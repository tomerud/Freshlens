from flask import Blueprint, request, jsonify
from DB.fridge.insert_fridge_to_db import insert_new_fridge

fridge_bp = Blueprint('fridge_bp', __name__)

@fridge_bp.route('/add_fridge', methods=['POST'])
def sign_user():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    insert_new_fridge(data["user_id"], data["fridge_name"])
    return jsonify({"message": "fridge added succesfuly!", "data": data}), 200