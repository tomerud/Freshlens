
from flask import Blueprint, request, jsonify
from DB.user.insert_user_to_db import insert_new_user
from DB.user.user_queries import is_user_already_known_in_db, update_user_subscription_in_db

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/is_user_already_known', methods=['GET'])
def is_user_already_known():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    try:
        result = is_user_already_known_in_db(user_id)
        return jsonify({"known": result}), 200
    except Exception as e:
            return jsonify({"error": str(e)}), 500

@user_bp.route('/update_user_subscription', methods=['POST'])
def update_user_subscription():
    """Updates the subscription_id for a user based on user_id"""
    data = request.json
    user_id = data.get("user_id")
    new_subscription_id = data.get("new_subscription_id")

    if not user_id or not new_subscription_id:
        return jsonify({"error": "user_id and new_subscription_id are required."}), 400

    try:
        update_user_subscription_in_db(user_id, new_subscription_id)
        return jsonify({"message": "User Subscription updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/sign_user', methods=['POST'])
def sign_user():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    if "@" not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400

    default_subscription_type = 'free'

    try:
        insert_new_user(data["userId"], data["userName"], data["email"], default_subscription_type)
        return jsonify({"message": "User signed up successfully!", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500