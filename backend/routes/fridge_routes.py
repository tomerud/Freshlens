from flask import Blueprint, request, jsonify
from DB.fridge.insert_fridge_to_db import insert_new_fridge_to_db
from DB.products.products_queries import get_all_categories_from_db, get_fridge_product_items_from_db, get_fridge_products_by_category_from_db
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
    fridges_list = [{"fridge_id": row[0], "fridge_name": row[1]} for row in fridges]

    return jsonify(fridges_list), 200


@fridge_bp.route('/get_all_categories', methods=['GET'])
def get_all_categories():
    """
    Fetches all categories from the database and returns them as JSON.
    """
    fridge_id = request.args.get("fridge_id")

    if not fridge_id:
        return jsonify({"error": "Missing fridge_id parameter"}), 400

    try:
        fridge_id = int(fridge_id)
    except ValueError:
        return jsonify({"error": "Invalid fridge_id. Must be an integer."}), 400

    categories = get_all_categories_from_db(fridge_id)
    category_list = [{"category_id": row[0], "category_name": row[1]} for row in categories]

    return jsonify(category_list), 200



@fridge_bp.route('/get_all_products', methods=['GET'])
def get_all_products():
    """
    Fetches all products from the database and returns them as JSON.
    """
    fridge_id = request.args.get("fridge_id")
    category_name = request.args.get("category_name")

    if not fridge_id or not category_name:
        return jsonify({"error": "Missing fridge_id or category_name parameter"}), 400

    try:
        fridge_id = int(fridge_id)
    except ValueError:
        return jsonify({"error": "Invalid fridge_id. Must be an integer."}), 400
    
    products = get_fridge_products_by_category_from_db(fridge_id, category_name)
    products_list = [{"product_id": row[0], "product_name": row[1]} for row in products]

    return jsonify(products_list), 200



@fridge_bp.route('/get_all_product_items', methods=['GET'])
def get_all_product_items():
    """
    Fetches all products from the database and returns them as JSON.
    """
    fridge_id = request.args.get("fridge_id")
    product_id = request.args.get("product_id")

    if not fridge_id or not product_id:
        return jsonify({"error": "Missing fridge_id or product_id parameter"}), 400

    try:
        fridge_id = int(fridge_id)
    except ValueError:
        return jsonify({"error": "Invalid fridge_id. Must be an integer."}), 400
    
    items = get_fridge_product_items_from_db(fridge_id, product_id)
    items_list = [{"product_name": row[0], "is_rotten": row[1]} for row in items]

    return jsonify(items_list), 200