from flask import Blueprint, request, jsonify
from mysqlDB.fridge.insert_fridge_to_db import insert_new_fridge_to_db
from mysqlDB.products.products_queries import get_all_categories_from_db, get_freshness_score_from_db, get_fridge_product_items_from_db, get_fridge_products_by_category_from_db, get_general_tips_from_db, get_product_name_from_db, get_product_nutrient_data, get_product_price_from_db, get_specific_product_tips_from_db
from mysqlDB.fridge.get_fridges import get_fridge_name_from_db, get_fridges_from_db


fridge_bp = Blueprint('fridge_bp', __name__)

@fridge_bp.route('/add_fridge', methods=['POST'])
def add_fridge():
    data = request.get_json()
    if not data or "user_id" not in data or "fridge_name" not in data:
        return jsonify({"error": "Invalid data format. 'user_id' and 'fridge_name' are required."}), 400

    insert_new_fridge_to_db(data["user_id"], data["fridge_name"])
    return jsonify({"message": "Fridge added successfully!"}), 200


@fridge_bp.route('/get_all_fridges', methods=['GET'])
def get_all_fridges():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    fridges = get_fridges_from_db(user_id)
    
    return jsonify(fridges), 200

@fridge_bp.route('/get_fridge_name', methods=['GET'])
def get_fridge_name():
    fridge_id = request.args.get("fridge_id")
    if not fridge_id:
        return jsonify({"error": "fridge_id query parameter is required."}), 400

    fridge_names = get_fridge_name_from_db(fridge_id)
  
    return jsonify(fridge_names), 200


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

    return jsonify(categories), 200


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

    return jsonify(products), 200


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
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "Invalid fridge_id or product_id. Must be an integer."}), 400
    
    items = get_fridge_product_items_from_db(fridge_id, product_id)
    
    return jsonify(items), 200


@fridge_bp.route('/get_product_nutrient', methods=['GET'])
def get_product_nutrient():
    """
    Fetches product nutrient data from the database and returns it as JSON.
    """
    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify({"error": "Missing product_id parameter"}), 400

    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "Invalid product_id. Must be an integer."}), 400

    nutrient_data = get_product_nutrient_data(product_id)

    if not nutrient_data:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(nutrient_data[0]), 200



@fridge_bp.route('/get_product_price', methods=['GET'])
def get_product_price():
    """
    Fetches product nutrient data from the database and returns it as JSON.
    """
    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify({"error": "Missing product_id parameter"}), 400

    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "Invalid product_id. Must be an integer."}), 400

    product_price = get_product_price_from_db(product_id)

    if not product_price:
        return jsonify({"product_name": None, "avg_price": None}), 200

    return jsonify(product_price[0]), 200


@fridge_bp.route('/get_product_tips', methods=['GET'])
def get_product_tips():
    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify({"error": "Missing product_id parameter"}), 400

    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "Invalid product_id. Must be an integer."}), 400
    
    tips = get_specific_product_tips_from_db(product_id)

    if not tips or all(tip is None for tip in tips):
        return jsonify([]), 200
    
    return jsonify(tips), 200


@fridge_bp.route('/get_general_storage_tips', methods=['GET'])
def get_general_storage_tips():

    tips = get_general_tips_from_db()
    if not tips or all(tip is None for tip in tips):
        return jsonify([]), 200
    
    return jsonify(tips), 200


@fridge_bp.route('/get_product_name', methods=['GET'])
def get_product_name():
    """
    Fetches product nutrient data from the database and returns it as JSON.
    """
    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify({"error": "Missing product_id parameter"}), 400

    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "Invalid product_id. Must be an integer."}), 400

    product_name = get_product_name_from_db(product_id)

    return jsonify(product_name[0]), 200


@fridge_bp.route('/get_freshness_score', methods=['GET'])
def get_freshness_score():
    """
    Get the avg freshness of the items in all user's fridges.
    We calculate the freshness of item like that:
    100% - until 4 days before expiration
    80% - 3 days before expiration
    60% - 2 days before expiration
    40% - 1 day before expiration
    20% - the day of expiration
    0% - if the expiration day already passed

   We want to encorage the user to eat the products instead of over tagging them as rotten.
    """
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id query parameter is required."}), 400

    freshness_score = get_freshness_score_from_db(user_id)
    # print(freshness_score['avg_freshness_score'])
    
    return jsonify(freshness_score), 200
