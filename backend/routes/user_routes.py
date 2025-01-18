
from flask import Blueprint, request, jsonify
from DB.user.insert_user_to_db import insert_new_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/sign_user', methods=['POST'])
def sign_user():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    if "@" not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400

    insert_new_user(data["firstName"], data["lastName"], data["email"], data["subscription"])
    return jsonify({"message": "User signed up successfully!", "data": data}), 200